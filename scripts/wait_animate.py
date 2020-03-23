

from PyQt5.QtWidgets import (QMainWindow, QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout,QMessageBox)
from PyQt5.QtGui import QPalette,QColor
from PyQt5 import QtWidgets
import sys

def runit(app):
    gui = wait_window(app)
    run = app#.exec_()
    return gui, run

def stop(run):
    sys.exit(run)

class wait_window(QMainWindow):

    def __init__(self, app):
        self.app = app
        super(wait_window, self).__init__()
        ##the main widget layout
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QGridLayout())
        self.widget.layout().setContentsMargins(10, 10, 10, 10)
        self.widget.layout().setSpacing(0)
        self.setWindowTitle("Please wait")
        self.widget.layout().setColumnMinimumWidth(0, 50)
        self.widget.layout().setColumnMinimumWidth(3, 50)
        self.widget.layout().setRowMinimumHeight(0, 50)
        self.widget.layout().setRowMinimumHeight(6, 50)
        self.showMaximized()

        # THEME COLOR
        self.setStyleSheet("QMainWindow {background-image: url(background/background.jpg)}")
        print("Patient GUI Screen")

        ##LOGOUT BUTTON
        button_logout = QPushButton('Logout')
        button_logout.clicked.connect(self.logout_success)
        self.widget.layout().addWidget(button_logout, 1, 0)


    def logout_success(self):
        msg = QMessageBox()
        msg.setText('Logged out successful')
        msg.exec_()
        ## go to login screen
        self.close()
        #self.app.quit()

