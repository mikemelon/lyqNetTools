import sys
from qt5.computer_browser import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox, QMenu, QAction
from net_utils.scapy_utils import get_living_hosts_by_arp_ping, get_gateway_ip, get_local_ip
from mytools_using_qt5.remote_control_window import RemoteControlWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    COLUMN_CNT = 8

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可调整大小
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置右键菜单策略

        # print('width={}, height={}'.format(self.label_1.width(), self.label_1.height()))
        self.label_1.setScaledContents(True) # 让图片自适应控件设置的大小
        self.label_1.setPixmap(QPixmap('../images/computer1.jpg'))
        self.label_1.setGeometry(self.label_1.x(), self.label_1.y(), 48, 48)

        row_cnt, column_cnt = 5, 8
        self.tableWidget.setRowCount(row_cnt)
        self.tableWidget.setColumnCount(column_cnt)

        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏行题
        self.tableWidget.horizontalHeader().setVisible(False)  # 隐藏列标题

        for m in range(row_cnt):
            for n in range(column_cnt):
                my_widget = QLabel()
                my_widget.setScaledContents(True)
                my_widget.setPixmap(QPixmap('../images/computer1.jpg').scaled(64, 64))
                my_widget.setStyleSheet('margin: 12px;') # 设置控件的外边距，美观
                self.tableWidget.setCellWidget(m, n, my_widget)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        self.tableWidget.cellClicked.connect(self.cell_clicked)
        # self.tableWidget.cellDoubleClicked.connect(self.cell_double_clicked)
        self.tableWidget.customContextMenuRequested.connect(self.show_custom_contex_menu)

        self.action_quit.triggered.connect(self.menu_action_quit)
        self.action_refresh_alive.triggered.connect(self.menu_action_refresh_alive)

        self.living_host_dict = {}  # ip:(所在行，所在列)
        self.living_host_position_dict = {}  # (所在行，所在列): ip
        self.refresh_alive_thread = None
        self.remote_control_window = None

    def cell_clicked(self, row, column):
        if (row, column) not in self.living_host_position_dict:
            return
        selected_host_ip = self.living_host_position_dict[(row, column)]

        print('所点击的主机信息row={}, column={}, ip={}'.format(row, column, selected_host_ip))
        display_str = '点击主机信息：\nIP地址：{}'.format(selected_host_ip)
        if get_gateway_ip() == selected_host_ip:
            display_str += '\n'+'所选为网关'
        if get_local_ip() == selected_host_ip:
            display_str += '\n'+'所选为本机'

        QMessageBox.about(self, '所点击的主机信息', display_str)

    def cell_double_clicked(self, row, column):  # 双击不起作用？（触发单击）
        print('double clicked!!!!!!')

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
        living_host_list.append('192.168.48.130')
        num_of_hosts = len(living_host_list)
        row_num = int(num_of_hosts / MyWindow.COLUMN_CNT + 1)
        column_num_remamins = int(num_of_hosts % MyWindow.COLUMN_CNT)

        self.tableWidget.setRowCount(row_num)
        self.tableWidget.setColumnCount(MyWindow.COLUMN_CNT)
        self.tableWidget.clear()

        host_idx = 0
        # living_host_dict = {}  # ip:(所在行，所在列)
        # living_host_position_dict = {}  # (所在行，所在列): ip
        for m in range(row_num):
            if m == row_num-1:
                current_column_cnt = column_num_remamins
            else:
                current_column_cnt = MyWindow.COLUMN_CNT
            for n in range(current_column_cnt):
                self.living_host_dict[living_host_list[host_idx]] = (m, n)
                self.living_host_position_dict[(m, n)] = living_host_list[host_idx]
                widget = create_computer_widget()
                if get_gateway_ip()==living_host_list[host_idx]:
                    widget = create_computer_widget(border_style=1)
                elif get_local_ip()==living_host_list[host_idx]:
                    widget = create_computer_widget(border_style=2)
                self.tableWidget.setCellWidget(m, n, widget)
                host_idx += 1


class RefreshAliveThread(QThread):
    signals = pyqtSignal(list)

    def __init__(self):
        super(RefreshAliveThread, self).__init__()

    def run(self):
        living_hosts_list = get_living_hosts_by_arp_ping()
        self.signals.emit(living_hosts_list)


def create_computer_widget(border_style=0):
    my_widget = QLabel()
    my_widget.setScaledContents(True)
    my_widget.setPixmap(QPixmap('../images/computer1.jpg').scaled(64, 64))
    if border_style == 0:
        my_widget.setStyleSheet('margin: 12px;')  # 设置控件的外边距，美观
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