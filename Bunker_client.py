import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5 import QtGui


class BunkerClientStartWindow(QWidget):
    """
    Окно для ввода никнейма и ip-адреса для подключения к серверу
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        client_window.show()


class BunkerClientMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window_1)
        self.setCentralWidget(self.button)

    def show_new_window_1(self):
        if self.w is None:
            self.w = BunkerClientStartWindow()
        self.w.show()
        self.close()

    def show_new_window_2(self, checked):
        """Этот метод аналог 1го"""
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_window = BunkerClientMainWindow()
    sys.exit(app.exec_())
