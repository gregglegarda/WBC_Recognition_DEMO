from PyQt5.QtWidgets import (QMainWindow, QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout,QMessageBox)
from PyQt5.QtGui import QPalette,QColor, QBrush, QPixmap
from PyQt5 import Qt
import sys
import numpy as np
from datetime import datetime
from uuid import uuid4

def runit(app):
    dialog = login(app)
    dialog.show()
    return dialog

def stop(dialog):
    dialog.close()

class login(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self,app):
        self.app = app
        super(login, self).__init__()

        self.username_info = "username"
        self.password_info = "password"
        self.makeform()


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        #mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Enter Login Information")
        #self.showMaximized()

        #THEME COLOR
        self.palette = self.palette()
        #self.palette.setColor(QPalette.Window, QColor("#82CAFA"))
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("background/texture.jpg")))
        #self.palette.setColor(QPalette.Button, QColor('red'))
        self.setPalette(self.palette)
        self.formGroupBox.setStyleSheet("QGroupBox {background-image: url(background/texture.jpg)}")
        self.success = False
        print("Login Screen")
        self.exec()


    def makeform(self):
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        self.line_edit_username = QLineEdit()
        self.line_edit_username.setPlaceholderText('Username')
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText('Password')
        self.line_edit_password.setEchoMode(QLineEdit.Password)


        self.username = QLabel("User Name:")
        self.password = QLabel("Password:")

        label_person = QLabel('User Type:')
        self.combo_label_person = QComboBox()
        self.combo_label_person.addItem("Technician")
        #self.combo_label_person.addItem("Patient")
        self.combo_label_person.addItem("Doctor")

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        button_login.clicked.connect(self.successlogin)


        layout.addRow(self.username, self.line_edit_username )
        layout.addRow(self.password, self.line_edit_password)
        layout.addRow(label_person, self.combo_label_person)
        layout.addRow(button_login)


        self.formGroupBox.setLayout(layout)



    def check_password(self):
        msg = QMessageBox()
        if (self.line_edit_username.text() == self.username_info) and (self.line_edit_password.text() == self.password_info):
            user_type = str(self.combo_label_person.currentText())
            result = True
            self.success = True
            msg.setText('Success')
            msg.exec_()
            #self.app.quit()
        elif (self.line_edit_username.text() == "") or (self.line_edit_password.text() == ""):
            msg.setText('Empty Fields')
            msg.exec_()
            user_type= None
            result = False
        else:
            msg.setText('Incorrect Password')
            msg.exec_()
            user_type= None
            result = False
        return (result, user_type)


    def successlogin(self):
        if (self.line_edit_username.text() == self.username_info) and (self.line_edit_password.text() == self.password_info) and (self.success==True):
            user_type = str(self.combo_label_person.currentText())
            result = True
            self.app.quit()
        else:
            user_type= None
            result = False

        return(result,user_type, 0,0,0,0)

