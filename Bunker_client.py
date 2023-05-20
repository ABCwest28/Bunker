import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit)
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QFont, QFontDatabase
import font_resources_rc


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
        self.btn_con = QPushButton("Connect", self)

        self.initUi()
        self.show()

    def initUi(self):
        self.setWindowTitle('Bunker Client')
        self.setMaximumSize(500, 150)
        self.setMinimumSize(380, 130)

        self.set_font_Google()

        self.line_edit_ip.setPlaceholderText("192.168.0.1")
        self.initUi_line_edit_ip_validation()

        self.btn_con.setEnabled(False)
        self.line_edit_nik.textChanged.connect(self.enable_disable_btn_con)
        self.line_edit_ip.textChanged.connect(self.enable_disable_btn_con)

        self.initUi_layouts()

    def initUi_line_edit_ip_validation(self):
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"                                           # Часть регулярного выржение
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")    # Само регулярное выражение
        ipValidator = QRegExpValidator(ipRegex, self)                                                   # Валидатор для QLineEdit
        self.line_edit_ip.setValidator(ipValidator)
        self.line_edit_ip.validator()

    def initUi_layouts(self):
        self.h_layout_1.addWidget(self.label_1)
        self.h_layout_1.addWidget(self.line_edit_nik)

        self.h_layout_2.addWidget(self.label_2)
        self.h_layout_2.addWidget(self.line_edit_ip)

        self.v_layout_1.addLayout(self.h_layout_1)
        self.v_layout_1.addLayout(self.h_layout_2)
        self.v_layout_1.addWidget(self.btn_con)
        self.setLayout(self.v_layout_1)

    def set_font_Google(self):
        fontId = QFontDatabase.addApplicationFont(":/fonts/GoogleSans-Regular.ttf")

        if fontId == 0:
            fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
            self.font0 = QFont(fontName, 30)
        else:
            self.font0 = QFont()

        self.font0.setPointSize(16)

        self.setFont(self.font0)

    def enable_disable_btn_con(self):
        if self.line_edit_nik.text() and self.line_edit_ip.text():
            self.btn_con.setEnabled(True)
        else:
            self.btn_con.setEnabled(False)


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
