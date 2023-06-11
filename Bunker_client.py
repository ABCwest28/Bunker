import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QTextBrowser, QGridLayout, QTabWidget, QToolTip)
from PyQt5.QtCore import QRegExp, QEvent, pyqtSignal, QSize
from PyQt5.QtGui import QRegExpValidator, QFont, QFontDatabase, QIcon
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket, QHostAddress, QNetworkProxy
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

        self.isFirst = False
        """True - первый игрок, может запустить сессию"""

        self.main_window = self.BunkerClientMainWindow(self)

        self.sock = QTcpSocket()
        self.proxy = QNetworkProxy()
        self.proxy.setType(QNetworkProxy.NoProxy)
        self.sock.setProxy(self.proxy)
        self.sock.readyRead.connect(self.read_data_slot)
        self.sock.connected.connect(self.handle_connected)
        self.sock.errorOccurred.connect(self.handle_error)
        self.sock.disconnected.connect(self.disconnected_slot)

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

        self.init_ui()
        self.show()

    def closeEvent(self, event):
        self.sock.close()
        event.accept()

    def init_ui(self):
        self.setWindowTitle('Bunker Client')
        self.setMaximumSize(500, 160)
        self.setMinimumSize(380, 140)

        self.setCentralWidget(self.wrapper)

        self.set_font_google()

        self.line_edit_ip.setPlaceholderText("192.168.0.1")
        self.set_line_edit_ip_validation()

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

        self.statusBar().showMessage("Started")

        self.init_layouts()

    def set_line_edit_ip_validation(self):
        ip_range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"                                               # Часть регулярного выржение
        ip_regex = QRegExp("^" + ip_range + "\\." + ip_range + "\\." + ip_range + "\\." + ip_range + "$")   # Само регулярное выражение
        ip_validator = QRegExpValidator(ip_regex, self)                                             # Валидатор для QLineEdit
        self.line_edit_ip.setValidator(ip_validator)
        self.line_edit_ip.validator()

    def init_layouts(self):
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

    def set_font_google(self):
        font_id = QFontDatabase.addApplicationFont(":/fonts/GoogleSans-Regular.ttf")

        if font_id == 0:
            font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font0 = QFont(font_name, 16)
            self.font1 = QFont(font_name, 10)
        else:
            self.font0 = QFont()
            self.font1 = QFont()

        # self.font0.setPointSize(16)
        QToolTip.setFont(self.font1)
        self.setFont(self.font0)
        self.main_window.setFont(self.font0)
        self.statusBar().setFont(self.font1)

    def enable_disable_btn_con(self):
        if self.line_edit_nik.text() and self.line_edit_ip.hasAcceptableInput():
            self.btn_con.setEnabled(True)
        else:
            self.btn_con.setEnabled(False)

    def auto_fill_ip(self):
        """Можно сохранять предыдущее подключение и вставлять его"""
        self.line_edit_ip.setText("192.168.0.1")

    def connect_button_event(self):
        ip = str(self.line_edit_ip.text())
        self.sock.connectToHost(ip, 40040)

    def handle_error(self):
        cur_error = self.sock.errorString()
        if cur_error != "The remote host closed the connection":
            self.statusBar().showMessage(f"Ошибка подключения: {cur_error}")

    def handle_connected(self):
        """При успешном подключении"""
        if self.sock.state() == QAbstractSocket.ConnectedState:
            self.sock.write(("00:" + self.line_edit_nik.text()).encode())
            self.sock.write("\n".encode())

            print("Успешно подключено к серверу")
            self.statusBar().showMessage("Connected")

            self.btn_con.hide()
            self.btn_discon.show()
            self.text_browser.show()

            self.setMinimumSize(380, 400)
            self.setMaximumSize(500, 450)

            self.sock.write("04:".encode())
            self.sock.write("\n".encode())

            self.line_edit_nik.setEnabled(False)
            self.line_edit_ip.setEnabled(False)
        else:
            print("Не удалось подключиться к серверу")
            self.statusBar().showMessage(f"Connection failed")

    def read_data_slot(self):
        """Обрабатывает получаемые сообщения"""
        message = self.sock.readAll().data().decode()
        commands = message.split("\n")[:-1]
        for command in commands:
            type_command = command[:3]
            des_command = command[3:]

            if type_command == "01:":
                self.statusBar().showMessage("Не хватило карт для вашего добавления")

            elif type_command == "02:":
                self.statusBar().showMessage("Достигнут лимит игроков")

            elif type_command == "03:":
                self.statusBar().showMessage("Никнейм игрока не уникален")

            elif type_command == "05:":
                if des_command == "1":
                    self.isFirst = True
                    self.btn_start.show()
                else:
                    self.isFirst = False
                    self.btn_start.hide()

            elif type_command == "06:":
                self.statusBar().showMessage("Игра уже начата")

            elif type_command == "07:":
                self.start_game_event(name=des_command, params=None)

            elif type_command == "08:":
                self.start_game_event(name=None, params=des_command.split(sep="\t"))

            elif type_command == "11:":
                self.text_browser.append("Игра уже начата")

            elif type_command == "12:":
                separated = des_command.split(sep="/")
                self.text_browser.append(f"Недостаточно игроков для старта: {separated[0]}/{separated[1]}")

            else:
                self.text_browser.append("UNKNOWN_COMMAND: " + type_command + des_command)

    def disconnected_slot(self):
        self.disconnect_button_event()

    def disconnect_button_event(self):
        """Событие
        НУЖНО отправить сигнал об отключении"""
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

    def start_button_event(self):
        """Отправка сигнала на сервер по запуску игры"""
        self.sock.write("10:".encode())
        self.sock.write("\n".encode())

    def start_game_event(self, name, params):
        self.main_window.show()
        if name is None:
            self.main_window.label_nik.setText(self.line_edit_nik.text())
            self.main_window.fill_characteristic(params=params)
        else:
            self.main_window.label_nik.setText(str(name))
        self.hide()

    class BunkerClientMainWindow(QMainWindow):
        """Основное окно игры"""
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            self.wrapper = QWidget()
            self.grid_wrapper = QGridLayout()

            self.label_nik = QLabel()

            self.tab = QTabWidget()
            self.widget_player = QWidget()
            self.widget_aboutAll = QWidget()
            self.widget_voting = QWidget()
            self.widget_history = QWidget()

            self.init_widget_player()
            self.init_widget_about_all()
            self.init_widget_voting()
            self.init_widget_history()

            self.btn_leave = QPushButton("Покинуть игру")

            self.init_ui()

        def init_ui(self):
            self.setMinimumSize(600, 500)

            self.setCentralWidget(self.wrapper)
            self.btn_leave.clicked.connect(self.btn_leave_event)

            self.init_grid()
            self.set_tooltips()

        def init_grid(self):
            self.grid_wrapper.addWidget(self.label_nik, 0, 0)
            self.grid_wrapper.addWidget(self.tab, 1, 0)
            self.grid_wrapper.addWidget(self.btn_leave, 2, 0)

            self.wrapper.setLayout(self.grid_wrapper)

        def init_widget_player(self):
            self.grid_player = QGridLayout()
            self.icon_reveal = QIcon("imgs/reveal.png")

            self.label_profession = QLabel("Профессия")
            self.label_bio =        QLabel("Био данные")
            self.label_health =     QLabel("Здоровье/стадия")
            self.label_phobia =     QLabel("Фобия/стадия")
            self.label_hobby =      QLabel("Хобби")
            self.label_baggage =    QLabel("Багаж")
            self.label_fact1 =      QLabel("Факт №1")
            self.label_fact2 =      QLabel("Факт №2")

            self.line_profession =  QLineEdit()
            self.line_bio_sex =     QLineEdit()
            self.line_bio_age =     QLineEdit()
            self.line_bio_pro =     QLineEdit()
            self.line_bio_hob =     QLineEdit()
            self.line_health =      QLineEdit()
            self.line_health_st =   QLineEdit()
            self.line_phobia =      QLineEdit()
            self.line_phobia_st =   QLineEdit()
            self.line_hobby =       QLineEdit()
            self.line_baggage =     QLineEdit()
            self.line_fact1 =       QLineEdit()
            self.line_fact2 =       QLineEdit()

            self.line_profession.setReadOnly(True)
            self.line_bio_sex.setReadOnly(True)
            self.line_bio_age.setReadOnly(True)
            self.line_bio_pro.setReadOnly(True)
            self.line_bio_hob.setReadOnly(True)
            self.line_health.setReadOnly(True)
            self.line_health_st.setReadOnly(True)
            self.line_phobia.setReadOnly(True)
            self.line_phobia_st.setReadOnly(True)
            self.line_hobby.setReadOnly(True)
            self.line_baggage.setReadOnly(True)
            self.line_fact1.setReadOnly(True)
            self.line_fact2.setReadOnly(True)

            self.btn_profession =   QPushButton(self.icon_reveal, "")
            self.btn_bio =          QPushButton(self.icon_reveal, "")
            self.btn_health =       QPushButton(self.icon_reveal, "")
            self.btn_phobia =       QPushButton(self.icon_reveal, "")
            self.btn_hobby =        QPushButton(self.icon_reveal, "")
            self.btn_baggage =      QPushButton(self.icon_reveal, "")
            self.btn_fact1 =        QPushButton(self.icon_reveal, "")
            self.btn_fact2 =        QPushButton(self.icon_reveal, "")

            self.btn_action_card1 = QPushButton(f"Активировать карту №1: ")
            self.btn_action_card2 = QPushButton(f"Активировать карту №2: ")

            self.btn_profession.setIconSize(QSize(26, 26))
            self.btn_bio.setIconSize(QSize(26, 26))
            self.btn_health.setIconSize(QSize(26, 26))
            self.btn_phobia.setIconSize(QSize(26, 26))
            self.btn_hobby.setIconSize(QSize(26, 26))
            self.btn_baggage.setIconSize(QSize(26, 26))
            self.btn_fact1.setIconSize(QSize(26, 26))
            self.btn_fact2.setIconSize(QSize(26, 26))

            self.grid_player.addWidget(self.label_profession,   0, 0)
            self.grid_player.addWidget(self.label_bio,          1, 0)
            self.grid_player.addWidget(self.label_health,       2, 0)
            self.grid_player.addWidget(self.label_phobia,       3, 0)
            self.grid_player.addWidget(self.label_hobby,        4, 0)
            self.grid_player.addWidget(self.label_baggage,      5, 0)
            self.grid_player.addWidget(self.label_fact1,        6, 0)
            self.grid_player.addWidget(self.label_fact2,        7, 0)

            self.grid_player.addWidget(self.line_profession,    0, 1, 1, 4)
            self.grid_player.addWidget(self.line_bio_sex,       1, 1)
            self.grid_player.addWidget(self.line_bio_age,       1, 2)
            self.grid_player.addWidget(self.line_bio_pro,       1, 3)
            self.grid_player.addWidget(self.line_bio_hob,       1, 4)
            self.grid_player.addWidget(self.line_health,        2, 1, 1, 3)
            self.grid_player.addWidget(self.line_health_st,     2, 4)
            self.grid_player.addWidget(self.line_phobia,        3, 1, 1, 3)
            self.grid_player.addWidget(self.line_phobia_st,     3, 4)
            self.grid_player.addWidget(self.line_hobby,         4, 1, 1, 4)
            self.grid_player.addWidget(self.line_baggage,       5, 1, 1, 4)
            self.grid_player.addWidget(self.line_fact1,         6, 1, 1, 4)
            self.grid_player.addWidget(self.line_fact2,         7, 1, 1, 4)

            self.grid_player.addWidget(self.btn_profession,     0, 5)
            self.grid_player.addWidget(self.btn_bio,            1, 5)
            self.grid_player.addWidget(self.btn_health,         2, 5)
            self.grid_player.addWidget(self.btn_phobia,         3, 5)
            self.grid_player.addWidget(self.btn_hobby,          4, 5)
            self.grid_player.addWidget(self.btn_baggage,        5, 5)
            self.grid_player.addWidget(self.btn_fact1,          6, 5)
            self.grid_player.addWidget(self.btn_fact2,          7, 5)

            self.grid_player.addWidget(self.btn_action_card1, 8, 0, 1, 6)
            self.grid_player.addWidget(self.btn_action_card2, 9, 0, 1, 6)

            self.widget_player.setLayout(self.grid_player)
            self.tab.addTab(self.widget_player, "О себе")

        def init_widget_about_all(self):
            self.tab.addTab(self.widget_aboutAll, "Общее")

        def init_widget_voting(self):
            self.tab.addTab(self.widget_voting, "Голосование")

        def init_widget_history(self):
            self.grid_history = QGridLayout()

            self.text_browser_history = QTextBrowser()
            self.text_browser_history.setReadOnly(True)
            self.grid_history.addWidget(self.text_browser_history)

            self.widget_history.setLayout(self.grid_history)
            self.tab.addTab(self.widget_history, "История")

        def set_tooltips(self):
            """Устанавливает всплывающие подсказки"""
            self.label_nik.setToolTip("Ваш ник")

            self.tab.setTabToolTip(0, "Окно информации о своем персонаже")

            self.btn_profession.setToolTip("Раскрыть характеристику")
            self.btn_bio.setToolTip("Раскрыть характеристику")
            self.btn_health.setToolTip("Раскрыть характеристику")
            self.btn_phobia.setToolTip("Раскрыть характеристику")
            self.btn_hobby.setToolTip("Раскрыть характеристику")
            self.btn_baggage.setToolTip("Раскрыть характеристику")
            self.btn_fact1.setToolTip("Раскрыть характеристику")
            self.btn_fact2.setToolTip("Раскрыть характеристику")

            self.btn_action_card1.setToolTip("Активировать карту действия<br>Можно воспользоваться в любой момент")
            self.btn_action_card2.setToolTip("Активировать карту действия<br>Можно воспользоваться в любой момент")

            self.btn_leave.setToolTip("Покинуть текущую игру<br>Вернуться в сессию будет <b>невозможно</b>")

        def fill_characteristic(self, params):
            self.line_profession.setText(params[0])
            self.line_bio_sex.setText(params[1])
            self.line_bio_age.setText(params[2])
            self.line_bio_pro.setText(params[3])
            self.line_bio_hob.setText(params[4])
            self.line_health.setText(params[5])
            self.line_health_st.setText(params[6])
            self.line_phobia.setText(params[7])
            self.line_phobia_st.setText(params[8])
            self.line_hobby.setText(params[9])
            self.line_baggage.setText(params[10])
            self.line_fact1.setText(params[11])
            self.line_fact2.setText(params[12])
            self.btn_action_card1.setText("Активировать карту №1: " + params[13])
            self.btn_action_card2.setText("Активировать карту №2: " + params[14])

        def btn_leave_event(self):
            self.parent.disconnect_button_event()
            self.parent.show()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_window = BunkerClientStartWindow()
    sys.exit(app.exec_())
