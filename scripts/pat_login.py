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
    dialog = pat_login(app)
    dialog.show()
    return dialog

def stop(dialog):
    dialog.close()

class pat_login(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self,app):
        self.app = app
        super(pat_login, self).__init__()

        self.firstname_info = "a"
        self.lastname_info = "a"
        self.ssn_info = "a"
        self.makeform()


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        #mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Enter Patient Information")
        #self.showMaximized()

        #THEME COLOR
        self.palette = self.palette()
        #self.palette.setColor(QPalette.Window, QColor("#82CAFA"))
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("background/texture.jpg")))
        #self.palette.setColor(QPalette.Button, QColor('red'))
        self.setPalette(self.palette)
        self.formGroupBox.setStyleSheet("QGroupBox {background-image: url(background/texture.jpg)}")
        self.success = False
        print("Patient Login Screen")
        self.exec()


    def makeform(self):
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        self.line_edit_firstname = QLineEdit()
        self.line_edit_firstname.setPlaceholderText('Enter First Name')
        self.line_edit_lastname = QLineEdit()
        self.line_edit_lastname.setPlaceholderText('Enter Last Name')
        self.line_edit_ssn = QLineEdit()
        self.line_edit_ssn.setPlaceholderText('Enter 9-Digit SSN')
        self.line_edit_ssn.setEchoMode(QLineEdit.Password)


        self.firstname = QLabel("First Name:")
        self.lastname = QLabel("Last Name:")
        self.ssn = QLabel("SSN:")


        #label_person = QLabel('User Type')
        #self.combo_label_person = QComboBox()
        #self.combo_label_person.addItem("Technician")
        #self.combo_label_person.addItem("Doctor")

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        button_login.clicked.connect(self.successlogin)


        layout.addRow(self.firstname, self.line_edit_firstname )
        layout.addRow(self.lastname, self.line_edit_lastname)
        layout.addRow(self.ssn, self.line_edit_ssn)
        #layout.addRow(label_person, self.combo_label_person)
        layout.addRow(button_login)


        self.formGroupBox.setLayout(layout)



    def check_password(self):
        msg = QMessageBox()
        if (self.line_edit_firstname.text() == self.firstname_info) and (self.line_edit_lastname.text() == self.lastname_info) and (self.line_edit_ssn.text() == self.ssn_info):
            user_type = "Patient"
            result = True
            self.success = True
            msg.setText('Success')
            msg.exec_()
            #self.app.quit()
        elif (self.line_edit_firstname.text() == "") or (self.line_edit_lastname.text() == "") or (self.line_edit_ssn.text() == ""):
            msg.setText('Empty Fields')
            msg.exec_()
            user_type= None
            result = False
        else:
            msg.setText('No Matching Records Found')
            msg.exec_()
            user_type= None
            result = False
        return (result, user_type)


    def successlogin(self):
        if (self.line_edit_firstname.text() == self.firstname_info) and (self.line_edit_lastname.text() == self.lastname_info) and (self.success==True):
            user_type = "Patient"
            result = True
            self.app.quit()
        else:
            user_type= None
            result = False

        return(result,user_type)

