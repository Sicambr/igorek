import sys
import os
import to_s191

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QAction
from PyQt5 import QtWidgets, uic
from UnIgor import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        current_path = to_s191.load_path()
        self.show_path.setText(current_path)
        
        self.start_button.pressed.connect(
            lambda: self.start_button_pressed())

        self.read_log_file.triggered.connect(lambda: self.read_log_file_pressed())

    def read_log_file_pressed(self):
        mistakes_path = os.path.join(os.path.abspath(''), 'error.log')
        if os.path.exists(mistakes_path):
            os.startfile(mistakes_path)

    def start_button_pressed(self):
        current_path=self.show_path.text()
        self.status_label.setText(
            'В работе по созданию новых .NC файлов. Ждем...')
        mistakes = to_s191.main(current_path)
        to_s191.save_path(current_path)
        if mistakes:
            self.status_label.setText(
                'Что-то пошло не так... Проверьте ошибки в файле error.log программы.')    
        else:
            self.status_label.setText(
                'Файлы для Bumotec и Macodell успешно собраны.')
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
