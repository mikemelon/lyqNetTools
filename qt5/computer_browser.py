# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'computer_browser.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 629)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(40, 520, 71, 16))
        self.label_1.setObjectName("label_1")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 751, 491))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 500, 631, 81))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_refresh_alive = QtWidgets.QAction(MainWindow)
        self.action_refresh_alive.setObjectName("action_refresh_alive")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.menu.addAction(self.action_refresh_alive)
        self.menu.addSeparator()
        self.menu.addAction(self.action_quit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "主机列表"))
        self.label_1.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "上图中，图标加红框表示网关，图标加蓝框表示本机，\n"
"鼠标左键单击上图中的图标查看IP地址和基本信息，\n"
"鼠标右键单击此图标进行远程控制。"))
        self.menu.setTitle(_translate("MainWindow", "局域网工具"))
        self.action_refresh_alive.setText(_translate("MainWindow", "刷新局域网存活主机...(&S)"))
        self.action_refresh_alive.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_quit.setText(_translate("MainWindow", "退出(&Q)"))