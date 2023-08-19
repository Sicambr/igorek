import sys
import os
import to_s191

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5 import QtWidgets, uic
from UnIgor import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        current_path = to_s191.create_path()
        self.show_path.setText(current_path)
        self.start_button.pressed.connect(
            lambda: self.start_button_pressed(current_path))
        # buttn = QLabel()
        # buttn.setText

    def start_button_pressed(self, current_path):
        self.status_label.setText(
            'В работе по созданию новых .NC файлов. Ждем...')
        to_s191.main(current_path)
        self.status_label.setText(
            'Файлы для Bumotec и Macodell успешно собраны.')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
