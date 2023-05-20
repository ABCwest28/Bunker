from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import sys


class Ui_Win1(object):
    def setupUi(self, Win1):
        Win1.setObjectName("Win1")
        Win1.resize(450, 800)
        self.widgetWin1 = QtWidgets.QWidget(Win1)
        self.widgetWin1.setObjectName("widgetWin1")

        self.text1 = QtWidgets.QLabel(self.widgetWin1)
        self.text1.setGeometry(QtCore.QRect(197, 378, 56, 16))
        self.text1.setObjectName("text1")

        Win1.setCentralWidget(self.widgetWin1)
        self.retranslateUi(Win1)
        QtCore.QMetaObject.connectSlotsByName(Win1)

    def retranslateUi(self, Win1):
        _translate = QtCore.QCoreApplication.translate
        Win1.setWindowTitle(_translate("Win1", "MainWindow"))
        self.text1.setText(_translate("Win1", "Win1"))


class Ui_Win2(object):
    def setupUi(self, Win2):
        Win2.setObjectName("Win2")
        Win2.resize(450, 800)
        self.widgetWin2 = QtWidgets.QWidget(Win2)
        self.widgetWin2.setObjectName("widgetWin2")
        self.text2 = QtWidgets.QLabel(self.widgetWin2)
        self.text2.setGeometry(QtCore.QRect(197, 378, 56, 16))
        self.text2.setObjectName("text2")

        Win2.setCentralWidget(self.widgetWin2)
        self.retranslateUi(Win2)
        QtCore.QMetaObject.connectSlotsByName(Win2)

    def retranslateUi(self, Win2):
        _translate = QtCore.QCoreApplication.translate
        Win2.setWindowTitle(_translate("Win2", "MainWindow"))
        self.text2.setText(_translate("Win2", "Win2"))


class Ui_Win3(object):
    def setupUi(self, Win3):
        Win3.setObjectName("Win3")
        Win3.resize(450, 800)
        self.widgetWin3 = QtWidgets.QWidget(Win3)
        self.widgetWin3.setObjectName("widgetWin3")
        self.text3 = QtWidgets.QLabel(self.widgetWin3)
        self.text3.setGeometry(QtCore.QRect(197, 378, 56, 16))
        self.text3.setObjectName("text3")

        Win3.setCentralWidget(self.widgetWin3)

        self.retranslateUi(Win3)
        QtCore.QMetaObject.connectSlotsByName(Win3)

    def retranslateUi(self, Win3):
        _translate = QtCore.QCoreApplication.translate
        Win3.setWindowTitle(_translate("Win3", "MainWindow"))
        self.text3.setText(_translate("Win3", "Win3"))


class Win1(QtWidgets.QMainWindow, Ui_Win1):
    def __init__(self, parent=None):
        super(Win1, self).__init__(parent)
        self.setupUi(self)


class Win2(QtWidgets.QMainWindow, Ui_Win2):
    def __init__(self, parent=None):
        super(Win2, self).__init__(parent)
        self.setupUi(self)


class Win3(QtWidgets.QMainWindow, Ui_Win3):
    def __init__(self, parent=None):
        super(Win3, self).__init__(parent)
        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.center()

        self.stacked = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked)

        self.window_Win1 = Win1(self)
        self.window_Win1.setStyleSheet('#Win1 {background-color: #ffbdcc;}')
        self.window_Win2 = Win2(self)
        self.window_Win2.setStyleSheet('#Win2 {background-color: #ccffbd;}')
        self.window_Win3 = Win3(self)
        self.window_Win3.setStyleSheet('#Win3 {background-color: #bdccccff;}')

        self.stacked.addWidget(self.window_Win1)
        self.stacked.addWidget(self.window_Win2)
        self.stacked.addWidget(self.window_Win3)

        self.create_buttons(self.window_Win1)

    def create_buttons(self, parent):
        bnt = QtWidgets.QPushButton("Win1", parent)
        #        self.bnt.setGeometry(QtCore.QRect(0, 772, 150, 28)) # установите свою геометрию
        bnt.setGeometry(QtCore.QRect(0, 572, 150, 28))

        bnt_2 = QtWidgets.QPushButton("Win2", parent)
        #        self.bnt_2.setGeometry(QtCore.QRect(150, 772, 150, 28))
        bnt_2.setGeometry(QtCore.QRect(150, 572, 150, 28))

        bnt_3 = QtWidgets.QPushButton("Win3", parent)
        #        self.bnt_3.setGeometry(QtCore.QRect(300, 772, 150, 28))
        bnt_3.setGeometry(QtCore.QRect(300, 572, 150, 28))

        bnt.clicked.connect(self.go_win1)
        bnt_2.clicked.connect(self.go_win2)
        bnt_3.clicked.connect(self.go_win3)
        bnt.show()
        bnt_2.show()
        bnt_3.show()

    def go_win1(self):
        self.stacked.setCurrentIndex(0)
        self.create_buttons(self.window_Win1)

    def go_win2(self):
        self.stacked.setCurrentIndex(1)
        self.create_buttons(self.window_Win2)

    def go_win3(self):
        self.stacked.setCurrentIndex(2)
        self.create_buttons(self.window_Win3)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(450, 650)  # <---- (450, 800)
    window.show()
    sys.exit(app.exec_())