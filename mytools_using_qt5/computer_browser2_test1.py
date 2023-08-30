import sys
import os
import io
import subprocess
import time
from qt5.computer_browser2 import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox, QMenu, QAction
from PIL import Image
from socket import socket, AF_INET, SOCK_STREAM
from net_utils.scapy_utils import get_living_hosts_by_arp_ping, get_gateway_ip, get_local_ip
from mytools_using_qt5.remote_control_window import RemoteControlWindow
from common_utils.config_loader import get_config
from common_utils.file_utils import save_im_as_formatted_filename


class MyWindow(QMainWindow, Ui_MainWindow):
    COLUMN_CNT = 9

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('../images/logo2.png'))
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可调整大小
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置右键菜单策略

        # print('width={}, height={}'.format(self.label_1.width(), self.label_1.height()))
        self.label_1.setScaledContents(True)  # 让图片自适应控件设置的大小
        self.label_1.setPixmap(QPixmap('../images/user.jpg'))
        self.label_1.setGeometry(self.label_1.x(), self.label_1.y(), 48, 48)

        row_cnt, column_cnt = 5, 9
        self.tableWidget.setRowCount(row_cnt)
        self.tableWidget.setColumnCount(column_cnt)

        # self.tableWidget.verticalHeader().setVisible(False)  # 隐藏行题
        # self.tableWidget.horizontalHeader().setVisible(False)  # 隐藏列标题

        for m in range(row_cnt):
            for n in range(column_cnt):
                my_widget = create_computer_widget()

                self.tableWidget.setCellWidget(m, n, my_widget)
                # QTableWidgetItem()
                # self.tableWidget.setItem(m, n, )

        #
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

        # self.tableWidget.itemClicked.connect(self.item_clicked)
        # self.tableWidget.cellClicked.connect(self.cell_clicked)
        # self.tableWidget.cellDoubleClicked.connect(self.cell_double_clicked)
        self.tableWidget.customContextMenuRequested.connect(self.show_custom_contex_menu)

        self.action_quit.triggered.connect(self.menu_action_quit)
        self.action_refresh_alive.triggered.connect(self.menu_action_refresh_alive)

        self.open_screen_broadcast_btn.clicked.connect(self.open_screen_broadcast)

        self.action_start_screen_broadcast.triggered.connect(self.open_screen_broadcast)
        self.action_close_screen_broadcast.triggered.connect(self.close_scree_broadcast)

        self.living_host_dict = {}  # ip:(所在行，所在列)
        self.living_host_position_dict = {}  # (所在行，所在列): ip
        self.refresh_alive_thread = None
        self.remote_control_window = None

        #  用于桌面广播功能，实现方式：首先，启动桌面广播服务器；然后根据需要广播的IP的个数，建立线程列表list, 逐个发送命令，要求其打开桌面广播。
        self.desktop_broadcast_server_process = None
        self.desktop_broadcast_thread_list = []

    # def item_clicked(self, item:QTableWidgetItem):
    #     row, column = item.row(), item.column()
    #     print('item clicked', row, column)
    #     if (row, column) not in self.living_host_position_dict:
    #         return
    #     selected_host_ip = self.living_host_position_dict[(row, column)]
    #
    #     print('所点击的主机信息row={}, column={}, ip={}'.format(row, column, selected_host_ip))
    #     display_str = '点击主机信息：\nIP地址：{}'.format(selected_host_ip)
    #     if get_gateway_ip() == selected_host_ip:
    #         display_str += '\n'+'所选为网关'
    #     if get_local_ip() == selected_host_ip:
    #         display_str += '\n'+'所选为本机'
    #
    #     QMessageBox.about(self, '所点击的主机信息', display_str)

    # def cell_clicked(self, row, column):  # 不知道为何，使用Richtext，则cellClicked无法响应
    #     print('cell clicked', row, column)

    # def cell_double_clicked(self, row, column):  # 双击不起作用？（触发单击）
    #     print('double clicked!!!!!!')

    # 参考：PyQt 在QTableView中如何为每个单元格添加右键菜单
    # https://deepinout.com/pyqt/pyqt-questions/79_pyqt_how_to_add_a_right_click_menu_to_each_cell_of_qtableview_in_pyqt.html
    def show_custom_contex_menu(self, pos):
        try:
            menu = QMenu(self.tableWidget)
            index = self.tableWidget.indexAt(pos)

            action_1 = QAction('远程控制', self)
            action_1.triggered.connect(lambda: self.context_menu_action_remote_control(index))
            menu.addAction(action_1)

            menu.exec_(self.tableWidget.viewport().mapToGlobal(pos))
        except Exception as ex:
            print(ex)

    def context_menu_action_remote_control(self, index):
        print('右键菜单被点击--row={}, column={}'.format(index.row(), index.column()))
        if (index.row(), index.column()) not in self.living_host_position_dict:
            return
        selected_host_ip = self.living_host_position_dict[(index.row(), index.column())]
        # QMessageBox.about(self, '所点击的主机信息', selected_host_ip)
        self.remote_control_window = RemoteControlWindow(selected_host_ip)
        self.remote_control_window.show()

    def menu_action_quit(self):
        self.close()

    def menu_action_refresh_alive(self):
        self.refresh_alive_thread = RefreshAliveThread()
        self.refresh_alive_thread.start()
        self.refresh_alive_thread.signals.connect(self.update_ui)

    def update_ui(self, living_host_list):
        # for n in range(60):
        #     living_host_list.append('192.168.48.130')
        # living_host_list.append('172.28.160.99')
        living_host_list.append('172.30.66.84')
        living_host_list.append('192.168.68.223')

        num_of_hosts = len(living_host_list)
        row_num = int(num_of_hosts / MyWindow.COLUMN_CNT + 1)
        column_num_remamins = int(num_of_hosts % MyWindow.COLUMN_CNT)

        self.tableWidget.setRowCount(row_num)
        self.tableWidget.setColumnCount(MyWindow.COLUMN_CNT)
        self.tableWidget.clear()

        host_idx = 0
        # living_host_dict = {}  # ip:(所在行，所在列 )
        # living_host_position_dict = {}  # (所在行，所在列): ip
        for m in range(row_num):
            if m == row_num-1:
                current_column_cnt = column_num_remamins
            else:
                current_column_cnt = MyWindow.COLUMN_CNT
            for n in range(current_column_cnt):
                self.living_host_dict[living_host_list[host_idx]] = (m, n)
                self.living_host_position_dict[(m, n)] = living_host_list[host_idx]
                widget = create_computer_widget(ip=living_host_list[host_idx])
                if get_gateway_ip() == living_host_list[host_idx]:
                    widget = create_computer_widget(ip=living_host_list[host_idx], name='网关', border_style=1)
                elif get_local_ip() == living_host_list[host_idx]:
                    widget = create_computer_widget(ip=living_host_list[host_idx], name='本机', border_style=2)
                self.tableWidget.setCellWidget(m, n, widget)
                host_idx += 1

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.setFixedSize(widget.width() * MyWindow.COLUMN_CNT
                                      + self.tableWidget.verticalHeader().width() + 150,
                                      widget.height() * row_num + self.tableWidget.horizontalHeader().height() + 50)
        self.setFixedSize(self.tableWidget.width()+20, self.tableWidget.height()+180)
        self.label_1.setGeometry(self.label_1.x(), self.tableWidget.height()+40,
                                 self.label_1.width(), self.label_1.height())
        self.label.setGeometry(self.label.x(), self.tableWidget.height()+20, self.label.width(), self.label.height())
        self.open_screen_broadcast_btn.setGeometry(self.open_screen_broadcast_btn.x(), self.tableWidget.height()+40,
                                                   self.open_screen_broadcast_btn.width(),
                                                   self.open_screen_broadcast_btn.height())
        self.get_multiple_screen_btn.setGeometry(self.get_multiple_screen_btn.x(), self.tableWidget.height()+40,
                                                 self.get_multiple_screen_btn.width(),
                                                 self.get_multiple_screen_btn.height())

    def open_screen_broadcast(self):
        #  桌面广播功能，实现方式：首先，启动桌面广播服务器；然后根据需要广播的IP的个数，建立线程列表list, 逐个发送命令，要求其打开桌面广播。
        self.start_desktop_broadcast_server()
        desktop_broadcast_server_port = get_config('desktop_broadcast', 'server_port')
        cmd_str = 'OPEN_DESKTOP_BROADCAST ' + get_local_ip() + ' ' + desktop_broadcast_server_port
        ip_list = self.living_host_dict.keys()
        for ip in ip_list:
            thread = WorkThread1(ip, cmd_str)
            self.desktop_broadcast_thread_list.append(thread)
            thread.start()

    def close_scree_broadcast(self):
        #  关闭桌面广播实现方式：首先，关闭桌面广播服务器；然后根据需要广播的IP的个数，建立线程列表list, 逐个发送命令，要求其关闭桌面广播。
        self.stop_desktop_broadcast_server()
        cmd_str = 'CLOSE_DESKTOP_BROADCAST'
        ip_list = self.living_host_dict.keys()
        for ip in ip_list:
            thread = WorkThread1(ip, cmd_str)
            self.desktop_broadcast_thread_list.append(thread)
            thread.start()

    def start_desktop_broadcast_server(self):
        try:
            # TODO: 将服务器地址改为相对路径转为的绝对路径，或从用户获取
            server_location = r'C:\Users\mikemelon2021\Desktop\StreamingTest\webrtc-streamer-v0.8.2-dirty-Windows-AMD64-Release'
            desktop_broadcast_server_port = get_config('desktop_broadcast', 'server_port')
            self.desktop_broadcast_server_process = subprocess.Popen([os.path.join(server_location,
                                                                                   'webrtc-streamer.exe'),
                                                                      '-H', '0.0.0.0:'+desktop_broadcast_server_port,
                                                                      'screen://3'], cwd=server_location, shell=False)
        except Exception as ex:
            print('Exception wile start desktop_broadcast_server:{}'.format(ex))

    def stop_desktop_broadcast_server(self):
        try:
            if self.desktop_broadcast_server_process:
                self.desktop_broadcast_server_process.terminate()
                self.desktop_broadcast_server_process.kill()
                time.sleep(1)  # 会造成界面失去响应
                # /t选项，关闭自己和由它启动的子进程
                # os.system('taskkill /t /f /pid {}'.format(self.desktop_broadcast_server_process.pid))
        except Exception as ex:
            print('Exception while Stopping desktop_broadcast_server:', ex)


