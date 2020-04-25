
"""
This script is the whole gui QMainWindow of the Doctor Terminal.
It includes :
    The out of range database (to be reviewed)
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
from PyQt5.QtCore import QItemSelectionModel
import sys
import os
import ntpath



import numpy as np
import re

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
        self.widget.layout().setContentsMargins(20, 20, 20, 20)
        self.widget.layout().setSpacing(5)
        self.setWindowTitle("Doctor Terminal")
        #self.widget.layout().setColumnMinimumWidth(0, 10)
        #self.widget.layout().setColumnMinimumWidth(1, 10)
        #self.widget.layout().setRowMinimumHeight(0, 10)
        #self.widget.layout().setRowMinimumHeight(2, 200)
        #self.widget.layout().setRowMinimumHeight(6, 10)
        self.showMaximized()
        #THEME COLOR
        self.setStyleSheet("QMainWindow {background-image: url(background/background.jpg)}")
        print("Doctor GUI Screen")

        #Small group1
        self.GroupBox1 = QGroupBox()
        layout1 = QGridLayout()
        self.GroupBox1.setLayout(layout1)
        layout1.setContentsMargins(5, 5, 5, 5)
        layout1.setSpacing(5)
        self.widget.layout().addWidget(self.GroupBox1, 0, 0,1,3)


        # Small group2
        self.GroupBox2 = QGroupBox()
        layout2 = QGridLayout()
        self.GroupBox2.setLayout(layout2)
        layout2.setContentsMargins(5, 5, 5, 5)
        layout2.setSpacing(5)
        layout2.setColumnStretch(0, 3)
        layout2.setColumnStretch(2,2)
        layout2.setColumnStretch(3, 1)
        layout2.setColumnStretch(4, 1)
        layout2.setRowStretch(1, 4)
        layout2.setRowStretch(2, 1)
        self.widget.layout().addWidget(self.GroupBox2, 1, 0,1,3)

        # Small group2a (in group box 2)
        self.GroupBox2a = QGroupBox()
        layout2a = QGridLayout()
        self.GroupBox2a.setLayout(layout2a)
        layout2a.setContentsMargins(60, 10, 10, 10)
        layout2a.setSpacing(5)
        layout2.addWidget(self.GroupBox2a, 2, 0, 2, 2)
        self.GroupBox2a.setStyleSheet("QGroupBox {background-color: white}")

        # Small group2b (in group box 2)
        self.GroupBox2b = QGroupBox()
        layout2b = QGridLayout()
        self.GroupBox2b.setLayout(layout2b)
        layout2b.setContentsMargins(60, 10, 10, 10)
        layout2b.setSpacing(5)
        layout2.addWidget(self.GroupBox2b, 2, 2, 2, 1)
        self.GroupBox2b.setStyleSheet("QGroupBox {background-image: url(background/image.png)}")


        # Small group3
        #self.GroupBox3 = QGroupBox()
        #layout3 = QGridLayout()
        #self.GroupBox3.setLayout(layout3)
        #layout3.setContentsMargins(5, 5, 5, 5)
        #layout3.setSpacing(5)
        #self.widget.layout().addWidget(self.GroupBox3, 2, 0, 1, 3)

        # ==================# END OF MAIN WIDGET LAYOUT #==================#

        # ==================+++++++++++++++++++++++++# FIRST SECTION #+++++++++++++++++++++++++==================#
        #==================# BUTTONS #==================#
        # TRUE NORMAL BUTTON
        pushButtonNormalDiffs = QtWidgets.QPushButton(self.widget)
        pushButtonNormalDiffs.setText("Normal")
        pushButtonNormalDiffs.clicked.connect(self.on_pushButtonLoad_clicked4)
        layout1.addWidget(pushButtonNormalDiffs, 0, 0, 1, 1)

        # TRUE ABNORMAL BUTTON
        pushButtonAbormalDiffs = QtWidgets.QPushButton(self.widget)
        pushButtonAbormalDiffs.setText("Abnormal")
        pushButtonAbormalDiffs.clicked.connect(self.on_pushButtonLoad_clicked5)
        layout1.addWidget(pushButtonAbormalDiffs, 0, 1, 1, 1)

        #TO BE REVIEWED BUTTON
        pushButtonUnreviewed = QtWidgets.QPushButton(self.widget)
        pushButtonUnreviewed.setText("In Progress")
        pushButtonUnreviewed.clicked.connect(self.on_pushButtonLoad_clicked2)
        layout1.addWidget(pushButtonUnreviewed, 0, 2, 1, 1)
        # REVIEWED BUTTON
        pushButtonReviewed = QtWidgets.QPushButton(self.widget)
        pushButtonReviewed.setText("Reviewed")
        pushButtonReviewed.clicked.connect(self.on_pushButtonLoad_clicked3)
        layout1.addWidget(pushButtonReviewed, 0, 3, 1, 1)
        #==================# END OF BUTTONS #==================#

        #==================# TABLE DATABASE #==================#
        filename = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_allruns.csv")
        self.items = []
        self.fileName = filename
        self.on_pushButtonLoad_clicked

        filename2 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_outofrange.csv")
        self.items2 = []
        self.fileName2 = filename2
        self.on_pushButtonLoad_clicked2

        filename3 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_reviewed.csv")
        self.items3 = []
        self.fileName3 = filename3
        self.on_pushButtonLoad_clicked3

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


        # set widths
        self.tableView.setColumnWidth(0, 325)  # id
        self.tableView.setColumnWidth(1, 200)  # date
        self.tableView.setColumnWidth(2, 120)  # first
        self.tableView.setColumnWidth(3, 120)  # last
        self.tableView.setColumnWidth(4, 120)  # DOB
        self.tableView.setColumnWidth(5, 120)  # SSN
        self.tableView.setColumnWidth(6, 60)  # E
        self.tableView.setColumnWidth(7, 60)  # L
        self.tableView.setColumnWidth(8, 60)  # M
        self.tableView.setColumnWidth(9, 60)  # N
        self.tableView.setColumnWidth(10, 150)  # Initial result

        #hide columns
        self.tableView.setColumnHidden(6, True)
        self.tableView.setColumnHidden(7, True)
        self.tableView.setColumnHidden(8, True)
        self.tableView.setColumnHidden(9, True)




        #add to layout
        layout1.addWidget(self.tableView, 1, 0, 1, 4)
        # ==================# END OF TABLE DATABASE #==================#


        # ==================+++++++++++++++++++++++++# SECOND SECTION #+++++++++++++++++++++++++==================#
        # ==================# VIEW SPECIMEN DATABASE #==================#

        #Qlineedit
        self.line_edit_viewImage = QLineEdit()
        self.line_edit_viewImage.setPlaceholderText('Enter Accession ID')
        self.line_edit_viewImage.mousePressEvent = lambda _: self.line_edit_viewImage.selectAll()
        layout2.addWidget(self.line_edit_viewImage, 0, 0, 1, 3)

        #view button
        viewImage_button = QPushButton('View Differential')
        viewImage_button.clicked.connect(self.button_find_specimen_clicked)
        #layout2.addRow(self.line_edit_viewImage, viewImage_button)
        layout2.addWidget(viewImage_button, 0, 3, 1, 2)

        #image box
        self.imageView = QLabel(self.widget)
        self.pixmap = QPixmap("background/image.png")
        self.imageView.setPixmap(self.pixmap)
        # scroller
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.imageView)
        #layout2.addRow(self.scroll)
        layout2.addWidget(self.scroll, 1, 0, 1, 5)

        # ==================# END VIEW IMAGE DATABASE #==================#

        # ==================# SPECIMEN INFO BOX #==================#
        self.specimen_info_label = QLabel()
        self.specimen_info_label.setAlignment(QtCore.Qt.AlignTop)
        self.specimen_info_label.setText(
            '\t'
            '\n\t'
            '\n\t'
            '\n\t'
            '\n\t'
            '\n\t')
        layout2a.addWidget(self.specimen_info_label, 0, 0, 1, 2)

        # ==================# END OF SPECIMEN INFO BOX #==================#

        # ==================# WBC RESULTS BOX #==================#
        self.specimen_results_label = QLabel()
        self.specimen_results_label.setAlignment(QtCore.Qt.AlignTop)
        self.specimen_results_label.setText(
            '\t'
            '\n\t'
            '\n\t'
            '\n\t'
            '\n\t'
            '\n\t')
        layout2b.addWidget(self.specimen_results_label, 0, 0, 1, 2)
        # ==================# END OF WBC RESULTS BOX #==================#


        # ==================# COMMENTX #==================#

        # COMMENT BOX
        self.comment_text_edit = QPlainTextEdit()
        self.comment_text_edit.setPlaceholderText('Enter Pathologist Comments')
        self.comment_text_edit.mousePressEvent = lambda _: self.comment_text_edit.selectAll()
        layout2.addWidget(self.comment_text_edit, 2, 3, 1, 2)

        # PATHOLOGIST NORMAL REVIEW BUTTON
        button_path_review_normal = QPushButton('Submit Review As Normal')
        button_path_review_normal.clicked.connect(self.button_path_review_clicked_normal)
        layout2.addWidget(button_path_review_normal, 3, 3, 1, 1)

        # PATHOLOGIST ABNORMAL REVIEW BUTTON
        button_path_review_abnormal = QPushButton('Submit Review As Abnormal')
        button_path_review_abnormal.clicked.connect(self.button_path_review_clicked_abnormal)
        layout2.addWidget(button_path_review_abnormal, 3, 4, 1, 1)

        # ==================# END OF COMMENTS #==================#

        # ==================+++++++++++++++++++++++++# THIRD SECTION #+++++++++++++++++++++++++==================#
        ##LOGOUT BUTTON
        button_logout = QPushButton('Logout')
        button_logout.clicked.connect(self.logout_success)
        #layout2.addRow(button_logout)
        self.widget.layout().addWidget(button_logout, 3, 2)



    ############################################   FUNCTIONS    ##################################################




    # ==============================# SUBMIT NORMAL OR ABNORMAL REVIEW FUNCTION#==============================#
    @QtCore.pyqtSlot()
    def button_path_review_clicked_normal(self):
        final_result = 'NORMAL\n\n'
        if str(self.comment_text_edit.toPlainText()) == '':
            msg = 'Empty comments'
            self.pop_up_msg(msg)
        else:
            msg = 'Saved to normal database'
            self.loadEntry(self.fileName2, self.fileName3, self.fileName4, msg, final_result)

    @QtCore.pyqtSlot()
    def button_path_review_clicked_abnormal(self):
        final_result = 'ABNORMAL\n\n'
        if str(self.comment_text_edit.toPlainText()) == '':
            msg = 'Empty comments'
            self.pop_up_msg(msg)
        else:
            msg = 'Saved to abnormal database'
            self.loadEntry(self.fileName2, self.fileName3, self.fileName5, msg, final_result)


    def loadEntry(self, fileName2, fileName3, fileName45, msg, final_result):
        # save results to csv files
        found = False
        try:  # try this first if there is a file. if none, go to except

            lines = list()
            with open(fileName3, 'a') as f3:  # output csv file
                writer3 = csv.writer(f3)
                with open(fileName45, 'a') as f45:  # output csv file
                    writer45 = csv.writer(f45)
                    with open(fileName2, 'r') as myfile:  # input csv file
                        reader = csv.reader(myfile, delimiter=',')
                        for entry in reader:
                            editline = self.line_edit_viewImage.text()
                            print(reader)
                            print("0", entry)
                            print("1", entry[0])
                            print("2", editline)
                            # move to the reviewed database
                            if entry[0] == editline:
                                row = entry
                                row.append(str(final_result + self.comment_text_edit.toPlainText()))
                                writer3.writerow(row)
                                writer45.writerow(row)
                                self.pop_up_msg(msg)
                                found = True
                            ### if the entry is not the editline, remove from the database since it was moved to the reviewed database
                            else:
                                lines.append(entry)


                        with open(fileName2, 'w') as writeFile:
                            writer2 = csv.writer(writeFile)
                            writer2.writerows(lines)
            self.comment_text_edit.clear()
            if found != True:
                msg = 'Enter a valid Accession ID from In Progress'
                self.pop_up_msg(msg)

        except IOError:
            print("No entry to review")



    def pop_up_msg(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.exec_()



    # ==============================# FIND IMAGE BUTTON  AND VIEW FUNCTION#==============================#
    @QtCore.pyqtSlot()
    def button_find_specimen_clicked(self):
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

        # show the specimen info and results
        try:
            aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk = self.readCsvForSpecInfo(self.fileName, editline)
            # show speciment info
            self.specimen_info_label.setText(
                'Accession ID\t\t\t{aa}'
                '\nAccession Date/Time\t\t{bb}'
                '\nPatient First Name\t\t{cc}'
                '\nPatient Last Name\t\t{dd}'
                '\nDate of Birth\t\t\t{ee}'
                '\nSocial Security Number\t\t{ff}'
                    .format(aa=aa, bb=bb, cc=cc, dd=dd, ee=ee, ff=ff, ))
            # show results
            self.specimen_results_label.setText(
                'Eosinophil %\t\t{gg}'
                '\nLymphocyte %\t\t{hh}'
                '\nMonocyte %\t\t{ii}'
                '\nNeutrophil %\t\t{jj}'
                '\n\t'
                '\nSTATUS\t\t{kk}'
                    .format(gg=gg, hh=hh, ii=ii, jj=jj, kk=kk))
        except:
            print("Edit Line Empty")

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    # ==============================# VIEW  DATABASES FUNCTION#==============================#
    # ==============# FUNCTION (ALL DIFFS)#==============#
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
            print("No All Differentials Database")

    # ==============# FUNCTION (IN PROGRESS)#==============#
    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked2(self):
        self.loadCsv2(self.fileName2)
    def loadCsv2(self, fileName):
        while (self.model.rowCount() > 0):
            self.model.removeRow(0)
        try:
            with open(fileName, "r") as fileInput:
                for row in csv.reader(fileInput):
                    self.items2 = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
                    self.model.appendRow(self.items2)
        except:
            print("No In Progress Database")

    # ==============# FUNCTION (REVIEWED)#==============#
    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked3(self):
        self.loadCsv3(self.fileName3)
    def loadCsv3(self, fileName):
        while (self.model.rowCount() > 0):
            self.model.removeRow(0)
        try:
            with open(fileName, "r") as fileInput:
                for row in csv.reader(fileInput):
                    self.items3 = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
                    self.model.appendRow(self.items3)
        except:
            print("No Reviewed Database")

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
                    self.items5 = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
                    self.model.appendRow(self.items5)
        except:
            print("No Abnormal Database")
    # ==============================# READ CSV FOR DISPLAY FUNCTION#==============================#
    def readCsvForSpecInfo(self, fileName, editline):
        try:
            with open(fileName, "r") as fileInput:
                for entry in csv.reader(fileInput):
                    print(entry[0])
                    print(editline)
                    if (entry[0]+".png") == editline:
                        aa = entry[0] #accID
                        bb = entry[1] #accDate
                        cc = entry[2] #FN
                        dd = entry[3] #LN
                        ee = entry[4] #DOB
                        ff = entry[5] #SSN
                        gg = entry[6] #E
                        hh = entry[7] #L
                        ii = entry[8] #M
                        jj = entry[9] #N
                        kk = entry[10] #Normality

            return aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk
        except:
            print("Reading Specimen Info Failed")




    # ==============================# LOGOUT FUNCTION#==============================#
    def logout_success(self):
        msg = QMessageBox()
        msg.setText('Logged out successful')
        msg.exec_()
        ## go to login screen
        self.close()

