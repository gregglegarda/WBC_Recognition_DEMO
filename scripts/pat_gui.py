from PyQt5.QtWidgets import (QMainWindow, QApplication, QComboBox, QDialog, QTableView,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout,QMessageBox, QSizePolicy,QAbstractItemView)
from PyQt5.QtGui import QPalette,QColor, QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import ntpath


def runit(app, fn, ln,dob,ssn):
    gui = patient_gui(app, fn, ln,dob,ssn)
    run = app.exec_()
    return gui, run

def stop(run):
    sys.exit(run)

class patient_gui(QMainWindow):

    def __init__(self, app, pat_fn, pat_ln,pat_dob,pat_ssn):
        self.app = app
        super(patient_gui, self).__init__()


        #=================VIEW IN TABLE INFO
        self.firstname_info = pat_fn
        self.lastname_info = pat_ln
        self.dob_info = pat_dob
        self.ssn_info = pat_ssn

        ##the main widget layout
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QGridLayout())
        self.widget.layout().setContentsMargins(10, 10, 10, 10)
        self.widget.layout().setSpacing(0)
        self.setWindowTitle("Patient Results")
        #self.widget.layout().setColumnMinimumWidth(0, 50)
        #self.widget.layout().setColumnMinimumWidth(3, 50)
        #self.widget.layout().setRowMinimumHeight(0, 50)
        #self.widget.layout().setRowMinimumHeight(6, 50)
        self.showMaximized()

        # THEME COLOR
        self.setStyleSheet("QMainWindow {background-image: url(background/background.jpg)}")
        print("Patient GUI Screen")
        #=================== GROUPS ====================#
        # Small group1
        self.GroupBox1 = QGroupBox()
        layout1 = QGridLayout()
        self.GroupBox1.setLayout(layout1)
        layout1.setSpacing(5)
        self.widget.layout().addWidget(self.GroupBox1, 0, 0, 1, 3)


        #==================# LOGOUT BUTTON #==================#
        button_logout = QPushButton('Logout')
        button_logout.clicked.connect(self.logout_success)
        self.widget.layout().addWidget(button_logout, 2, 2)

        # ==================# NORMAL AND ABNORMAL BUTTON #==================#
        # TRUE NORMAL BUTTON
        pushButtonNormalDiffs = QtWidgets.QPushButton(self.widget)
        pushButtonNormalDiffs.setText("Normal")
        # pushButtonNormalDiffs.clicked.setText(QColor.blue("Normal Results"))
        pushButtonNormalDiffs.clicked.connect(self.on_pushButtonLoad_clicked4)
        layout1.addWidget(pushButtonNormalDiffs, 0, 2, 1, 1)

        # TRUE ABNORMAL BUTTON
        pushButtonAbnormalDiffs = QtWidgets.QPushButton(self.widget)
        pushButtonAbnormalDiffs.setText("Abnormal")
        pushButtonAbnormalDiffs.clicked.connect(self.on_pushButtonLoad_clicked5)
        layout1.addWidget(pushButtonAbnormalDiffs, 0, 3, 1, 1)

        #==================# TABLE DATABASE #==================#
        filename4 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_normal.csv")
        self.items4 = []
        self.fileName4 = filename4
        self.on_pushButtonLoad_clicked4

        filename5 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_abnormal.csv")
        self.items5 = []
        self.fileName5 = filename5
        self.on_pushButtonLoad_clicked5

        #set model settings
        self.model = QtGui.QStandardItemModel(self.widget)
        self.model.setHorizontalHeaderLabels(['Accession ID', 'Acc Date', 'First Name', 'Last Name', 'DOB', 'SSN', 'EOS %', 'LYM %','MON %', 'NEU %', 'Initial Result', 'Final Result'])
        self.tableView = QTableView(self.widget)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSortingEnabled(True)
        self.model.rowsInserted.connect(lambda: QtCore.QTimer.singleShot(0, self.tableView.scrollToBottom))
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #set widths
        self.tableView.setColumnWidth(0, 325)#id
        self.tableView.setColumnWidth(1, 200)#date
        self.tableView.setColumnWidth(2, 120)#first
        self.tableView.setColumnWidth(3, 120)#last
        self.tableView.setColumnWidth(4, 120)# DOB
        self.tableView.setColumnWidth(5, 120)# SSN
        self.tableView.setColumnWidth(6, 60)# E
        self.tableView.setColumnWidth(7, 60)# L
        self.tableView.setColumnWidth(8, 60)# M
        self.tableView.setColumnWidth(9, 60) # N
        self.tableView.setColumnWidth(10, 150) # Initial result

        #hide some columns
        self.tableView.setColumnHidden(6, True)
        self.tableView.setColumnHidden(7, True)
        self.tableView.setColumnHidden(8, True)
        self.tableView.setColumnHidden(9, True)
        self.tableView.setColumnHidden(10, False)


        #layout1.addRow(self.tableView)
        layout1.addWidget(self.tableView, 1, 0, 1, 4)





    ##############################   FUNCTIONS   #########################

    # ==============# FUNCTION (NORMAL)#==============#
    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked4(self):
        self.loadCsv4(self.fileName4)

    def loadCsv4(self, fileName):
        while (self.model.rowCount() > 0):
            self.model.removeRow(0)
        try:
            with open(fileName, "r") as fileInput:
                for row in csv.reader(fileInput):
                    if self.firstname_info == row[2] and self.lastname_info == row[3]:
                        self.items4 = [
                            QtGui.QStandardItem(field)
                            for field in row
                        ]
                        self.model.appendRow(self.items4)
        except:
            print("No Normal Database")

    # ==============# FUNCTION (ABNORMAL)#==============#
    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked5(self):
        self.loadCsv5(self.fileName5)

    def loadCsv5(self, fileName):
        while (self.model.rowCount() > 0):
            self.model.removeRow(0)
        try:
            with open(fileName, "r") as fileInput:
                for row in csv.reader(fileInput):
                    if self.firstname_info == row[2] and self.lastname_info == row[3]:
                        self.items5 = [
                            QtGui.QStandardItem(field)
                            for field in row
                        ]
                        self.model.appendRow(self.items5)
        except:
            print("No Abnormal Database")


    # ===============# LOGOUT FUNCTION#===============#
    def logout_success(self):
        msg = QMessageBox()
        msg.setText('Logged out successful')
        msg.exec_()
        ## go to login screen
        self.close()
        #self.app.quit()



    # ===============# LOAD CSV AND CHECK FOR THE LOGIN INFO#===============#