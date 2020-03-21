
"""
This script is the whole gui QMainWindow of the Doctor Terminal.
It includes :
    The abnormal database (to be reviewed)
    Reviewed database (commented by the pathologist)
    View Images
    Comment section
    Logout button

"""



from PyQt5.QtWidgets import (QMainWindow, QTableView,
                            QGridLayout, QGroupBox,
                            QLabel, QLineEdit,  QPushButton,
                            QMessageBox, QAbstractItemView,
                            QPlainTextEdit)
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import ntpath



import numpy as np

def runit(app):

    gui = doctor_gui(app)
    run = app.exec_()
    return gui, run

def stop(run):
    sys.exit(run)

class doctor_gui(QMainWindow):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self,app):
        self.app = app
        super(doctor_gui, self).__init__()
        #==================# MAIN WIDGET LAYOUT #==================#
        #Big window


        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QGridLayout())
        self.widget.layout().setContentsMargins(40, 40, 40, 40)
        self.widget.layout().setSpacing(10)
        self.setWindowTitle("Pathologist Terminal")
        #self.widget.layout().setColumnMinimumWidth(0, 10)
        #self.widget.layout().setColumnMinimumWidth(1, 10)
        #self.widget.layout().setRowMinimumHeight(0, 10)
        #self.widget.layout().setRowMinimumHeight(2, 200)
        #self.widget.layout().setRowMinimumHeight(6, 10)
        self.showMaximized()
        #THEME COLOR
        self.setStyleSheet("QMainWindow {background-image: url(background/background.jpg)}")
        print("Pathologist GUI Screen")

        #Small group1
        self.GroupBox1 = QGroupBox()
        layout1 = QGridLayout()
        self.GroupBox1.setLayout(layout1)
        layout1.setSpacing(5)
        self.widget.layout().addWidget(self.GroupBox1, 0, 0,1,3)


        # Small group2
        self.GroupBox2 = QGroupBox()
        layout2 = QGridLayout()
        self.GroupBox2.setLayout(layout2)
        layout2.setSpacing(5)
        self.widget.layout().addWidget(self.GroupBox2, 1, 0,1,3)

        # Small group3
        self.GroupBox3 = QGroupBox()
        layout3 = QGridLayout()
        self.GroupBox3.setLayout(layout3)
        layout3.setSpacing(5)
        self.widget.layout().addWidget(self.GroupBox3, 2, 0, 1, 3)

        # ==================# END OF MAIN WIDGET LAYOUT #==================#

        # ==================+++++++++++++++++++++++++# FIRST SECTION #+++++++++++++++++++++++++==================#
        #==================# BUTTONS #==================#
        #TO BE REVIEWED BUTTON
        pushButtonUnreviewed = QtWidgets.QPushButton(self.widget)
        pushButtonUnreviewed.setText("In Progress")
        pushButtonUnreviewed.clicked.connect(self.on_pushButtonLoad_clicked)
        layout1.addWidget(pushButtonUnreviewed, 0, 0, 1, 1)
        # REVIEWED BUTTON
        pushButtonReviewed = QtWidgets.QPushButton(self.widget)
        pushButtonReviewed.setText("Reviewed")
        pushButtonReviewed.clicked.connect(self.on_pushButtonLoad_clicked)
        layout1.addWidget(pushButtonReviewed, 0, 1, 1, 1)
        #==================# END OF BUTTONS #==================#

        #==================# TABLE DATABASE #==================#
        filename = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_abnormal.csv")
        self.items = []
        self.fileName = filename
        self.on_pushButtonLoad_clicked
        self.model = QtGui.QStandardItemModel(self.widget)
        self.model.setHorizontalHeaderLabels(['Accession ID', 'Acc Date', 'First Name', 'Last Name', 'DOB', 'SSN', 'EOS %', 'LYM %','MON %', 'NEU %'])

        self.tableView = QTableView(self.widget)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 430)#id
        self.tableView.setColumnWidth(1, 160)#date
        self.tableView.setColumnWidth(2, 140)#first
        self.tableView.setColumnWidth(3, 140)#last
        self.tableView.setColumnWidth(4, 100)# DOB
        self.tableView.setColumnWidth(5, 110)# SSN
        self.tableView.setColumnWidth(6, 60)# E
        self.tableView.setColumnWidth(7, 60)# L
        self.tableView.setColumnWidth(8, 60)# M
        self.tableView.setColumnWidth(9, 60) # N

        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.model.rowsInserted.connect(lambda: QtCore.QTimer.singleShot(0, self.tableView.scrollToBottom))
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #layout1.addRow(self.tableView)
        layout1.addWidget(self.tableView, 1, 0, 1, 2)
        # ==================# END OF TABLE DATABASE #==================#


        # ==================+++++++++++++++++++++++++# SECOND SECTION #+++++++++++++++++++++++++==================#
        # ==================# VIEW IMAGE DATABASE #==================#

        #Qlineedit
        self.line_edit_viewImage = QLineEdit()
        self.line_edit_viewImage.setPlaceholderText('Enter Accession ID')
        self.line_edit_viewImage.mousePressEvent = lambda _: self.line_edit_viewImage.selectAll()
        layout2.addWidget(self.line_edit_viewImage, 0, 0, 1, 2)

        #view button
        viewImage_button = QPushButton('View Differential')
        viewImage_button.clicked.connect(self.button_find_image_clicked)
        #layout2.addRow(self.line_edit_viewImage, viewImage_button)
        layout2.addWidget(viewImage_button, 0, 2, 1, 1)

        #image box
        self.imageView = QLabel(self.widget)
        self.pixmap = QPixmap("background/image.png")
        self.imageView.setPixmap(self.pixmap)
        # scroller
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.imageView)
        #layout2.addRow(self.scroll)
        layout2.addWidget(self.scroll, 1, 0, 1, 3)

        # ==================# END VIEW IMAGE DATABASE #==================#

        # ==================+++++++++++++++++++++++++# THIRD SECTION #+++++++++++++++++++++++++==================#
        # ==================# BUTTONS #==================#


        # COMMENT BOX
        self.comment_text_edit = QPlainTextEdit()
        self.comment_text_edit.setPlaceholderText('Enter Pathologist Comments')
        #self.comment_text_edit.mousePressEvent = lambda _: self.comment_text_edit.selectAll()
        layout3.addWidget(self.comment_text_edit, 0, 0, 1, 1)

        # PATHOLOGIST REVIEW BUTTON
        button_path_review = QPushButton('Finalize Review')
        layout3.addWidget(button_path_review, 1, 0, 1, 1)



        # ==================# END OF BUTTONS #==================#






        ##LOGOUT BUTTON
        button_logout = QPushButton('Logout')
        button_logout.clicked.connect(self.logout_success)
        #layout2.addRow(button_logout)
        self.widget.layout().addWidget(button_logout, 3, 2)



    ######################   FUNCTIONS    ############################


    #===============# FIND IMAGE BUTTON  AND VIEW#===============#



    @QtCore.pyqtSlot()
    def button_find_image_clicked(self):
        # directory
        self.imageFolder = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/images/")
        self.classifiedImageList = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/images/{}").format(i) for
                                    i in os.listdir(self.imageFolder)]

        for imagepath in self.classifiedImageList:
            image = self.path_leaf(imagepath)
            editline = self.line_edit_viewImage.text() +".png"
            if image == editline:

                self.pixmap = QPixmap(self.imageFolder+editline)
                self.imageView.setPixmap(self.pixmap)
                # scroller
                #self.scroll = QtWidgets.QScrollArea(self.widget)
                #self.scroll.setWidget(self.imageView)
                #self.widget.layout().addWidget(self.scroll, 5, 1, 6, 2)
                print(self.imageFolder+editline)
                print("image is:",image)
                print("editline is:", editline)


    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)










    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

    def loadCsv(self, fileName):
        while (self.model.rowCount() > 0):
            self.model.removeRow(0)
        try:
            with open(fileName, "r") as fileInput:
                for row in csv.reader(fileInput):
                    self.items = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
                    self.model.appendRow(self.items)
        except:
            print("No Database")

    def logout_success(self):
        msg = QMessageBox()
        msg.setText('Logged out successful')
        msg.exec_()
        ## go to login screen
        self.close()

    @QtCore.pyqtSlot()
    def button_run_new_clicked(self):
        self.run_specimen()