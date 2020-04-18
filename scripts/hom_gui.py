#!/usr/bin/env python3

import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QGroupBox, QPushButton, QLabel,  QGridLayout, QMainWindow)
from PyQt5.QtGui import QPixmap


def runit(app):
    gui = home_gui(app)
    gui.show()
    run = app.exec_()
    return gui, run

def stop(run):
    sys.exit(run)

#create home window class
class home_gui(QMainWindow):
    def __init__(self,app):
        self.app = app
        super().__init__()
        self.successful= 0
        self.usertype = 0

        self.setWindowTitle('Osmosis Jones Counter')
        self.resize(500, 190)


        ##the main widget layout
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QGridLayout())
        self.widget.layout().setContentsMargins(625, 260, 625, 330)
        self.widget.layout().setSpacing(20)
        #self.widget.layout().setColumnMinimumWidth(0, 100)
        #self.widget.layout().setColumnMinimumWidth(2, 100)
        #self.widget.layout().setRowMinimumHeight(0, 100)
        #self.widget.layout().setRowMinimumHeight(3, 100)
        self.showMaximized()

        # Small group1
        self.GroupBox1 = QGroupBox()
        layout1 = QGridLayout()
        self.GroupBox1.setLayout(layout1)
        #layout1.setContentsMargins(10, 10, 20, 5)
        layout1.setSpacing(10)
        self.widget.layout().addWidget(self.GroupBox1, 0, 0)
        self.GroupBox1.setStyleSheet("QGroupBox {background-image: url(background/texture.jpg);border: 5px solid white; border-radius: 5px;}")




        # image box1
        self.imageView = QLabel(self.widget)
        self.pixmap = QPixmap("background/user_icon.png")
        self.imageView.setPixmap(self.pixmap)
        layout1.addWidget(self.imageView, 0, 1,1,1)




        button_pat_login = QPushButton('Patients')
        button_pat_login.clicked.connect(self.button_login_clicked2)
        layout1.addWidget(button_pat_login, 1, 0,1,3)

        button_login = QPushButton('Medical Personnel')
        button_login.clicked.connect(self.button_login_clicked)
        #button_login.clicked.connect(self.login_button)
        #button_login.clicked.connect(self.success)
        layout1.addWidget(button_login,2,0,1,3)

        self.setStyleSheet("QMainWindow {background-image: url(background/background.jpg)}")
        print("Home Screen")

        #=====PASS PATIENT INFO THROUGH THESE VARIABLES
        self.fn =0
        self.ln =0
        self.dob=0
        self.ssn=0


    #======================== LOGIN FUNCTION ==========================#
    @QtCore.pyqtSlot()
    def button_login_clicked(self):
        #self.login_button()
        from scripts import login
        loginapp = login.runit(self.app)
        self.successful, self.usertype,self.fn, self.ln, self.dob, self.ssn = loginapp.successlogin()

    def login_button(self):
        return self.successful, self.usertype , self.fn, self.ln, self.dob, self.ssn

    # ======================== PATIENT LOGIN FUNCTION ==========================#
    @QtCore.pyqtSlot()
    def button_login_clicked2(self):
        #self.login_button()
        from scripts import pat_login
        loginapp2 = pat_login.runit(self.app)
        self.successful, self.usertype, self.fn, self.ln, self.dob, self.ssn = loginapp2.successlogin()

