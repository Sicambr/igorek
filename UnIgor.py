# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(922, 390)
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title_lable = QtWidgets.QLabel(self.centralwidget)
        self.title_lable.setGeometry(QtCore.QRect(310, 50, 271, 31))
        self.title_lable.setObjectName("title_lable")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 90, 901, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.show_path = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.show_path.setObjectName("show_path")
        self.horizontalLayout.addWidget(self.show_path)
        self.change_path = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.change_path.setObjectName("change_path")
        self.horizontalLayout.addWidget(self.change_path)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(10, 280, 121, 41))
        self.start_button.setObjectName("start_button")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(150, 280, 771, 41))
        self.status_label.setText("")
        self.status_label.setObjectName("status_label")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 0, 711, 51))
        self.label.setObjectName("label")
        self.replace_mac_feed = QtWidgets.QCheckBox(self.centralwidget)
        self.replace_mac_feed.setGeometry(QtCore.QRect(20, 240, 451, 31))
        self.replace_mac_feed.setObjectName("replace_mac_feed")
        self.gen_macodel = QtWidgets.QCheckBox(self.centralwidget)
        self.gen_macodel.setGeometry(QtCore.QRect(20, 200, 401, 31))
        self.gen_macodel.setObjectName("gen_macodel")
        self.gen_bumotec = QtWidgets.QCheckBox(self.centralwidget)
        self.gen_bumotec.setGeometry(QtCore.QRect(20, 160, 351, 31))
        self.gen_bumotec.setObjectName("gen_bumotec")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 922, 31))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.read_log_file = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.read_log_file.setFont(font)
        self.read_log_file.setObjectName("read_log_file")
        self.menu.addAction(self.read_log_file)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IGOREK_v1.32"))
        self.title_lable.setText(_translate(
            "MainWindow", "Папка где лежат *.NC файлы:"))
        self.change_path.setText(_translate("MainWindow", "Открыть"))
        self.start_button.setText(_translate("MainWindow", "Старт"))
        self.label.setText(_translate(
            "MainWindow", "Программа для сборки *.NC файлов. Постпроцессоры: S191_v8.2,  W508S_v7.1"))
        self.replace_mac_feed.setText(_translate(
            "MainWindow", "Замена подач F на F#10 для Macodell файлов"))
        self.gen_macodel.setText(_translate(
            "MainWindow", "Собрать файлы для Macodell"))
        self.gen_bumotec.setText(_translate(
            "MainWindow", "Собрать файлы для Bumotec"))
        self.menu.setTitle(_translate("MainWindow", "Управление"))
        self.action.setText(_translate("MainWindow", "открыть"))
        self.read_log_file.setText(_translate(
            "MainWindow", "Посмотреть error.log"))
