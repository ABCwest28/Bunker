import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit)
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


class BunkerClientStartWindow(QWidget):
    """
    Окно для ввода никнейма и ip-адреса для подключения к серверу
    """
    def __init__(self):
        super().__init__()

        self.h_layout_1 = QHBoxLayout()
        self.h_layout_2 = QHBoxLayout()
        self.v_layout_1 = QVBoxLayout()

        self.label_1 = QLabel("Никнейм:", self)
        self.label_2 = QLabel("Ip-адрес сервера:", self)
        self.line_edit_nik = QLineEdit(self)
        self.line_edit_ip = QLineEdit(self)

        self.initUi()
        self.show()

    def initUi(self):
        self.setWindowTitle('Bunker Client')
        self.initUi_line_edit_ip_validation()
        self.initUi_layouts()

    def initUi_line_edit_ip_validation(self):
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"                                           # Часть регулярного выржение
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")    # Само регулярное выражение
        ipValidator = QRegExpValidator(ipRegex, self)                                                   # Валидатор для QLineEdit
        self.line_edit_ip.setValidator(ipValidator)

    def initUi_layouts(self):
        self.h_layout_1.addWidget(self.label_1)
        self.h_layout_1.addWidget(self.line_edit_nik)

        self.h_layout_2.addWidget(self.label_2)
        self.h_layout_2.addWidget(self.line_edit_ip)

        self.v_layout_1.addLayout(self.h_layout_1)
        self.v_layout_1.addLayout(self.h_layout_2)
        self.setLayout(self.v_layout_1)


class BunkerClientMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window_1)
        self.setCentralWidget(self.button)

    def show_new_window_1(self):
        if self.w is None:
            self.w = BunkerClientStartWindow()
        self.w.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_window = BunkerClientStartWindow()
    sys.exit(app.exec_())
