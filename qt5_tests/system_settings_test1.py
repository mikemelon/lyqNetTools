import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication
from qt5.system_settings import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        self.res_ratio_combo.addItems(['16:9', '16:10', '4:3'])
        self.res_ratio_combo.setCurrentIndex(0)
        self.res_ratio_combo.currentIndexChanged.connect(self.res_ratio_combo_index_changed)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())


