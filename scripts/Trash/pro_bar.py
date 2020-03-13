from PyQt5.QtWidgets import (QMainWindow, QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout,QMessageBox, QProgressBar)
from PyQt5.QtGui import QPalette,QColor, QBrush, QPixmap, QIntValidator
from PyQt5 import QtCore
import sys
import numpy as np
from datetime import datetime
from uuid import uuid4

def runit(app):
    dialog = load_bar(app)
    dialog.show()
    return dialog

def stop(dialog):
    dialog.close()

class load_bar(QDialog):

    def __init__(self,app):
        self.app = app
        super(load_bar, self).__init__()

        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        # progressbar
        self.progressBar_runNew = QProgressBar()
        self.progressBar_runNew.setGeometry(200, 80, 250, 20)
        # ----progress bar
        layout.addRow(self.progressBar_runNew)
        self.formGroupBox.setLayout(layout)

        runButton = QPushButton(self.tr("&Run"))
        runButton.setDefault(True)
        buttonBox = QDialogButtonBox()
        buttonBox.addButton(runButton, QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(self.accept)



        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Progress")
        #self.showMaximized()



        #THEME COLOR
        self.palette = self.palette()
        #self.palette.setColor(QPalette.Window, QColor("#82CAFA"))
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("background/texture.jpg")))
        #self.palette.setColor(QPalette.Button, QColor('red'))
        self.setPalette(self.palette)
        self.formGroupBox.setStyleSheet("QGroupBox {background-image: url(background/texture.jpg)}")
        print("progress Bar")

        self.exec()


    def progress_bar_running(self):
        # PROGRESS BAR FUNCTION
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.001
            self.progressBar_runNew.setValue(self.completed)
            print(111)

