import sys
import wmi
import pythoncom
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication
from qt5.wmi_process_list import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        self.model = QStandardItemModel(0, 4)
        self.model.setHorizontalHeaderLabels(['name', 'pid', 'thread_count', 'creation_date', 'exepath'])

        self.tableView.setModel(self.model)
        self.tableView.resizeColumnToContents(0)

        pc = wmi.WMI()
        os_info = pc.Win32_OperatingSystem()[0]
        processor = pc.Win32_Processor()[0]
        gpus = pc.Win32_VideoController()

        show_info_str = '*' * 40 + '\n'
        show_info_str = show_info_str + '操作系统：{}'.format(os_info.Caption) + '\n'
        show_info_str = show_info_str + 'CPU：{}，\n\t 内核：{}，逻辑处理器：{}，L2 Cache：{}M，L3 Cache：{}M\n' \
            .format(processor.Name, processor.NumberOfCores, processor.NumberOfLogicalProcessors,
                    float(processor.L2CacheSize) / 1024, float(processor.L3CacheSize) / 1024)
        show_info_str = show_info_str + '显卡：\n'
        for gpu in gpus:
            show_info_str = show_info_str + gpu.Name + '\n'
        show_info_str = '*' * 40 + '\n'
        self.textBrowser.setText(show_info_str)

        self.work_thread = WorkThread()
        self.work_thread.start()
        self.work_thread.signals.connect(self.update_model)

        self.work_thread2 = WorkThread2()
        self.work_thread2.start()
        self.work_thread2.signals.connect(self.update_model2)

    def update_model(self, process_list):
        # 到如下地址查Win32_Process的属性
        # https://learn.microsoft.com/zh-cn/windows/win32/cimwin32prov/win32-process?source=recommendations
        for process in process_list:
            item1 = QStandardItem(process.Name)
            item2 = QStandardItem(str(process.ProcessID))
            item3 = QStandardItem(str(process.ThreadCount))
            str_creation_date = process.CreationDate
            item4 = QStandardItem(
                str_creation_date[:4] + '-' + str_creation_date[4:6] + '-' + str_creation_date[6:8] + ' '
                + str_creation_date[8:10] + ':' + str_creation_date[10:12] + ':'
                + str_creation_date[12:14])
            item5 = QStandardItem(process.ExecutablePath)
            self.model.appendRow([item1, item2, item3, item4, item5])

            self.tableView.setColumnWidth(0, 200)
            self.tableView.setColumnWidth(1, 120)
            self.tableView.setColumnWidth(2, 140)
            self.tableView.setColumnWidth(3, 300)
            self.tableView.setColumnWidth(4, 600)

    def update_model2(self, info_str):
        self.textBrowser.setText(info_str)


class WorkThread(QThread):
    signals = pyqtSignal(list)

    def __init__(self):
        super(WorkThread, self).__init__()

    def run(self):
        start_time = time.time()
        pythoncom.CoInitialize()
        # pc = wmi.WMI(find_classes=False)
        pc = wmi.WMI(computer='192.168.68.223', user='ec1', password='tplink',
                     find_classes=False)  # Win10专业版物理机，连接成功！
        # pc = wmi.WMI(computer='192.168.48.130', user='lynulyq', password='tplink', find_classes=False)  # VMWare里的Win7企业版，连接成功！
        # pc = wmi.WMI(computer='192.168.48.131', user='Administrator', password='12345678', find_classes=False) # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）
        process_list = pc.Win32_Process()
        print('wmi load process_list used {:.1f} seconds'.format(time.time() - start_time))
        pythoncom.CoUninitialize()
        self.signals.emit(list(process_list))


class WorkThread2(QThread):
    signals = pyqtSignal(str)

    def __init__(self):
        super(WorkThread2, self).__init__()

    def run(self):
        start_time = time.time()
        pythoncom.CoInitialize()
        pc = wmi.WMI(find_classes=False)
        # pc = wmi.WMI(computer='192.168.68.223', user='ec1', password='tplink',
        #                      find_classes=False)  # Win10专业版物理机，连接成功！
        # pc = wmi.WMI(computer='192.168.48.130', user='lynulyq', password='12345678', find_classes=False)  # VMWare里的Win7企业版，连接成功！
        # pc = wmi.WMI(computer='192.168.48.131', user='Administrator', password='12345678', find_classes=False) # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）

        os_info = pc.Win32_OperatingSystem()[0]
        processor = pc.Win32_Processor()[0]
        gpus = pc.Win32_VideoController()

        show_info_str = '*' * 60 + '\n'
        show_info_str = show_info_str + '操作系统：' + os_info.Caption + '\n'
        show_info_str = show_info_str + 'CPU：' + processor.Name + '，\n   内核：' + str(processor.NumberOfCores) + '，'
        show_info_str = show_info_str + '逻辑处理器：' + str(processor.NumberOfLogicalProcessors) + '，L2 Cache：'
        show_info_str = show_info_str + str(float(processor.L2CacheSize) / 1024) + 'M，L3 Cache：'
        show_info_str = show_info_str + str(float(processor.L3CacheSize) / 1024) + 'M\n'
        show_info_str = show_info_str + '显卡：\n'
        for gpu in gpus:
            show_info_str = show_info_str + '   ' + gpu.Name + '\n'
        show_info_str = show_info_str + '*' * 60 + '\n'

        print('wmi load system info used {:.1f} seconds'.format(time.time() - start_time))
        pythoncom.CoUninitialize()
        print('show_info_str = ', show_info_str)
        self.signals.emit(show_info_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())

# 'children', 'cmdline', 'connections', 'cpu_affinity', 'cpu_percent', 'cpu_times',
# 'create_time', 'cwd', 'environ','exe', 'io_counters', 'ionice','is_running', 'kill',
# 'memory_full_info', 'memory_info','memory_info_ex','memory_maps', 'memory_percent',
# 'name', 'nice', 'num_ctx_switches','num_handles', 'num_threads','oneshot', 'open_files',
# 'parent', 'parents', 'pid', 'ppid', 'resume', 'send_signal', 'status', 'suspend',
# 'terminate', 'threads', 'username', 'wait'
