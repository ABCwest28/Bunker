from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtCore import Qt
import sys

app = QApplication(sys.argv)

client = QTcpSocket()
ip_address_input = QLineEdit()
connect_button = QPushButton("Connect")

def handle_connect():
    ip_address = ip_address_input.text()
    client.connectToHost(ip_address, 8888)

def handle_connected():
    if client.state() == Qt.ConnectedState:
        print("Успешно подключено к серверу")
    else:
        print("Не удалось подключиться к серверу")

client.connected.connect(handle_connected)

connect_button.clicked.connect(handle_connect)

layout = QVBoxLayout()
layout.addWidget(ip_address_input)
layout.addWidget(connect_button)

window = QWidget()
window.setLayout(layout)
window.show()

sys.exit(app.exec_())

# 192.168.0.1