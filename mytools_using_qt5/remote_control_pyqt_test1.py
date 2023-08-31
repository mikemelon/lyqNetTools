import sys
import io
import os
import time
import subprocess
from qt5.remote_control1 import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from socket import socket, AF_INET, SOCK_STREAM
from PIL import Image
from common_utils.config_loader import get_config
from net_utils.scapy_utils import get_local_ip
import remote_desktop.server as rd_server


# TODO: 目前多个远程控制命令共用同一个线程，这样一个命令执行完毕后，才可能执行另外一个。
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('../images/logo2.png'))
        self.setFixedSize(self.width(), self.height()) # 设置窗口不可调整大小

        self.send_to_remote_button.clicked.connect(self.send_to_remote)
        self.remote_execute_thread = None
        self.remote_desktop_thread = None
        self.desktop_broadcast_server_process = None

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
            cmd_str = 'REMOTE_DESKTOP ' + get_local_ip() + ' 8001'
            self.remote_desktop_thread = RemoteDesktopWorkThread()
            self.remote_desktop_thread.start()
        elif self.desktop_broadcast_radio.isChecked():
            cmd_str = 'OPEN_DESKTOP_BROADCAST'
            self.start_desktop_broadcast_server()
        elif self.close_desktop_broadcast_radio.isChecked():
            cmd_str = 'CLOSE_DESKTOP_BROADCAST'
            self.stop_desktop_broadcast_server()

        self.remote_execute_thread = WorkThread1(remote_ip, cmd_str)
        self.remote_execute_thread.start()
        self.response_browser.setText('开始远程控制！')

    def start_desktop_broadcast_server(self):
        try:
            server_location = get_config('desktop_broadcast','webrtc_streamer_location',
                                         trim_double_quote=True)
            self.desktop_broadcast_server_process = subprocess.Popen([os.path.join(server_location,
                                                                                   'webrtc-streamer.exe'),
                                                                      '-H', '0.0.0.0:9001', 'screen://3'],
                                                                     cwd=server_location, shell=False)
        except Exception as ex:
            print('Exception wile start desktop_broadcast_server:{}'.format(ex))

    def stop_desktop_broadcast_server(self):
        try:
            if self.desktop_broadcast_server_process:
                self.desktop_broadcast_server_process.terminate()
                self.desktop_broadcast_server_process.kill()
                time.sleep(1) # 会造成界面失去响应
                os.system('taskkill /t /f /pid {}'.format(self.desktop_broadcast_server_process.pid)) # /t选项，关闭自己和由它启动的子进程
        except Exception as ex:
            print('Exception while Stopping desktop_broadcast_server:', ex)


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
        self.signals.emit(ex)  # 只返回异常信息


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_win = MyWindow()
    my_win.show()
    sys.exit(app.exec_())
