import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
import numpy as np

class data_entry(QWidget):

    def __init__(self):
        self.app = QApplication([])
        super().__init__()

        self.title = 'Enter Patient Information'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        #self.show()


    def getinfo(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        f = self.firstname()
        l = self.lastname()
        d = self.dob()
        s = self.ssn()
        return f,l,d,s


    def firstname(self):
        text, okPressed = QInputDialog.getText(self, 'Enter Patient Information', "First Name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
            return text

    def lastname(self):
        text, okPressed = QInputDialog.getText(self, 'Enter Patient Information', "Last Name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
            return text

    def dob(self):
        text, okPressed = QInputDialog.getText(self, 'Enter Patient Information', "Date of Birth (MM-DD-YYY):", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
            return text

    def ssn(self):
        text, okPressed = QInputDialog.getText(self, 'Enter Patient Information', "Social Security Number (XXX-XX-XXXX):", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
            return text




