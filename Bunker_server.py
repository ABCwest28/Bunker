import sys, sqlite3, random
from PyQt5.QtNetwork import QTcpServer, QHostAddress, QNetworkInterface
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTextBrowser, QGridLayout, QLabel, QToolTip, QTabWidget,
                             QPushButton, QScrollBar, QLineEdit, QHBoxLayout, QSplitter)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
import font_resources_rc


class Server(QMainWindow):
    def __init__(self):
        super(Server, self).__init__()

        self.set_full_number()

        self.players = []
        self.limit_players = 20
        self.status = False
        """True-игра начата, False-в ожидании"""

        self.server = QTcpServer(self)
        if not self.server.listen(QHostAddress.Any, 40040):
            self.browser.append(self.server.errorString())
        self.server.newConnection.connect(self.new_socket_slot)

        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(600, 500)

        self.wrapper = QWidget()
        self.grid_wrapper = QGridLayout()

        self.label_ip = QLabel(f"Текущий ip: {QNetworkInterface.allAddresses()[1].toString()}")
        self.tab = QTabWidget()
        self.btn_start_stop_session = QPushButton("Начать игру")

        self.setCentralWidget(self.wrapper)

        self.init_grid_wrapper()
        self.init_tab_players()
        self.init_tab_history()
        self.init_tab_settings()

        self.set_font_google()

    def init_grid_wrapper(self):
        self.grid_wrapper.addWidget(self.label_ip, 0, 0)
        self.grid_wrapper.addWidget(self.tab, 1, 0)
        self.grid_wrapper.addWidget(self.btn_start_stop_session, 2, 0)

        self.wrapper.setLayout(self.grid_wrapper)

    def init_tab_players(self):
        self.widget_players = QWidget()
        self.widget_players_list = QWidget()
        self.widget_players_list.setMinimumSize(200, 100)
        self.widget_players_output = QWidget()

        self.splitter = QSplitter()
        self.splitter.addWidget(self.widget_players_list)
        self.splitter.addWidget(self.widget_players_output)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.splitter)
        self.widget_players.setLayout(self.hbox)

        self.grid_players_list = QGridLayout()
        self.widget_players_list.setLayout(self.grid_players_list)

        self.grid_players_output = QGridLayout()
        self.widget_players_output.setLayout(self.grid_players_output)

        self.label_name =               QLabel("Имя")
        self.label_ip =                 QLabel("IP")
        self.label_profession =         QLabel("Профессия")
        self.label_bio =                QLabel("Био данные")
        self.label_health =             QLabel("Здоровье/стадия")
        self.label_phobia =             QLabel("Фобия/стадия")
        self.label_hobby =              QLabel("Хобби")
        self.label_baggage =            QLabel("Багаж")
        self.label_fact1 =              QLabel("Факт №1")
        self.label_fact2 =              QLabel("Факт №2")
        self.label_action_card1 =       QLabel("Карта действия №1")
        self.label_action_card2 =       QLabel("Карта действия №2")

        self.label_name.setAlignment(Qt.AlignRight)
        self.label_ip.setAlignment(Qt.AlignRight)
        self.label_profession.setAlignment(Qt.AlignRight)
        self.label_bio.setAlignment(Qt.AlignRight)
        self.label_health.setAlignment(Qt.AlignRight)
        self.label_phobia.setAlignment(Qt.AlignRight)
        self.label_hobby.setAlignment(Qt.AlignRight)
        self.label_baggage.setAlignment(Qt.AlignRight)
        self.label_fact1.setAlignment(Qt.AlignRight)
        self.label_fact2.setAlignment(Qt.AlignRight)
        self.label_action_card1.setAlignment(Qt.AlignRight)
        self.label_action_card2.setAlignment(Qt.AlignRight)

        self.line_name =                QLineEdit()
        self.line_ip =                  QLineEdit()
        self.line_profession =          QLineEdit()
        self.line_bio_sex =             QLineEdit()
        self.line_bio_age =             QLineEdit()
        self.line_bio_pro =             QLineEdit()
        self.line_bio_hob =             QLineEdit()
        self.line_health =              QLineEdit()
        self.line_health_st =           QLineEdit()
        self.line_phobia =              QLineEdit()
        self.line_phobia_st =           QLineEdit()
        self.line_hobby =               QLineEdit()
        self.line_baggage =             QLineEdit()
        self.line_fact1 =               QLineEdit()
        self.line_fact2 =               QLineEdit()
        self.line_action_card1 =        QLineEdit()
        self.line_action_card2 =        QLineEdit()

        self.grid_players_output.addWidget(self.label_name,         0, 0)
        self.grid_players_output.addWidget(self.label_ip,           1, 0)
        self.grid_players_output.addWidget(self.label_profession,   2, 0)
        self.grid_players_output.addWidget(self.label_bio,          3, 0)
        self.grid_players_output.addWidget(self.label_health,       4, 0)
        self.grid_players_output.addWidget(self.label_phobia,       5, 0)
        self.grid_players_output.addWidget(self.label_hobby,        6, 0)
        self.grid_players_output.addWidget(self.label_baggage,      7, 0)
        self.grid_players_output.addWidget(self.label_fact1,        8, 0)
        self.grid_players_output.addWidget(self.label_fact2,        9, 0)
        self.grid_players_output.addWidget(self.label_action_card1, 10, 0)
        self.grid_players_output.addWidget(self.label_action_card2, 11, 0)

        self.grid_players_output.addWidget(self.line_name,          0, 1, 1, 4)
        self.grid_players_output.addWidget(self.line_ip,            1, 1, 1, 4)
        self.grid_players_output.addWidget(self.line_profession,    2, 1, 1, 4)
        self.grid_players_output.addWidget(self.line_bio_sex,       3, 1)
        self.grid_players_output.addWidget(self.line_bio_age,       3, 2)
        self.grid_players_output.addWidget(self.line_bio_pro,       3, 3)
        self.grid_players_output.addWidget(self.line_bio_hob,       3, 4)
        self.grid_players_output.addWidget(self.line_health,        4, 1, 1, 3)
        self.grid_players_output.addWidget(self.line_health_st,     4, 4)
        self.grid_players_output.addWidget(self.line_phobia,        5, 1, 1, 3)
        self.grid_players_output.addWidget(self.line_phobia_st,     5, 4)
        self.grid_players_output.addWidget(self.line_hobby,         6, 1, 1, 4)
        self.grid_players_output.addWidget(self.line_baggage,       7, 1, 1, 4)
        self.grid_players_output.addWidget(self.line_fact1,         8, 1, 1, 4)
        self.grid_players_output.addWidget(self.line_fact2,         9, 1, 1, 4)
        self.grid_players_output.addWidget(self.line_action_card1,  10, 1, 1, 4)
        self.grid_players_output.addWidget(self.line_action_card2,  11, 1, 1, 4)

        self.tab.addTab(self.widget_players, "Игроки")

    def init_tab_history(self):
        self.widget_history = QWidget()
        self.grid_history = QGridLayout()

        self.browser = QTextBrowser()
        self.horizontal_scrollbar = QScrollBar()
        self.browser.setHorizontalScrollBar(self.horizontal_scrollbar)
        self.btn_clear_history = QPushButton("Очистить историю")
        self.btn_clear_history.clicked.connect(self.clear_history)
        self.grid_history.addWidget(self.browser, 0, 0)
        self.grid_history.addWidget(self.btn_clear_history, 1, 0)
        self.widget_history.setLayout(self.grid_history)

        self.tab.addTab(self.widget_history, "История")

    def clear_history(self):
        self.browser.clear()

    def init_tab_settings(self):
        self.widget_settings = QWidget()
        self.grid_settings = QGridLayout()

        self.tab.addTab(self.widget_settings, "Настройки")

    def set_font_google(self):
        font_id = QFontDatabase.addApplicationFont(":/fonts/GoogleSans-Regular.ttf")

        if font_id == 0:
            font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font14 = QFont(font_name, 14)
            self.font10 = QFont(font_name, 10)
        else:
            self.font14 = QFont()
            self.font10 = QFont()

        QToolTip.setFont(self.font10)
        self.setFont(self.font14)
        self.widget_players.setFont(self.font10)
        self.browser.setFont(self.font10)

    def new_socket_slot(self):
        sock = self.server.nextPendingConnection()

        peer_name = str(sock.peerName())
        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Connected {} address {}, port {}'.format(peer_name, peer_address, str(peer_port))
        self.browser.append(news)

        sock.readyRead.connect(lambda: self.read_data_slot(sock))
        sock.disconnected.connect(lambda: self.disconnected_slot(sock))

    def read_data_slot(self, sock):
        message = sock.readAll().data().decode()
        commands = message.split("\n")[:-1]
        for command in commands:
            type_command = command[:3]
            des_command = command[3:]
            if type_command == "00:":
                if len(self.players) == self.limit_players:
                    sock.write("02:".encode())  # Достигнут лимит игроков
                    sock.write("\n".encode())
                    sock.close()
                else:
                    """проверяем уникальность и если норм то добавляем"""
                    uniq = True
                    for cur_player in self.players:
                        if cur_player.name == des_command:
                            uniq = False
                    if uniq:
                        self.add_new_player(name=des_command, sock=sock)
                    else:
                        sock.write("03:".encode())  # Игрок с этим ником уже есть
                        sock.write("\n".encode())
                        sock.close()

            elif type_command == "04:":
                if len(self.players) == 1:
                    sock.write("05:1".encode())
                else:
                    sock.write("05:0".encode())
                sock.write("\n".encode())
            else:
                self.browser.append("UNKNOWN_COMMAND: " + type_command + des_command)

    def disconnected_slot(self, sock):
        """НУЖНО ПОДУМАТЬ ИГРОК ВЫГНАН ДИСКОНЕКТНУЛСА """
        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Disconnected with address {}, port {}'.format(peer_address, str(peer_port))
        self.browser.append(news)
        if not self.status:
            for cur_player in self.players:
                if isinstance(cur_player, Player):
                    if cur_player.get_name_by_sock(sock) is not None:
                        cur_player.return_cards_to_deck()
                        self.players.remove(cur_player)
                        if len(self.players) != 0:
                            self.players[0].sock.write("05:1".encode())
                            self.players[0].sock.write("\n".encode())
                else:
                    print("disconnected_slot-> cur_player - не является объектом Player")
        else:
            pass
        sock.close()

    def add_new_player(self, name, sock):
        player = Player(parent=self, name=name, sock=sock)
        if player.no_cards_remain:
            player.return_cards_to_deck()
            sock.write("01:".encode())
            sock.write("\n".encode())
            sock.close()
        else:
            self.players.append(player)
            self.browser.append(f"Добавлен игрок {player.get_info()}")

    def set_full_number(self):
        """remain = number для всех записей в бд"""
        try:
            sqlite_connection = sqlite3.connect('BunkerDB.db')
            cursor = sqlite_connection.cursor()
            for table in ("profession", "health", "phobia", "hobby", "baggage", "fact", "action_card"):
                sqlite_update_0 = f"UPDATE {table} SET remain = number"
                cursor.execute(sqlite_update_0)
                sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("set_full_number->Ошибка при работе с SQLite", error)
            self.browser.append(f"Ошибка при работе с SQLite: {error}")
        finally:
            if sqlite_connection:
                sqlite_connection.close()


