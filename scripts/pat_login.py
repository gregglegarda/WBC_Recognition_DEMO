from PyQt5.QtWidgets import (QMainWindow, QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QDateEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout,QMessageBox)
from PyQt5.QtGui import QPalette,QColor, QBrush, QPixmap
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt
import os
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
        #=============== LOGIN INFO================
        filename4 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_normal.csv")
        self.fileName4 = filename4

        filename5 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_abnormal.csv")
        self.fileName5 = filename5

        self.input_result = 0
        self.input_result2 = 0
        self.firstname_info = 0
        self.lastname_info = 0
        self.dob_info = 0
        self.ssn_info = 0


        self.makeform()


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        #mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Check Patient Results")
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
        regex = QtCore.QRegExp("[a-z-A-Z_]+")
        validator = QtGui.QRegExpValidator(regex)


        self.line_edit_firstname = QLineEdit()
        self.line_edit_firstname.setPlaceholderText('Enter First Name')
        self.line_edit_firstname.setValidator(validator)

        self.line_edit_lastname = QLineEdit()
        self.line_edit_lastname.setPlaceholderText('Enter Last Name')
        self.line_edit_lastname.setValidator(validator)

        #from scripts.line_edit import LineEditDOB
        self.line_edit_dob = QDateEdit()
        self.line_edit_dob.setDisplayFormat("MM/dd/yyyy")
        #self.line_edit_dob = LineEditDOB(self.formGroupBox)

        from scripts.line_edit import LineEditSSN
        self.line_edit_ssn = QLineEdit()
        self.line_edit_ssn = LineEditSSN(self.formGroupBox)





        self.firstname = QLabel("First Name:")
        self.lastname = QLabel("Last Name:")
        self.dob = QLabel("DOB:")
        self.ssn = QLabel("SSN:")


        #label_person = QLabel('User Type')
        #self.combo_label_person = QComboBox()
        #self.combo_label_person.addItem("Technician")
        #self.combo_label_person.addItem("Doctor")

        button_login = QPushButton('Check Results')
        button_login.clicked.connect(self.check_password)
        button_login.clicked.connect(self.successlogin)


        layout.addRow(self.firstname, self.line_edit_firstname )
        layout.addRow(self.lastname, self.line_edit_lastname)
        layout.addRow(self.dob, self.line_edit_dob)
        layout.addRow(self.ssn, self.line_edit_ssn)
        #layout.addRow(label_person, self.combo_label_person)
        layout.addRow(button_login)


        self.formGroupBox.setLayout(layout)



    def check_password(self):
        msg = QMessageBox()
        self.input_result = self.loadCsv4(self.fileName4)
        self.input_result2 = self.loadCsv5(self.fileName5)

        print("Normal Database", self.input_result)
        print("Abormal Database", self.input_result2)
        if  self.input_result == True or self.input_result2 == True:
            user_type = "Patient"
            result = True
            self.success = True
            msg.setText('Success')
            msg.exec_()
            #self.app.quit()
        elif (self.line_edit_firstname.text() == "") or (self.line_edit_lastname.text() == "")  or (self.line_edit_ssn.text() == "") or (self.line_edit_dob.text() == ""):
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
        if (self.input_result == True or self.input_result2 == True) and (self.success==True):
            user_type = "Patient"
            result = True
            self.app.quit()
        else:
            user_type= None
            result = False

        return(result,user_type, self.line_edit_firstname.text(), self.line_edit_lastname.text(),self.line_edit_dob.text(),self.line_edit_ssn.text())

    # ==============# FUNCTION LOAD (NORMAL)#==============#

    def loadCsv4(self, fileName):
        try:
            with open(fileName, "r") as fileInput:
                for row in csv.reader(fileInput):
                    if self.line_edit_firstname.text() == row[2] and self.line_edit_lastname.text() == row[3] and self.line_edit_dob.text() == row[4] and self.line_edit_ssn.text() == row[5]:
                        print(self.line_edit_firstname.text(),"=", row[2] ,"and", self.line_edit_lastname.text() ,"=", row[3] ,"and", self.line_edit_dob.text() ,"=", row[4] ,"and", self.line_edit_ssn.text() ,"=", row[5])
                        return True
        except:
            print("No Normal Database")

    def loadCsv5(self, fileName):
        try:
            with open(fileName, "r") as fileInput:
                for row in csv.reader(fileInput):
                    if self.line_edit_firstname.text() == row[2] and self.line_edit_lastname.text() == row[3] and self.line_edit_dob.text() == row[4] and self.line_edit_ssn.text() == row[5]:
                        return True
        except:
            print("No Normal Database")



