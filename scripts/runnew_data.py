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
    dialog = data_entry(app)
    dialog.show()
    return dialog.getinfo(), dialog

def stop(dialog):
    dialog.close()

class data_entry(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self,app):
        self.app = app
        super(data_entry, self).__init__()


        self.makeform()

        runButton = QPushButton(self.tr("&Run"))
        runButton.setDefault(True)
        exitButton = QPushButton(self.tr("&Exit"))
        exitButton.setAutoDefault(False)
        buttonBox = QDialogButtonBox()
        buttonBox.addButton(runButton, QDialogButtonBox.AcceptRole)
        buttonBox.addButton(exitButton, QDialogButtonBox.RejectRole)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Enter Specimen Information")
        #self.showMaximized()

        #THEME COLOR
        self.palette = self.palette()
        #self.palette.setColor(QPalette.Window, QColor("#82CAFA"))
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("background/texture.jpg")))
        #self.palette.setColor(QPalette.Button, QColor('red'))
        self.setPalette(self.palette)
        self.formGroupBox.setStyleSheet("QGroupBox {background-image: url(background/texture.jpg)}")
        self.success = False
        print("Data Entry Screen")
        self.exec()


    def makeform(self):
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        self.line_edit_firstname = QLineEdit()
        self.line_edit_lastname = QLineEdit()
        self.line_edit_dob = QLineEdit()
        self.line_edit_ssn = QLineEdit()

        self.firstname = QLabel("First Name:")
        self.lastname = QLabel("Last Name:")
        self.dob = QLabel("DOB:")
        self.ssn = QLabel("SSN:")


        layout.addRow(self.firstname, self.line_edit_firstname )
        layout.addRow(self.lastname, self.line_edit_lastname)
        layout.addRow(self.dob, self.line_edit_dob)
        layout.addRow(self.ssn, self.line_edit_ssn)
        #layout.addRow(QLabel("Country:"), QComboBox())
        #layout.addRow(QLabel("Age:"), QSpinBox())
        self.formGroupBox.setLayout(layout)





    def accept(self):
        msg = QMessageBox()
        if self.line_edit_firstname.text() != '' and self.line_edit_lastname.text() != '' and self.line_edit_dob.text() != '' and self.line_edit_ssn.text() != '':
            msg.setText('Success')
            msg.exec_()
            self.close()
            #self.app.quit()
            self.success = True
            return self.line_edit_firstname.text(), self.line_edit_lastname.text(), self.line_edit_dob.text(), self.line_edit_ssn.text()

        else:
            msg.setText('Empty Fields')
            msg.exec_()
            self.success = False
    def getinfo(self):

        uniqueid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        accession = uniqueid
        specimen_type = "Blood Smear"
        delta = np.timedelta64(5, 'h')  # EST(eastern) is -5 of UCT(universal)
        todays_datetime = np.datetime64('now') - delta  # timestamp right now

        return accession, todays_datetime, specimen_type, self.line_edit_firstname.text(), self.line_edit_lastname.text(), self.line_edit_dob.text(), self.line_edit_ssn.text(), self.success