class Player:
    def __init__(self, parent, name, sock):
        self.parent = parent
        self.name = name
        self.sock = sock

        self.no_cards_remain = False

        self.bio_sex = "inited"
        self.bio_age = 0
        self.bio_pro = 0
        self.bio_hob = 0
        self.get_data(param="bio")
        self.profession = self.get_data(param="profession")
        self.health_st = "inited"
        self.health = self.get_data(param="health")
        self.phobia_st = "inited"
        self.phobia = self.get_data(param="phobia")
        self.hobby = self.get_data(param="hobby")
        self.baggage = self.get_data(param="baggage")
        self.fact1 = self.get_data(param="fact")
        self.fact2 = self.get_data(param="fact")
        self.action_card1 = self.get_data(param="action_card")
        self.action_card2 = self.get_data(param="action_card")

        self.is_action_card1 = True
        self.is_action_card2 = True

    def get_info(self, param="browser"):
        """
        param=="browser" - выдает инфу для уведомления в browser
        param=="sql_keys" - выдает значения полученные из таблицы
        """
        if param == "browser":
            return [self.name, self.bio_sex, self.bio_age, self.bio_pro, self.bio_hob, self.profession, self.health, self.health_st,
                    self.phobia, self.phobia_st, self.hobby, self.baggage, self.fact1, self.fact2,
                    self.action_card1, self.is_action_card1, self.action_card2, self.is_action_card2]
        elif param == "sql_keys":
            return [self.profession, self.health, self.phobia, self.hobby, self.baggage, self.fact1,
                    self.fact2, self.action_card1, self.action_card2]
        else:
            return "wrong param"

    def get_sock_by_name(self, name):
        """Возвращает socket player-а если name совпал с name-ом аргумента, None если не совпало"""
        if name == self.name:
            return self.sock
        else:
            return None

    def get_name_by_sock(self, sock):
        """Возвращает имя player-а если ссылка на socket совпала с socket-ом аргумента, None если не совпало"""
        if sock == self.sock:
            return self.name
        else:
            return None

    def get_data(self, param):
        result = "inited"
        if param == "bio":
            self.bio_age = sum(random.randint(0, 100) for _ in range(3)) // 3
            if self.bio_age < 18: self.bio_age = 18
            self.bio_pro = min(random.randint(0, self.bio_age - 18) for _ in range(3))
            self.bio_hob = min(random.randint(0, self.bio_age - 16) for _ in range(3))
            t_rand = random.randint(0, 3) == 0
            if t_rand == 0:
                self.bio_sex = "Муж."
            elif t_rand == 1:
                self.bio_sex = "Муж. бесплоден"
            elif t_rand == 2:
                self.bio_sex = "Жен."
            else:
                self.bio_sex = "Жен. бесплодна"

        else:
            try:
                sqlite_connection = sqlite3.connect('BunkerDB.db')
                cursor = sqlite_connection.cursor()
                sqlite_select_0 = f"SELECT name FROM {param} WHERE remain > 0 LIMIT 1 OFFSET ABS(RANDOM()) % " \
                                  f"MAX((SELECT COUNT(*) FROM {param} WHERE remain > 0), 1)"
                cursor.execute(sqlite_select_0)

                try:
                    result = cursor.fetchone()[0]
                except:
                    result = "no_cards_remain"

                sqlite_update_0 = f"UPDATE {param} SET remain = remain - 1 WHERE name = \"{result}\""
                cursor.execute(sqlite_update_0)
                sqlite_connection.commit()

                if param == "phobia" or param == "health":
                    if result != "no_cards_remain":
                        sqlite_select_1 = f"SELECT abss FROM {param} WHERE name=\"{result}\""
                        cursor.execute(sqlite_select_1)
                        abss = int(cursor.fetchone()[0])
                    else:
                        abss = 1

                cursor.close()

            except sqlite3.Error as error:
                self.parent.browser.append(f"Ошибка при работе с SQLite: {error}")
                result = "sql_error"
                abss = 0

            finally:
                if sqlite_connection:
                    sqlite_connection.close()

        if param == "health" and abss == 0:
            self.health_st = random.choice(["10% тяжести", "30% тяжести", "60% тяжести", "100% тяжести"])
        elif param == "health" and abss == 1:
            self.health_st = "Не применимо"
        if param == "phobia" and abss == 0:
            self.phobia_st = random.choice(["10% тяжести", "30% тяжести", "60% тяжести", "100% тяжести"])
        elif param == "phobia" and abss == 1:
            self.phobia_st = "Не применимо"

        if result == "no_cards_remain":
            self.no_cards_remain = True
        return result

    def __del__(self):
        print("__del__ is called")

    def return_cards_to_deck(self):
        """Возвращает значения remain (+1) для текущих параметров"""
        params = self.get_info("sql_keys")
        try:
            sqlite_connection = sqlite3.connect('BunkerDB.db')
            cursor = sqlite_connection.cursor()
            for table, param in zip(["profession", "health", "phobia", "hobby", "baggage",
                                     "fact", "fact", "action_card", "action_card"], params):
                sqlite_update_0 = f"UPDATE {table} SET remain = remain + 1 WHERE name = \"{param}\""
                cursor.execute(sqlite_update_0)
            sqlite_connection.commit()
        except sqlite3.Error as error:
            self.parent.browser.append(f"return_cards_to_deck->Ошибка при работе с SQLite: {error}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Server()
    demo.show()
    sys.exit(app.exec_())
