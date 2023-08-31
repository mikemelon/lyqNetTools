import os
import subprocess
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication
from common_utils.config_loader import get_config
from qt5.system_settings import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        self.res_ratio_combo.addItems(['16:9', '16:10', '4:3'])
        self.res_ratio_combo.setCurrentIndex(0)
        self.res_ratio_combo.currentIndexChanged.connect(self.res_ratio_combo_index_changed)

        self.start_rtsp_server_btn.clicked.connect(self.start_rtsp_server_clicked)
        self.stop_rtsp_server_button.clicked.connect(self.stop_rtsp_server_clicked)

        self.rtsp_server_name = 'easydarwin'
        if self.easydarwin_radio.isChecked():
            self.rtsp_server_name = 'easydarwin'
        elif self.mediamtx_radio.isChecked():
            self.rtsp_server_name = 'mediamtx'
        elif self.happytime_radio.isChecked():
            self.rtsp_server_name = 'happytime'

        self.easydarwin_radio.clicked.connect(self.easydarwin_radio_clicked)
        self.mediamtx_radio.clicked.connect(self.mediamtx_radio_clicked)
        self.happytime_radio.clicked.connect(self.happytime_radio_clicked)

        self.easydarwin_process = None
        self.mediamtx_process = None
        self.happytime_process = None

    def res_ratio_combo_index_changed(self, i):
        print('选中分辨率比例：{}'.format(i))
        width = self.res_width_spin.value()
        height = self.res_height_spin.value()
        if i == 0: # 16:9
            height = int(width / 16 * 9)
        elif i == 1: # 16:10
            height = int(width /10 * 9)
        elif i == 2: # 4:3
            height = int(width / 4 * 3)
        self.res_height_spin.setValue(height)

    def easydarwin_radio_clicked(self):
        self.rtsp_server_name = 'easydarwin'

    def mediamtx_radio_clicked(self):
        self.rtsp_server_name = 'mediamtx'

    def happytime_radio_clicked(self):
        self.rtsp_server_name = 'happytime'

    def start_rtsp_server_clicked(self):
        print('启动rtsp服务')
        if self.rtsp_server_name == 'easydarwin':
            self.start_easydarwin()
        elif self.rtsp_server_name == 'mediamtx':
            self.start_mediamtx()
        elif self.rtsp_server_name == 'happytime':
            self.start_happytime()

    def stop_rtsp_server_clicked(self):
        print('关闭rtsp服务')
        if self.rtsp_server_name == 'easydarwin':
            self.stop_easydarwin()
        elif self.rtsp_server_name == 'mediamtx':
            self.stop_mediamtx()
        elif self.rtsp_server_name == 'happytime':
            self.stop_happytime()

    def start_easydarwin(self):
        try:
            darwin_location = get_config('desktop_broadcast', 'easydarwin_location',
                                         trim_double_quote=True)
            self.easydarwin_process = subprocess.Popen([os.path.join(darwin_location, 'EasyDarwin.exe')],
                                                       shell=False)
        except Exception as ex:
            print('Exception wile start easydarwin:{}'.format(ex))

    def stop_easydarwin(self):
        try:
            if self.easydarwin_process:
                self.easydarwin_process.terminate()
                self.easydarwin_process.kill()
                time.sleep(2) # 会造成界面失去响应
                os.system('taskkill /t /f /pid {}'.format(self.easydarwin_process.pid)) # /t选项，关闭自己和由它启动的子进程
        except Exception as ex:
            print('Exception while Stopping easydarwin:', ex)

    def start_mediamtx(self):
        try:
            mediamtx_location = get_config('desktop_broadcast', 'mediamtx_location',
                                           trim_double_quote=True)
            self.mediamtx_process = subprocess.Popen([os.path.join(mediamtx_location, 'mediamtx.exe')],
                                                     shell=False)
        except Exception as ex:
            print('Exception wile start mediamtx:{}'.format(ex))

    def stop_mediamtx(self):
        try:
            if self.mediamtx_process:
                self.mediamtx_process.terminate()
                self.mediamtx_process.kill()
                time.sleep(2)  # 会造成界面失去响应
                os.system('taskkill /t /f /pid {}'.format(self.mediamtx_process.pid))  # /t选项，关闭自己和由它启动的子进程
        except Exception as ex:
            print('Exception while Stopping mediamtx:', ex)

    def start_happytime(self):
        try:
            # TODO: 将服务器地址改为相对路径转为的绝对路径，或从用户获取
            happytime_location = get_config('desktop_broadcast', 'happytime_location',
                                            trim_double_quote=True)
            self.happytime_process = subprocess.Popen([os.path.join(happytime_location, 'RtspServer.exe')],
                                                      shell=False, stdout=sys.stdout, stderr=sys.stderr)
            # 奇怪的是 Happytime Server没有向控制台打印任何内容, 进程启动了，占用了554(rtsp)端口，但没有像占用80(命令行下启动是占用的）
            # Happytime还有一些很好的特性，比如抓桌面、抓指定窗口、抓摄像头，抓麦克风、抓麦克风+摄像头等
            # > RtspServer -l device 显示音视频设备（摄像头、麦克风等）
            # > RtspServer -l window 显示可用窗口
            # 详细见其Manual.pdf
            # 有一个“RTP Multicast”的实验值得一做！
        except Exception as ex:
            print('Exception wile start happytime:{}'.format(ex))

    def stop_happytime(self):
        try:
            if self.happytime_process:
                self.happytime_process.terminate()
                self.happytime_process.kill()
                time.sleep(2)  # 会造成界面失去响应
                os.system('taskkill /t /f /pid {}'.format(self.happytime_process.pid))  # /t选项，关闭自己和由它启动的子进程
        except Exception as ex:
            print('Exception while Stopping happytime:', ex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())


