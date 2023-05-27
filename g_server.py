import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class ClientThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, socket_descriptor):
        super(ClientThread, self).__init__()
        self.socket_descriptor = socket_descriptor

    def run(self):
        socket = QTcpSocket()
        socket.setSocketDescriptor(self.socket_descriptor)

        while socket.state() == QTcpSocket.ConnectedState:
            if socket.waitForReadyRead():
                data = socket.readAll().data().decode()
                self.data_received.emit(data)

        socket.deleteLater()


class ServerWindow(QMainWindow):
    def __init__(self):
        super(ServerWindow, self).__init__()

        self.tcp_server = QTcpServer()
        self.tcp_server.listen(QHostAddress.Any, port=8888)
        self.tcp_server.newConnection.connect(self.handle_new_connection)

        self.clients = []

    def handle_new_connection(self):
        client_socket = self.tcp_server.nextPendingConnection()
        client_thread = ClientThread(client_socket.socketDescriptor())
        client_thread.data_received.connect(self.handle_client_data)
        client_thread.finished.connect(client_thread.deleteLater)
        client_thread.start()
        self.clients.append(client_thread)

    def handle_client_data(self, data):
        # Обработка полученных данных от клиента
        # Например, можно отправить данные всем клиентам:
        for client in self.clients:
            client.socket().write(data.encode())
            client.socket().flush()

        # Или можно отправить данные только конкретному клиенту:
        # client = self.clients[0]
        # client.socket().write(data.encode())
        # client.socket().flush()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server_window = ServerWindow()
    server_window.show()
    sys.exit(app.exec_())