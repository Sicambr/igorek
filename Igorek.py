import sys
import os
import to_s191

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QAction, QFileDialog
from PyQt5 import QtWidgets, uic, QtGui
from UnIgor import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        ico = QtGui.QIcon('cnc.ico')
        self.setWindowIcon(ico)
        load_switchers, current_path = to_s191.load_path()
        self.show_path.setText(current_path)
        self.gen_bumotec.setCheckState(int(load_switchers[0]))
        self.gen_macodel.setCheckState(int(load_switchers[1]))
        self.replace_mac_feed.setCheckState(int(load_switchers[2]))

        self.start_button.pressed.connect(
            lambda: self.start_button_pressed())

        self.read_log_file.triggered.connect(
            lambda: self.read_log_file_pressed())

        self.new_explorer = QFileDialog
        self.change_path.pressed.connect(lambda: self.change_path_pressed())

    def change_path_pressed(self):
        current_path = self.show_path.text()
        dir_name = self.new_explorer.getExistingDirectory(
            directory=current_path)
        if not dir_name:
            self.show_path.setText(current_path)
        else:
            self.show_path.setText(dir_name)

    def read_log_file_pressed(self):
        mistakes_path = os.path.join(os.path.abspath(''), 'error.log')
        if os.path.exists(mistakes_path):
            os.startfile(mistakes_path)

    def start_button_pressed(self):
        current_path = self.show_path.text()
        self.status_label.setText(
            'В работе по созданию новых .NC файлов. Ждем...')
        load_switchers = list()
        load_switchers.append(self.gen_bumotec.checkState())
        load_switchers.append(self.gen_macodel.checkState())
        load_switchers.append(self.replace_mac_feed.checkState())
        mistakes = to_s191.main(current_path, load_switchers)
        to_s191.save_config(load_switchers, current_path)
        if mistakes:
            self.status_label.setText(
                'Что-то пошло не так... Проверьте ошибки в файле error.log программы.')
        else:
            if load_switchers[0] and load_switchers[1]:
                self.status_label.setText(
                    'Файлы для Bumotec и Macodell успешно собраны.')
            elif load_switchers[0] and not load_switchers[1]:
                self.status_label.setText(
                    'Файлы для Bumotec успешно собраны.')
            elif load_switchers[1] and not load_switchers[0]:
                self.status_label.setText(
                    'Файлы для Macodell успешно собраны.')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
