import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtNetwork import QTcpSocket


class ClientWindow(QMainWindow):
    def __init__(self):
        super(ClientWindow, self).__init__()

        self.wrapper = QWidget()
        self.setCentralWidget(self.wrapper)

        self.layout1 = QGridLayout()
        self.connect_button = QPushButton("connect")
        self.send_button = QPushButton("send")

        self.layout1.addWidget(self.connect_button, 0, 0)
        self.layout1.addWidget(self.send_button, 1, 0)

        self.wrapper.setLayout(self.layout1)

        self.tcp_socket = QTcpSocket()
        self.tcp_socket.connected.connect(self.handle_connected)
        self.tcp_socket.readyRead.connect(self.handle_ready_read)

        self.connect_button.clicked.connect(self.connect_to_server)
        self.send_button.clicked.connect(self.send_data)

    def connect_to_server(self):
        self.tcp_socket.connectToHost('127.0.0.1', 8888)

    def handle_connected(self):
        self.status_label.setText('Connected to server')

    def handle_ready_read(self):
        data = self.tcp_socket.readAll().data().decode()
        self.receive_text.append(data)

    def send_data(self):
        data = self.send_text.text()
        self.tcp_socket.write(data.encode())
        self.tcp_socket.flush()
        self.send_text.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_window = ClientWindow()
    client_window.show()
    sys.exit(app.exec_())
