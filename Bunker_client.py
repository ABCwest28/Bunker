import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QTextBrowser)
from PyQt5.QtCore import QRegExp, QEvent, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QFont, QFontDatabase, QMouseEvent
import font_resources_rc


class BunkerClientStartWindow(QWidget):
    """
    Окно для ввода никнейма и ip-адреса для подключения к серверу
    """

    class LineEditWithDoubleClick(QLineEdit):
        doubleClicked = pyqtSignal()

        def event(self, event):
            if event.type() == QEvent.Type.MouseButtonDblClick:
                self.doubleClicked.emit()
            return super().event(event)

    def __init__(self):
        super().__init__()

        self.h_layout_1 = QHBoxLayout()
        self.h_layout_2 = QHBoxLayout()
        self.v_layout_1 = QVBoxLayout()

        self.label_1 = QLabel("Никнейм:", self)
        self.label_2 = QLabel("Ip-адрес сервера:", self)
        self.line_edit_nik = QLineEdit(self)
        self.line_edit_ip = self.LineEditWithDoubleClick(self)

        self.text_browser = QTextBrowser(self)

        self.btn_con = QPushButton("Connect", self)
        self.btn_discon = QPushButton("Disconnect", self)
        self.btn_start = QPushButton("Start", self)

        self.initUi()
        self.show()

        print(self.size())

    def initUi(self):
        self.setWindowTitle('Bunker Client')
        self.setMaximumSize(500, 150)
        self.setMinimumSize(380, 130)

        self.set_font_Google()

        self.line_edit_ip.setPlaceholderText("192.168.0.1")
        self.initUi_line_edit_ip_validation()

        self.btn_con.setEnabled(False)
        self.btn_con.clicked.connect(self.connect_button_event)

        self.text_browser.hide()
        self.text_browser.setMinimumHeight(200)
        self.text_browser.setReadOnly(True)

        self.btn_discon.hide()
        self.btn_discon.clicked.connect(self.disconnect_button_event)

        self.btn_start.hide()
        self.btn_start.clicked.connect(self.start_button_event)

        self.line_edit_nik.textChanged.connect(self.enable_disable_btn_con)
        self.line_edit_ip.textChanged.connect(self.enable_disable_btn_con)
        self.line_edit_ip.doubleClicked.connect(self.auto_fill_ip)

        self.initUi_layouts()

    def initUi_line_edit_ip_validation(self):
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"                                               # Часть регулярного выржение
        self.ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")   # Само регулярное выражение
        self.ipValidator = QRegExpValidator(self.ipRegex, self)                                             # Валидатор для QLineEdit
        self.line_edit_ip.setValidator(self.ipValidator)
        self.line_edit_ip.validator()

    def initUi_layouts(self):
        self.h_layout_1.addWidget(self.label_1)
        self.h_layout_1.addWidget(self.line_edit_nik)

        self.h_layout_2.addWidget(self.label_2)
        self.h_layout_2.addWidget(self.line_edit_ip)

        self.v_layout_1.addLayout(self.h_layout_1)
        self.v_layout_1.addLayout(self.h_layout_2)
        self.v_layout_1.addWidget(self.text_browser)
        self.v_layout_1.addWidget(self.btn_con)
        self.v_layout_1.addWidget(self.btn_discon)
        self.v_layout_1.addWidget(self.btn_start)
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
        if self.line_edit_nik.text() and self.line_edit_ip.hasAcceptableInput():
            self.btn_con.setEnabled(True)
        else:
            self.btn_con.setEnabled(False)

    def auto_fill_ip(self):
        self.line_edit_ip.setText("192.168.0.1")

    # def mouseDoubleClickEvent(self, event):
    #     if event.pos() == self.line_edit_ip.pos():
    #         self.line_edit_ip.setText("192.168.0.1")
    def connect_button_event(self):
        """
        попытка соединения с сервером, проверка уникальности имени
        если не удалось подключится - вывод в поле ip
        если ник уже занят - вывод в поле никнейма
        если все норм, то вывод на окно ожидания
        """
        self.btn_con.hide()
        self.btn_discon.show()
        self.text_browser.show()

        self.setMinimumSize(380, 380)
        self.setMaximumSize(500, 450)

        self.btn_start.show() #нужно будет сделать ф-ию только 1ый подключившийся может запустить

        self.line_edit_nik.setEnabled(False)
        self.line_edit_ip.setEnabled(False)

        self.get_data_text_browser()

    def get_data_text_browser(self):
        """
        Получение информации о всех подключенных игроках, при добавлении сервер должен рассылать всем игрокам инфу
        """
        pass

    def disconnect_button_event(self):
        """нужно добавить дисконнект с сервером"""
        self.setMaximumSize(500, 150)
        self.setMinimumSize(380, 130)
        self.resize(410, 132)

        self.text_browser.hide()
        self.btn_con.show()
        self.btn_discon.hide()
        self.btn_start.hide()

        self.line_edit_nik.setEnabled(True)
        self.line_edit_ip.setEnabled(True)

    def start_button_event(self):
        pass


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
