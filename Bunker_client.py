import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QTextBrowser, QGridLayout, QTabWidget)
from PyQt5.QtCore import QRegExp, QEvent, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QFont, QFontDatabase
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
import font_resources_rc


class BunkerClientStartWindow(QMainWindow):
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

        self.isFirst = True
        """True - первый игрок, может запустить сессию"""

        self.main_window = self.BunkerClientMainWindow(self)
        self.sock = QTcpSocket(self)

        self.wrapper = QWidget(self)

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
        self.init_sock()
        self.show()

    def init_sock(self):
        self.sock.connected.connect(self.connected_slot)
        self.sock.readyRead.connect(self.read_data_slot)

    def connected_slot(self):
        """при подключении"""
        pass

    def read_data_slot(self):
        """при получении данных"""
        while self.sock.bytesAvailable():
            datagram = self.sock.read(self.sock.bytesAvailable())

        message = datagram.decode()
        self.text_browser.append('Server: {}'.format(message))

    def closeEvent(self, event):
        self.sock.close()
        event.accept()

    def initUi(self):
        self.setWindowTitle('Bunker Client')
        self.setMaximumSize(500, 160)
        self.setMinimumSize(380, 140)

        self.setCentralWidget(self.wrapper)

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

        self.statusBar().showMessage("Ready")

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
        self.wrapper.setLayout(self.v_layout_1)

    def set_font_Google(self):
        fontId = QFontDatabase.addApplicationFont(":/fonts/GoogleSans-Regular.ttf")

        if fontId == 0:
            fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
            self.font0 = QFont(fontName, 16)
            self.font1 = QFont(fontName, 10)
        else:
            self.font0 = QFont()
            self.font1 = QFont()

        # self.font0.setPointSize(16)
        self.setFont(self.font0)
        self.main_window.setFont(self.font0)
        self.statusBar().setFont(self.font1)

    def enable_disable_btn_con(self):
        if self.line_edit_nik.text() and self.line_edit_ip.hasAcceptableInput():
            self.btn_con.setEnabled(True)
        else:
            self.btn_con.setEnabled(False)

    def auto_fill_ip(self):
        self.line_edit_ip.setText("192.168.0.1")

    def connect_button_event(self):
        """
        попытка соединения с сервером, проверка уникальности имени
        если не удалось подключится - вывод в поле ip
        если ник уже занят - вывод в поле никнейма
        если все норм, то вывод на окно ожидания

        + НУЖНО IS_FIRST ЗАПРОС
        """

        try:
            ip = str(self.line_edit_ip.text())
            self.sock.connectToHost(ip, 6666)
            self.statusBar().showMessage(f"Connected to: {ip}")
        except QTcpSocket.SocketError as error:
            self.statusBar().showMessage(f"Connection error: {error}")

        self.btn_con.hide()
        self.btn_discon.show()
        self.text_browser.show()

        self.setMinimumSize(380, 400)
        self.setMaximumSize(500, 450)

        if self.isFirst:
            self.btn_start.show()

        self.line_edit_nik.setEnabled(False)
        self.line_edit_ip.setEnabled(False)

        self.get_data_text_browser()

    def get_data_text_browser(self):
        """
        Получение информации о всех подключенных игроках, при добавлении сервер должен рассылать всем игрокам инфу
        """
        pass

    def disconnect_button_event(self):
        self.sock.close()

        self.setMaximumSize(500, 160)
        self.setMinimumSize(380, 140)
        self.resize(410, 132)

        self.text_browser.hide()
        self.btn_con.show()
        self.btn_discon.hide()
        self.btn_start.hide()

        self.line_edit_nik.setEnabled(True)
        self.line_edit_ip.setEnabled(True)

        self.statusBar().showMessage("Ready")

    def start_button_event(self):
        """отправка сигнала на серевер по запуску игры"""
        self.main_window.show()
        self.main_window.label_nik.setText(self.line_edit_nik.text())
        self.hide()

    class BunkerClientMainWindow(QMainWindow):
        def __init__(self, parent):
            super().__init__()
            self.w = parent

            self.wrapper = QWidget()
            self.grid_wrapper = QGridLayout()

            self.label_nik = QLabel()
            print(str())

            self.tab = QTabWidget()
            self.widget_player = QWidget()
            self.widget_aboutAll = QWidget()
            self.widget_voting = QWidget()
            self.widget_history = QWidget()

            self.init_widget_player()
            self.init_widget_aboutAll()
            self.init_widget_voting()
            self.init_widget_history()

            self.btn_leave = QPushButton("Покинуть игру")

            self.initUi()
            self.init_grid()

        def initUi(self):
            self.setCentralWidget(self.wrapper)
            self.btn_leave.clicked.connect(self.btn_leave_event)

        def init_grid(self):
            self.grid_wrapper.addWidget(self.label_nik, 0, 0)
            self.grid_wrapper.addWidget(self.tab, 1, 0)
            self.grid_wrapper.addWidget(self.btn_leave, 2, 0)

            self.wrapper.setLayout(self.grid_wrapper)

        def init_widget_player(self):
            self.grid_player = QGridLayout()

            self.label_profession = QLabel("Профессия")
            self.label_bio = QLabel("Пол и возраст")
            self.label_health = QLabel("Здоровье")
            self.label_phobia = QLabel("Фобия")
            self.label_hobby = QLabel("Хобби")
            self.label_baggage = QLabel("Багаж")
            self.label_fact1 = QLabel("Факт1")
            self.label_fact2 = QLabel("Факт2")

            self.line_profession = QLineEdit()
            self.line_bio = QLineEdit()
            self.line_health = QLineEdit()
            self.line_phobia = QLineEdit()
            self.line_hobby = QLineEdit()
            self.line_baggage = QLineEdit()
            self.line_fact1 = QLineEdit()
            self.line_fact2 = QLineEdit()

            self.grid_player.addWidget(self.label_profession, 0, 0)
            self.grid_player.addWidget(self.label_bio, 1, 0)
            self.grid_player.addWidget(self.label_health, 2, 0)
            self.grid_player.addWidget(self.label_phobia, 3, 0)
            self.grid_player.addWidget(self.label_hobby, 4, 0)
            self.grid_player.addWidget(self.label_baggage, 5, 0)
            self.grid_player.addWidget(self.label_fact1, 6, 0)
            self.grid_player.addWidget(self.label_fact2, 7, 0)
            self.grid_player.addWidget(self.line_profession, 0, 1)
            self.grid_player.addWidget(self.line_bio, 1, 1)
            self.grid_player.addWidget(self.line_health, 2, 1)
            self.grid_player.addWidget(self.line_phobia, 3, 1)
            self.grid_player.addWidget(self.line_hobby, 4, 1)
            self.grid_player.addWidget(self.line_baggage, 5, 1)
            self.grid_player.addWidget(self.line_fact1, 6, 1)
            self.grid_player.addWidget(self.line_fact2, 7, 1)

            self.widget_player.setLayout(self.grid_player)
            self.tab.addTab(self.widget_player, "О себе")

        def init_widget_aboutAll(self):
            pass

        def init_widget_voting(self):
            pass

        def init_widget_history(self):
            pass

        def btn_leave_event(self):
            if self.w is None:
                self.w = BunkerClientStartWindow()
            self.w.show()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_window = BunkerClientStartWindow()
    sys.exit(app.exec_())
