import sys
import threading
import time
from pythonping import ping
from multiprocessing import Pool
from dns_finder import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QThread, pyqtSignal


def read_dns():
    with open('dns.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    ip2comment, comment2ip = {}, {}
    for line in lines:
        tmp = line.split(',')
        ip2comment[tmp[0]] = tmp[1].strip()
        comment2ip[tmp[1].strip()] = tmp[0]
    return ip2comment, comment2ip


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可调整大小

        self.model = QStandardItemModel(0, 3)
        self.model.setHorizontalHeaderLabels(['DNS服务器名', 'IPv4地址', '往返时间'])

        ip2comment, comment2ip = read_dns()
        for name in comment2ip.keys():
            item1 = QStandardItem(name)
            item2 = QStandardItem(comment2ip[name])
            item3 = QStandardItem('未知')
            self.model.appendRow([item1, item2, item3])
        self.tableView.setModel(self.model)

        self.tableView.resizeColumnToContents(0)
        self.pushButton.clicked.connect(self.re_calc_dns)
        self.work_thread = None

    def re_calc_dns(self):
        # print('re_calc_dns, thread = ',QThread.currentThread())
        self.work_thread = WorkThread()
        self.work_thread.start()
        self.work_thread.signals.connect(self.update_model)
        self.pushButton.setText('DNS测速中...')

    def update_model(self, reachable_ip_list):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['DNS服务器名', 'IPv4地址', '往返时间'])
        print(('{:30}{:20}{}\n' + '-' * 70).format('名称', 'IPv4地址', '往返时间'))
        # print(reachable_ip_list)
        ip2comment, comment2ip = read_dns()
        for item in sorted(reachable_ip_list, key=lambda x: x[1]):
            print('{:30}{:20}{}'.format(ip2comment[item[0]], item[0], str(item[1]) + ' ms'))
            item1 = QStandardItem(ip2comment[item[0]])
            item2 = QStandardItem(item[0])
            item3 = QStandardItem(str(item[1]) + ' ms')
            self.model.appendRow([item1, item2, item3])

        self.pushButton.setText('DNS重新测速')


class WorkThread(QThread):
    signals = pyqtSignal(list)

    def __init__(self):
        super(WorkThread, self).__init__()

    def run(self):
        # print('run, thread = ', QThread.currentThread())
        # print('run, thread 2 = ', self.thread())
        # print('run, thread 3 = ', threading.currentThread())
        pool = Pool(255)
        result_list = []
        ip2comment, comment2ip = read_dns()
        for ip in ip2comment.keys():
            result = pool.apply_async(func=my_ping, args=(ip,))
            result_list.append(result)

        pool.close()
        pool.join()
        # print('all process over!!!!')
        # print(result_list)

        reachable_ip_list = []
        for r in result_list:
            if r.get()[1]:
                reachable_ip_list.append((r.get()[0], r.get()[2]))

        self.signals.emit(reachable_ip_list)
        # time.sleep(3)
        # self.signals.emit([('8.8.8.8', '1.0'),])


def my_ping(ip):
    # print('pinging '+ip+' start')
    resp = ping(ip)
    # print('-->',resp)
    if 'Reply' in str(resp):
        return ip, True, resp.rtt_avg_ms
    else:
        return ip, False, 999.9


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
