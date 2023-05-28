import sys, sqlite3, random
from PyQt5.QtNetwork import QTcpServer, QHostAddress, QNetworkInterface
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QVBoxLayout, QLabel


class Server(QWidget):
    def __init__(self):
        super(Server, self).__init__()

        self.players = []

        self.resize(500, 450)

        self.label = QLabel(f"Текущий ip: {QNetworkInterface.allAddresses()[1].toString()}")

        self.browser = QTextBrowser(self)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.browser)
        self.setLayout(self.v_layout)

        self.server = QTcpServer(self)
        if not self.server.listen(QHostAddress.Any, 40040):
            self.browser.append(self.server.errorString())
        self.server.newConnection.connect(self.new_socket_slot)

    def new_socket_slot(self):
        sock = self.server.nextPendingConnection()

        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Connected with address {}, port {}'.format(peer_address, str(peer_port))
        self.browser.append(news)

        sock.readyRead.connect(lambda: self.read_data_slot(sock))
        sock.disconnected.connect(lambda: self.disconnected_slot(sock))

    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            datagram = sock.read(sock.bytesAvailable())

        message = datagram.decode()
        if message[:3] == "00:":
            """тут нужно сравнить имя в базе на уникальность"""
            self.add_new_player(name=message[3:])

    def disconnected_slot(self, sock):
        peer_address = sock.peerAddress().toString()

        peer_port = sock.peerPort()
        news = 'Disconnected with address {}, port {}'.format(peer_address, str(peer_port))
        self.browser.append(news)

        sock.close()

    def add_new_player(self, name):
        player = Player(parent=self, name=name)
        self.players.append(player)
        self.browser.append("Добавлен игрок")


class Player:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

        self.bio =          self.get_data(param="bio")
        self.profession =   self.get_data(param="profession")
        self.health =       self.get_data(param="health")
        self.phobia =       self.get_data(param="phobia")
        self.hobby =        self.get_data(param="hobby")
        self.baggage =      self.get_data(param="baggage")
        self.fact1 =        self.get_data(param="fact")
        self.fact2 =        self.get_data(param="fact")
        self.action_card1 = self.get_data(param="action_card")
        self.action_card2 = self.get_data(param="action_card")

    def get_data(self, param):
        if param == "bio":
            age = sum(random.randint(0, 100) for _ in range(3)) // 3
            if age < 18: age = 18
            exp_prof = min(random.randint(0, age - 18) for _ in range(3))
            exp_hobby = min(random.randint(0, age - 16) for _ in range(3))
            t_rand = random.randint(0, 3) == 0
            if t_rand == 0:
                sex = "Муж."
            elif t_rand == 1:
                sex = "Муж. бесплоден"
            elif t_rand == 2:
                sex = "Жен."
            else:
                sex = "Жен. бесплодна"

            result = f"{sex}, стаж работы: {exp_prof}, стаж хобби: {exp_hobby}"
        else:
            try:
                sqlite_connection = sqlite3.connect('BunkerDB.db')
                cursor = sqlite_connection.cursor()
                print("get_data->Подключен к SQLite")

                sqlite_select_0 = """
                SELECT name FROM ? 
                WHERE remain > 0 
                LIMIT 1 
                OFFSET ABS(RANDOM()) % MAX((SELECT COUNT(*) 
                                            FROM table
                                            WHERE remain > 0), 1)"""
                cursor.execute(sqlite_select_0, (param, ))
                result = cursor.fetchone()
                cursor.close()

            except sqlite3.Error as error:
                self.parent.browser.append(f"Ошибка при работе с SQLite: {error}")
                result = "sql_error"

            finally:
                if sqlite_connection:
                    sqlite_connection.close()

        if param == "phobia" or param == "health":
            result += random.choice([" 10% тяжести", " 30% тяжести", " 60% тяжести", " 100% тяжести"])

        self.parent.browser.append(result)
        return result



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Server()
    demo.show()
    sys.exit(app.exec_())