import sys, sqlite3
from PyQt5.QtNetwork import QTcpServer, QHostAddress, QNetworkInterface
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QVBoxLayout, QLabel


class Server(QWidget):
    def __init__(self):
        super(Server, self).__init__()

        self.resize(500, 450)

        self.label = QLabel(f"Текущий ip: {QNetworkInterface.allAddresses()[1].toString()}")

        self.browser = QTextBrowser(self)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.browser)
        self.setLayout(self.v_layout)

        self.server = QTcpServer(self)
        # if not self.server.listen(QHostAddress.Any, 40040):
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

    # 3
    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            datagram = sock.read(sock.bytesAvailable())

        message = datagram.decode()
        sock.write(message)

    def disconnected_slot(self, sock):
        peer_address = sock.peerAddress().toString()

        peer_port = sock.peerPort()
        news = 'Disconnected with address {}, port {}'.format(peer_address, str(peer_port))
        self.browser.append(news)

        sock.close()

class Player:
    def __init__(self):
        self.profession =   self.get_data("profession")
        self.bio =          self.get_data("bio")
        self.health =       self.get_data("health")
        self.phobia =       self.get_data("phobia")
        self.hobby =        self.get_data("hobby")
        self.baggage =      self.get_data("baggage")
        self.fact1 =        self.get_data("fact")
        self.fact2 =        self.get_data("fact")
        self.action_card1 = self.get_data("action_card")

    def get_data(self, param):
        try:
            sqlite_connection = sqlite3.connect('BunkerDB.db')
            cursor = sqlite_connection.cursor()
            print("get_data->Подключен к SQLite")

            sqlite_select_0 = f"SELECT name FROM {param} WHERE remain > 0"
            cursor.execute(sqlite_select_0)
            result_0 = cursor.fetchall()

            sqlite_select_1 = """SELECT * FROM TasksTable WHERE isComplete = '1'"""
            cursor.execute(sqlite_select_1)
            result_1 = cursor.fetchall()

            n = 0
            for i in result_0:
                self.table.setRowCount(n + 1)
                self.table.setItem(n, 0, QTableWidgetItem(str(i[0])))
                self.table.setItem(n, 1, QTableWidgetItem(i[1]))
                self.table.setItem(n, 2, QTableWidgetItem(i[2]))
                self.table.setItem(n, 3, QTableWidgetItem("не выполнено"))
                self.table.item(n, 3).setBackground(QColor(50, 50, 150, 35))

                n += 1

            for i in result_1:
                self.table.setRowCount(n + 1)
                self.table.setItem(n, 0, QTableWidgetItem(str(i[0])))
                self.table.setItem(n, 1, QTableWidgetItem(i[1]))
                self.table.setItem(n, 2, QTableWidgetItem(i[2]))
                self.table.setItem(n, 3, QTableWidgetItem("выполнено"))
                self.table.item(n, 3).setBackground(QColor(0, 250, 150, 35))
                n += 1

            cursor.close()

        except sqlite3.Error as error:
            print("outputTaskTable->Ошибка при работе с SQLite", error)
            self.statusBar().showMessage(f"Ошибка при работе с SQLite: {error}")

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("outputTaskTable->Соединение с SQLite закрыто")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Server()
    demo.show()
    sys.exit(app.exec_())