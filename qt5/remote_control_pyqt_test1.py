import sys
import io
import time
from remote_control1 import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from socket import socket, AF_INET, SOCK_STREAM
from PIL import Image


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height()) # 设置窗口不可调整大小

        self.send_to_remote_button.clicked.connect(self.send_to_remote)
        self.remote_execute_thread = None

    def send_to_remote(self):
        remote_ip = self.remote_ip_edit.text()
        remote_user = self.remote_user_edit.text()
        remote_password = self.remote_password_edit.text()
        cmd_str = 'NOTING'
        if self.reboot_radio.isChecked():
            # print(remote_ip, remote_user, remote_password)
            cmd_str = 'RESTART'
        elif  self.black_screen_radio.isChecked():
            cmd_str = 'BLACK_SCREEN'
        elif self.capture_screen_radio.isChecked():
            cmd_str = 'CAPTURE_SCREEN'
        elif self.typing_radio.isChecked():
            cmd_str = 'AUTO_TYPING'

        self.remote_execute_thread = WorkThread1(remote_ip, cmd_str)
        self.remote_execute_thread.start()
        self.response_browser.setText('开始远程控制！')


class WorkThread1(QThread):
    signals = pyqtSignal(str)

    def __init__(self, target_ip, target_cmd):
        super(WorkThread1, self).__init__()
        self.target_ip = target_ip
        self.target_cmd = target_cmd

    def run(self):
        start_time = time.time()
        try:
            serverName = self.target_ip  # Win7 remote computer
            serverPort = 12000
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            # sentence = input('Input lowercase sentence:')
            sentence = self.target_cmd
            clientSocket.send(sentence.encode())
            receivedMessage = clientSocket.recv(5 * 1024 * 1024)

            if sentence.upper() == 'CAPTURE_SCREEN':
                print('picture saved!')
                im_show = Image.open(io.BytesIO(receivedMessage))
                # im_show.save('mytest.png')  # 可以存，也可以直接打开
                im_show.show()
            else:
                print('From Server:', receivedMessage.decode())

            clientSocket.close()

            result_str = 'NOTING'
            if self.target_cmd != 'CAPTURE_SCREEN':
                result_str = receivedMessage.decode()
            print('result_str = ', result_str)
        except Exception as ex:
            print('发生异常，提示信息：{}'.format(ex))

        print('WordThread1 completed, used {:.1f} seconds'.format(time.time() - start_time))
        self.signals.emit(result_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_win = MyWindow()
    my_win.show()
    sys.exit(app.exec_())
