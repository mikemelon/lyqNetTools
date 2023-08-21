import sys
import io
import time
from qt5.remote_control1 import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from socket import socket, AF_INET, SOCK_STREAM
from PIL import Image
from common_utils.config_loader import get_config
from common_utils.file_utils import save_im_as_formatted_filename
from net_utils.scapy_utils import get_local_ip
import remote_desktop.server as rd_server
import winsound


# TODO: 目前多个远程控制命令共用同一个线程，这样一个命令执行完毕后，才可能执行另外一个。（也许这不记为Bug，而是一个Feature）
# 注：本代码在remote_control_pyqt_testtt1.py基础上进行模块化（添加了IP地址参数），并进行了若干Bug修改。
# 因此，不再维护原程序remote_control_pyqt_testtt1.py
class RemoteControlWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, ip_address=None):
        super(RemoteControlWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height()) # 设置窗口不可调整大小

        self.send_to_remote_button.clicked.connect(self.send_to_remote)

        if not ip_address:
            self.ip_address = get_local_ip()  # 默认使用本机IP
        else:
            self.ip_address = ip_address
        self.remote_ip_edit.setText(self.ip_address)
        self.remote_execute_thread = None
        self.remote_desktop_thread = None

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
        elif self.remote_desktop_radio.isChecked():
            # 远程桌面时，命令格式固定为'REMOTE_DESKTOP <rd_server_ip> <rd_server_port>'
            # 这里，rd_server_ip是指remote desktop server's ip，即远程桌面服务器的IP地址
            # 对于本应用，是指发送该命令的教师机（主控机）的本机IP地址。
            # rd_server_port固定为8001, 如需修改，可参看remote_desktop下的server.py和client.py
            rd_server_port = get_config('remote_desktop','server_port')
            cmd_str = 'REMOTE_DESKTOP ' + get_local_ip() + ' ' + rd_server_port
            self.remote_desktop_thread = RemoteDesktopWorkThread()
            self.remote_desktop_thread.start()

        self.remote_execute_thread = WorkThread1(remote_ip, cmd_str)
        self.remote_execute_thread.start()
        self.remote_execute_thread.signals.connect(self.handle_remote_execute_thread_result)
        self.response_browser.setText('开始远程控制！')

    def handle_remote_execute_thread_result(self, result_str):
        print('WordThread1 returns --> {}'.format(result_str))
        if 'Error' not in result_str:
            self.response_browser.append(result_str + '功能执行完毕！')
            winsound.Beep(350, 150)
        else:
            self.response_browser.append(result_str)
            winsound.PlaySound('SystemQuestion', winsound.SND_ALIAS)


class WorkThread1(QThread):
    signals = pyqtSignal(str)

    def __init__(self, target_ip, target_cmd):
        super(WorkThread1, self).__init__()
        self.target_ip = target_ip
        self.target_cmd = target_cmd

    def run(self):
        start_time = time.time()
        try:
            result_str = 'NOTING'
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
                saving_flag = get_config('remote_control', 'screen_saving_to_client', to_bool=True)
                if saving_flag:
                    save_im_as_formatted_filename(im_show, self.target_ip)
                im_show.show()
            else:
                print('From Server:', receivedMessage.decode())

            clientSocket.close()

            if self.target_cmd != 'CAPTURE_SCREEN':
                result_str = receivedMessage.decode()
            print('result_str = ', result_str)
        except Exception as ex:
            print('发生异常，提示信息：{}'.format(ex))
            result_str = '{}'.format(ex)

        print('WordThread1 completed, {:.1f} seconds elapsed'.format(time.time() - start_time))
        try:
            self.signals.emit(result_str)
        except Exception as ex:
            print('WorkThread1 emiting ex:{}'.format(ex))


class RemoteDesktopWorkThread(QThread):
    signals = pyqtSignal(str)

    def __init__(self):
        super(RemoteDesktopWorkThread, self).__init__()

    def run(self):
        start_time = time.time()
        try:
            rd_server.socket_service()  # 直接启动远程桌面server
        except Exception as ex:
            print('发生异常，提示信息：{}'.format(ex))

        print('RemoteDesktopWorkThread completed, used {:.1f} seconds'.format(time.time() - start_time))
        try:
            self.signals.emit('{}'.format(ex))  # 只返回异常信息
        except Exception as ex2:
            print('RemoteDesktopWorkThread emiting ex:{}'.format(ex2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # my_win = RemoteControlWindow('192.168.48.130')
    my_win = RemoteControlWindow()
    my_win.show()
    sys.exit(app.exec_())