class RefreshAliveThread(QThread):
    signals = pyqtSignal(list)

    def __init__(self):
        super(RefreshAliveThread, self).__init__()

    def run(self):
        living_hosts_list = get_living_hosts_by_arp_ping()
        self.signals.emit(living_hosts_list)


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
            serverPort = get_config('remote_control', 'server_port', to_int=True)  # default 12000
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
                print('[{}]:From Server:{}'.format(self.target_ip, receivedMessage.decode()))

            clientSocket.close()

            if self.target_cmd != 'CAPTURE_SCREEN':
                result_str = receivedMessage.decode()
            print('[{}]:result_str={}'.format(self.target_ip,result_str))
        except Exception as ex:
            print('[{}]: 发生异常，提示信息：{}'.format(self.target_ip, ex))
            result_str = '{}'.format(ex)

        print('[{}]:WordThread1 completed, {:.1f} seconds elapsed'.format(self.target_ip, time.time() - start_time))
        try:
            self.signals.emit(result_str)
        except Exception as ex:
            print('[{}]: WorkThread1 emiting ex:{}'.format(self.target_ip, ex))


def create_computer_widget(ip='x.x.x.x', name='unknown', border_style=0):
    my_widget = QLabel()
    my_widget.setTextFormat(Qt.RichText)
    my_widget.setStyleSheet('padding: 12px;')  # 设置控件的外边距，美观

    icon_show_ip = get_config('computer_browser_ui', 'icon_show_ip', to_bool=True)
    icon_show_name = get_config('computer_browser_ui', 'icon_show_name', to_bool=True)
    icon_size = get_config('computer_browser_ui', 'icon_size', to_int=True)
    icon_font_size = get_config('computer_browser_ui', 'icon_font_size', to_int=True)
    html_text = '<div style="text-align:center;">'
    if icon_show_ip:
        html_text += '<p><font size={}>{}</h4></font></p>'.format(icon_font_size, ip)
    html_text += '<p><img width={} src="../images/user.jpg"></p>'.format(icon_size)
    if icon_show_name:
        html_text += '<p><font size={}>{}</font></p>'.format(icon_font_size, name)
    html_text += '</div>'

    my_widget.setText(html_text)
    my_widget.setScaledContents(True)
    my_widget.setToolTip('<p style="background:#ffe;font-weight:bold;">IP: '+ip
                         + '</p><p style="background:#efe;font-weight:bold;">Name: ' + name + '</p>')
    # my_widget.setText('help me')
    # my_widget.setPixmap(QPixmap('../images/computer1.jpg').scaled(64, 64))
    if border_style == 0:
        my_widget.setStyleSheet('padding: 12px;')  # 设置控件的外边距，美观
    elif border_style == 1:
        my_widget.setStyleSheet('padding: 12px; border: 2px dashed red;')  # 红框，表示网关
    elif border_style == 2:
        my_widget.setStyleSheet('padding: 12px; border: 2px dashed blue;')  # 蓝框，表示本机
    return my_widget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
