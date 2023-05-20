import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class Server1(QWidget):
    def __init__(self):
        super(Server1, self).__init__()

        # 1
        self.sock = QUdpSocket(self)

        # 2
        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.btn = QPushButton('Start Server', self)
        self.btn.clicked.connect(self.start_stop_slot)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.btn)
        self.setLayout(self.v_layout)

        # 3
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.send_data_slot)

    def start_stop_slot(self):
        """При запуске таймера сервер будет отправлять данные клиенту каждую секунду"""
        if not self.timer.isActive():
            self.btn.setText('Stop Server')

            self.timer.start(1000)
        else:
            self.btn.setText('Start Server')
            self.timer.stop()

    def send_data_slot(self):
        message = QDateTime.currentDateTime().toString()

        self.label.setText(message)
        datagram = message.encode()
        self.sock.writeDatagram(datagram, QHostAddress.LocalHost, 6666)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Server1()
    ex.show()
    sys.exit(app.exec_())