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
        self.widget.layout().setSpacing(10)
        self.setWindowTitle("Patient Results")
        #self.widget.layout().setColumnMinimumWidth(0, 50)
        #self.widget.layout().setColumnMinimumWidth(3, 50)
        #self.widget.layout().setRowMinimumHeight(0, 50)
        self.widget.layout().setRowMinimumHeight(1, 500)
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
        self.widget.layout().addWidget(self.GroupBox1, 0, 0, 3, 2)

        # Small group2
        self.GroupBox2 = QGroupBox()
        layout2 = QGridLayout()
        self.GroupBox2.setLayout(layout2)
        layout2.setSpacing(5)
        self.widget.layout().addWidget(self.GroupBox2, 0, 2, 3, 2)

        # Small group3 (in group box 2)
        self.GroupBox3 = QGroupBox()
        layout3 = QGridLayout()
        self.GroupBox3.setLayout(layout3)
        layout3.setContentsMargins(60, 10, 10, 10)
        layout3.setSpacing(5)
        layout2.addWidget(self.GroupBox3, 2, 0, 1, 3)
        self.GroupBox3.setStyleSheet("QGroupBox {background-image: url(background/image.png)}")

        # Small group4 (in group box 2)
        #self.GroupBox4 = QGroupBox()
        #layout4 = QGridLayout()
        #self.GroupBox4.setLayout(layout4)
        #layout4.setContentsMargins(60, 10, 10, 10)
        #layout4.setSpacing(5)
        #layout2.addWidget(self.GroupBox4, 2, 2, 1, 1)
        #self.GroupBox4.setStyleSheet("QGroupBox {background-image: url(background/image.png)}")




        #==================# LOGOUT BUTTON #==================#
        button_logout = QPushButton('Logout')
        button_logout.clicked.connect(self.logout_success)
        self.widget.layout().addWidget(button_logout, 3, 3, 1,1)

        # ==================# NORMAL AND ABNORMAL BUTTON #==================#
        # View Differential BUTTON
        #pushButtonNormalDiffs = QtWidgets.QPushButton(self.widget)
        #pushButtonNormalDiffs.setText("View Differential Results")
        # pushButtonNormalDiffs.clicked.setText(QColor.blue("Normal Results"))
        #pushButtonNormalDiffs.clicked.connect(self.on_pushButtonLoad_clicked4)
        #layout1.addWidget(pushButtonNormalDiffs, 0, 2, 1, 1)



        #==================# TABLE DATABASE #==================#

        filename2 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_outofrange.csv")
        self.fileName2 = filename2
        filename4 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_normal.csv")
        self.fileName4 = filename4
        filename5 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_abnormal.csv")
        self.fileName5 = filename5
        self.items_all = []
        #self.on_pushButtonLoad_clicked4




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
        self.tableView.setColumnWidth(0, 200)#id
        self.tableView.setColumnWidth(1, 150)#date
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
        self.tableView.setColumnHidden(2, True)
        self.tableView.setColumnHidden(3, True)
        self.tableView.setColumnHidden(4, True)
        self.tableView.setColumnHidden(5, True)
        self.tableView.setColumnHidden(6, True)
        self.tableView.setColumnHidden(7, True)
        self.tableView.setColumnHidden(8, True)
        self.tableView.setColumnHidden(9, True)
        self.tableView.setColumnHidden(10, False)


        #layout1.addRow(self.tableView)
        layout1.addWidget(self.tableView, 1, 0, 1, 4)

        #show table on login
        self.on_pushButtonLoad_clicked4()


        # ==================# EDIT AND VIEW BUTTON  #==================#

        # Qlineedit
        self.line_edit_viewImage = QLineEdit()
        self.line_edit_viewImage.setPlaceholderText('Enter Accession ID')
        self.line_edit_viewImage.mousePressEvent = lambda _: self.line_edit_viewImage.selectAll()
        layout2.addWidget(self.line_edit_viewImage, 0, 0, 1, 2)

        # view button
        viewImage_button = QPushButton('View Differential')
        viewImage_button.clicked.connect(self.button_find_specimen_clicked)
        # layout2.addRow(self.line_edit_viewImage, viewImage_button)
        layout2.addWidget(viewImage_button, 0, 2, 1, 1)
        # ==================# END EDIT AND VIEW BUTTON  #==================#

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
        layout3.addWidget(self.specimen_info_label, 0, 0, 1, 2)

        # ==================# END OF SPECIMEN INFO BOX #==================#

        # ==================# WBC RESULTS BOX #==================#
        #self.specimen_results_label = QLabel()
        #self.specimen_results_label.setAlignment(QtCore.Qt.AlignTop)
        #self.specimen_results_label.setText(
            #'\t'
            #'\n\t'
            #'\n\t'
            #'\n\t'
            #'\n\t'
            #'\n\t')
        #layout4.addWidget(self.specimen_results_label, 0, 0, 1, 2)
        # ==================# END OF WBC RESULTS BOX #==================#


    ##############################   FUNCTIONS   #########################

    # ==============# FUNCTION (VIEW DIFFERENTIAL RESULTS)#==============#
    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked4(self):
        self.loadCsv4(self.fileName2, self.fileName4, self.fileName5)

    def loadCsv4(self, fileName2, fileName4, fileName5):
        while (self.model.rowCount() > 0):
            self.model.removeRow(0)

        try:
            with open(fileName2, "r") as fileInput2:
                for row2 in csv.reader(fileInput2):
                    if self.firstname_info == row2[2] and self.lastname_info == row2[3]:
                        row2.append('PENDING')
                        self.items_all = [
                            QtGui.QStandardItem(field2)
                            for field2 in row2
                        ]
                        self.model.appendRow(self.items_all)

        except:
            print("No Out of range Database")

        try:
            with open(fileName4, "r") as fileInput4:
                for row4 in csv.reader(fileInput4):
                    if self.firstname_info == row4[2] and self.lastname_info == row4[3]:
                        self.items_all = [
                            QtGui.QStandardItem(field4)
                            for field4 in row4
                        ]
                        self.model.appendRow(self.items_all)
        except:
            print("No Normal Database")

        try:
            with open(fileName5, "r") as fileInput5:
                for row5 in csv.reader(fileInput5):
                    if self.firstname_info == row5[2] and self.lastname_info == row5[3]:
                        self.items_all = [
                            QtGui.QStandardItem(field5)
                            for field5 in row5
                        ]
                        self.model.appendRow(self.items_all)
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

    # ===============# FIND IMAGE BUTTON  AND VIEW#===============#

    @QtCore.pyqtSlot()
    def button_find_specimen_clicked(self):
        # show the specimen info and results
        editline = self.line_edit_viewImage.text()
        pat_text_format =  ('<p>'
                '<br/><b><h3>PATIENT INFORMATION</h3></b>'
                'Patient First Name &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{cc}'
                '<br/>Patient Last Name &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{dd}'
                '<br/>Date of Birth &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{ee}'
                '<br/>Social Security Number &nbsp; &nbsp; &nbsp; &nbsp;{ff}'
                '<br/>'
                '<br/><b><h3>SPECIMEN INFORMATION</h3></b>'
                'Accession ID &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{aa}'
                '<br/>Accession Date/Time &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{bb}'
                '<br/>'
                '<br/><h3><b>SPECIMEN RESULT</b></h3>'
                'INITIAL RESULT &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{kk}'
                '<br/>Eosinophil % &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{gg}'
                '<br/>Lymphocyte %  &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;{hh}'
                '<br/>Monocyte %  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{ii}'
                '<br/>Neutrophil %  &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{jj}'
                '<br/>'
                '<br/><b><h3>DOCTORS COMMENTS</h3></b>'
                '<html><body><pre style=font-family:Arial>{ll}</pre></body></html>'
                '</p>')

        ############## OUT OF RANGE ##################
        try:
            aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll = self.readCsvForSpecInfo(self.fileName2, editline)
            # show speciment info
            self.specimen_info_label.setText(
                    pat_text_format

                    .format(aa=aa, bb=bb, cc=cc, dd=dd, ee=ee, ff=ff, gg=gg, hh=hh, ii=ii, jj=jj, kk=kk, ll=ll))
            # show results
            #self.specimen_results_label.setText(
                #'Eosinophil %\t\t{gg}'
                #'\nLymphocyte %\t\t{hh}'
                #'\nMonocyte %\t\t{ii}'
                #'\nNeutrophil %\t\t{jj}'
                #'\n'
                #'\nINITIAL RESULT\t\t\t{kk}'
                #'\nDOCTORS COMMENTS\t\t\t{ll}'
                    #.format(gg=gg, hh=hh, ii=ii, jj=jj, kk=kk, ll=ll))
        except:
            print("Edit Line Empty for abnormal")





        ################ ABNORMAL ###################
        try:
            aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll = self.readCsvForSpecInfo(self.fileName5, editline)
            # show speciment info
            self.specimen_info_label.setText(pat_text_format
                    .format(aa=aa, bb=bb, cc=cc, dd=dd, ee=ee, ff=ff, gg=gg, hh=hh, ii=ii, jj=jj, kk=kk, ll=ll))
            # show results
            #self.specimen_results_label.setText(
                #'Eosinophil %\t\t{gg}'
                #'\nLymphocyte %\t\t{hh}'
                #'\nMonocyte %\t\t{ii}'
                #'\nNeutrophil %\t\t{jj}'
                #'\n'
                #'\nINITIAL RESULT\t\t\t{kk}'
                #'\nDOCTORS COMMENTS\t\t\t{ll}'
                    #.format(gg=gg, hh=hh, ii=ii, jj=jj, kk=kk, ll=ll))
        except:
            print("Edit Line Empty for abnormal")

        ################ NORMAL ###################
        try:
            aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll = self.readCsvForSpecInfo(self.fileName4, editline)
            # show speciment info
            self.specimen_info_label.setText(pat_text_format
                    .format(aa=aa, bb=bb, cc=cc, dd=dd, ee=ee, ff=ff, gg=gg, hh=hh, ii=ii, jj=jj, kk=kk, ll=ll))
            # show results
            #self.specimen_results_label.setText(
                #'Eosinophil %\t\t{gg}'
                #'\nLymphocyte %\t\t{hh}'
                #'\nMonocyte %\t\t{ii}'
                #'\nNeutrophil %\t\t{jj}'
                #'\n'
                #'\nINITIAL RESULT\t\t\t{kk}'
                #'\nDOCTORS COMMENTS\t\t\t{ll}'

                    #.format(gg=gg, hh=hh, ii=ii, jj=jj, kk=kk, ll=ll))
        except:
            print("Edit Line Empty for normal")
    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)
    def readCsvForSpecInfo(self, fileName, editline):
        try:
            with open(fileName, "r") as fileInput:
                for entry in csv.reader(fileInput):
                    print(entry[0])
                    print(editline)
                    if (entry[0]) == editline:
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
                        try:
                            ll = entry[11] #Comments
                        except:
                            ll = 'PENDING'

            return aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll
        except:
            print("Reading Specimen Info Failed")
    # ===============# LOAD CSV AND CHECK FOR THE LOGIN INFO#===============#