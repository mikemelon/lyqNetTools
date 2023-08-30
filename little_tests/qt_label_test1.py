import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont

# 定义窗口函数window
def window():
    # 我事实上不太明白干嘛要这一句话，只是pyqt窗口的建立都必须调用QApplication方法
    app = QtWidgets.QApplication(sys.argv)
    # 新建一个窗口，名字叫做w
    w = QtWidgets.QWidget()
    # 定义w的大小
    w.setGeometry(100, 100, 300, 200)
    # 给w一个Title
    w.setWindowTitle('lesson 2')
    # 在窗口w中，新建一个lable，名字叫做l1
    l1 = QtWidgets.QLabel(w)
    # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
    # png = QtGui.QPixmap('/home/capture/Pictures/Selection_026.png')
    png = QtGui.QPixmap('../images/computer1.jpg')
    # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
    l1.setPixmap(png.scaled(64, 64))

    # 在窗口w中，新建另一个label，名字叫做l2
    l2 = QtWidgets.QLabel(w)
    # 用open方法打开一个文本文件，并且调用read命令，将其内容读入到file_text中
    # file = open('/home/capture/eric6_test/auto_k2_all/test1.log')
    # file_text = file.read()
    # 调用setText命令，在l2中显示刚才的内容
    # l2.setText(file_text)

    l2.setText('test测试')

    font = QFont()
    font.setPointSize(16)
    l2.setFont(font)

    # 调整l1和l2的位置
    l1.move(60, 60)
    l2.move(180, 280)
    # 显示整个窗口
    w.show()
    # 退出整个app
    app.exit(app.exec_())


# 调用window这个函数
window()