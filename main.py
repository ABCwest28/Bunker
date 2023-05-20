import sys
import socket
import sqlite3
import font_resources_rc

from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QFontDatabase, QColor
from PyQt5.QtWidgets import *

class WidgetBunkerClient(QMainWindow):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        super().__init__()
        self.wrapper = QWidget(self)
        self.initUI()
        self.initConnect()

    def initUI(self):
        self.resize(900, 500)
        self.setWindowTitle('Bunker Client')
        self.statusBar().showMessage(f"Запущено. IP:")
        self.setWindowToCenter()

    def initConnect(self):
        current_ip = input()
        self.client.connect((str(current_ip), 2050))

    def setWindowToCenter(self):
        my_frame_geom = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        my_frame_geom.moveCenter(screen_center)
        self.move(my_frame_geom.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WidgetBunkerClient()
    sys.exit(app.exec_())