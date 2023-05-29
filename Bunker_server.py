import sys, sqlite3, random
from PyQt5.QtNetwork import QTcpServer, QHostAddress, QNetworkInterface
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QVBoxLayout, QLabel


class Server(QWidget):
    def __init__(self):
        super(Server, self).__init__()

        self.set_full_number()

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
        """is_first"""
        sock = self.server.nextPendingConnection()

        peer_name = str(sock.peerName())
        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Connected {} address {}, port {}'.format(peer_name, peer_address, str(peer_port))
        self.browser.append(news)

        sock.readyRead.connect(lambda: self.read_data_slot(sock))
        sock.disconnected.connect(lambda: self.disconnected_slot(sock))

    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            datagram = sock.read(sock.bytesAvailable())

        message = datagram.decode()
        command = message[:3]
        if command == "00:":
            """тут нужно сравнить имя в базе на уникальность"""
            self.add_new_player(name=message[3:], sock=sock, id=len(self.players))
        elif command == "01:":
            pass

    def disconnected_slot(self, sock):
        peer_address = sock.peerAddress().toString()

        peer_port = sock.peerPort()
        news = 'Disconnected with address {}, port {}'.format(peer_address, str(peer_port))
        self.browser.append(news)

        sock.close()

    def add_new_player(self, name, sock, id):
        player = Player(parent=self, name=name, sock=sock, id=id)
        if player.no_cards_remain == True:
            sock.write("01:".encode())
            sock.close()
        self.players.append(player)
        self.browser.append(f"Добавлен игрок {player.get_info()}")

    def set_full_number(self):
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
    def __init__(self, parent, name, sock, id):
        self.parent = parent
        self.name = name
        self.sock = sock
        self.id = int(id)

        self.no_cards_remain = False

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

        self.is_action_card1 = True
        self.is_action_card2 = True

    def get_info(self):
        return (self.id, self.name, self.bio, self.profession, self.health, self.phobia, self.hobby,
                self.baggage, self.fact1, self.fact2,
                self.action_card1, self.is_action_card1, self.action_card2, self.is_action_card2)

    def get_sock_by_id(self, id):
        if id == self.id:
            return self.sock
        else:
            return False

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

            result = f"{sex}, возраст: {age}, стаж работы: {exp_prof}, стаж хобби: {exp_hobby}"
        else:
            try:
                sqlite_connection = sqlite3.connect('BunkerDB.db')
                cursor = sqlite_connection.cursor()
                sqlite_select_0 = f"SELECT name FROM {param} WHERE remain > 0 LIMIT 1 OFFSET ABS(RANDOM()) % MAX((SELECT COUNT(*) FROM {param} WHERE remain > 0), 1)"

                try:
                    cursor.execute(sqlite_select_0)
                    result = cursor.fetchone()[0]
                except:
                    result = "no_cards_remain"

                sqlite_update_0 = f"UPDATE {param} SET remain = remain - 1 WHERE name = \"{result}\""
                cursor.execute(sqlite_update_0)
                sqlite_connection.commit()

                if (param == "phobia" or param == "health"):
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

        if (param == "phobia" or param == "health") and abss == 0:
            result += random.choice([" 10% тяжести", " 30% тяжести", " 60% тяжести", " 100% тяжести"])

        # self.parent.browser.append(result)
        if result=="no_cards_remain":
            self.no_cards_remain = True
        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Server()
    demo.show()
    sys.exit(app.exec_())