"""
This script is the whole gui QMainWindow of the Technician Terminal.
It includes :
    the layout (columns and rows)
    Logout button
    Run new specimen button
For running the new specimen:
    take the data entered in the Qdialog window using runnew_data.py
    generate the counts using another script using gen_diff.py
    save it in a database
    and run the visual of the results
"""



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



import numpy as np

def runit(app):

    gui = technician_gui(app)
    run = app.exec_()
    return gui, run

def stop(run):
    sys.exit(run)

class technician_gui(QMainWindow):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self,app):
        self.app = app
        super(technician_gui, self).__init__()
        #==================# MAIN WIDGET LAYOUT #==================#
        #Big window


        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QGridLayout())
        self.widget.layout().setContentsMargins(40, 40, 40, 40)
        self.widget.layout().setSpacing(10)
        self.setWindowTitle("Laboratory Technician Terminal")
        #self.widget.layout().setColumnMinimumWidth(0, 10)
        #self.widget.layout().setColumnMinimumWidth(1, 10)
        #self.widget.layout().setRowMinimumHeight(0, 10)
        #self.widget.layout().setRowMinimumHeight(2, 200)
        #self.widget.layout().setRowMinimumHeight(6, 10)
        self.showMaximized()
        #THEME COLOR
        self.setStyleSheet("QMainWindow {background-image: url(background/background.jpg)}")
        print("Technician GUI Screen")

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

        # Small group3 (in group box 2)
        self.GroupBox3 = QGroupBox()
        layout3 = QGridLayout()
        self.GroupBox3.setLayout(layout3)
        layout3.setContentsMargins(60, 10, 10, 10)
        layout3.setSpacing(5)
        layout2.addWidget(self.GroupBox3, 2, 0, 1, 2)
        self.GroupBox3.setStyleSheet("QGroupBox {background-image: url(background/image.png)}")

        # Small group4 (in group box 2)
        self.GroupBox4 = QGroupBox()
        layout4 = QGridLayout()
        self.GroupBox4.setLayout(layout4)
        layout4.setContentsMargins(60, 10, 10, 10)
        layout4.setSpacing(5)
        layout2.addWidget(self.GroupBox4, 2, 2, 1, 1)
        self.GroupBox4.setStyleSheet("QGroupBox {background-image: url(background/image.png)}")

        # ==================# END OF MAIN WIDGET LAYOUT #==================#



        #==================# BUTTONS #==================#

        #RUN NEW SPECIMEN BUTTON
        button_run_new = QPushButton('Run New Specimen')
        button_run_new.clicked.connect(self.button_run_new_clicked)
        #layout1.addRow(button_run_new)
        layout1.addWidget(button_run_new, 0, 0, 1, 1)

        # UPDATE DATABASE BUTTON
        pushButtonLoad = QtWidgets.QPushButton(self.widget)
        pushButtonLoad.setText("View All Runs")
        pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
        #layout1.addRow(button_run_new, pushButtonLoad)
        layout1.addWidget(pushButtonLoad, 0, 1, 1, 1)

        # TRUE NORMAL BUTTON
        pushButtonNormalDiffs = QtWidgets.QPushButton(self.widget)
        pushButtonNormalDiffs.setText("Normal")
        #pushButtonNormalDiffs.clicked.setText(QColor.blue("Normal Results"))
        pushButtonNormalDiffs.clicked.connect(self.on_pushButtonLoad_clicked4)
        layout1.addWidget(pushButtonNormalDiffs, 0, 2, 1, 1)

        # TRUE ABNORMAL BUTTON
        pushButtonAbnormalDiffs = QtWidgets.QPushButton(self.widget)
        pushButtonAbnormalDiffs.setText("Abnormal")
        pushButtonAbnormalDiffs.clicked.connect(self.on_pushButtonLoad_clicked5)
        layout1.addWidget(pushButtonAbnormalDiffs, 0, 3, 1, 1)

        #==================# END OF BUTTONS #==================#

        #==================# TABLE DATABASE #==================#
        filename = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_allruns.csv")
        self.items = []
        self.fileName = filename
        self.on_pushButtonLoad_clicked

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
        # ==================# END OF TABLE DATABASE #==================#


        # ==================# VIEW IMAGE DATABASE #==================#

        #Qlineedit
        self.line_edit_viewImage = QLineEdit()
        self.line_edit_viewImage.setPlaceholderText('Enter Accession ID')
        self.line_edit_viewImage.mousePressEvent = lambda _: self.line_edit_viewImage.selectAll()
        layout2.addWidget(self.line_edit_viewImage, 0, 0, 1,2)

        #view button
        viewImage_button = QPushButton('View Differential')
        viewImage_button.clicked.connect(self.button_find_specimen_clicked)
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
        self.specimen_results_label = QLabel()
        self.specimen_results_label.setAlignment(QtCore.Qt.AlignTop)
        self.specimen_results_label.setText(
            '\t'
            '\n\t'
            '\n\t'
            '\n\t'
            '\n\t'
            '\n\t')
        layout4.addWidget(self.specimen_results_label, 0, 0, 1, 2)
        # ==================# END OF WBC RESULTS BOX #==================#

        ##LOGOUT BUTTON
        button_logout = QPushButton('Logout')
        button_logout.clicked.connect(self.logout_success)
        #layout2.addRow(button_logout)
        self.widget.layout().addWidget(button_logout, 2, 2)



    ###########################################   FUNCTIONS    ######################################################################


    #===============# FIND IMAGE BUTTON  AND VIEW#===============#
    @QtCore.pyqtSlot()
    def button_find_specimen_clicked(self):
        # directory
        self.imageFolder = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/images/")
        self.classifiedImageList = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/images/{}").format(i) for
                                    i in os.listdir(self.imageFolder)]
        #show the images
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
            #show speciment info
            self.specimen_info_label.setText(
                'Accession ID\t\t\t{aa}'
                '\nAccession Date/Time\t\t{bb}'
                '\nPatient First Name\t\t{cc}'
                '\nPatient Last Name\t\t{dd}'
                '\nDate of Birth\t\t\t{ee}'
                '\nSocial Security Number\t\t{ff}'
                    .format(aa=aa, bb=bb, cc=cc, dd=dd, ee=ee, ff=ff, ))
            #show results
            self.specimen_results_label.setText(
                'Eosinophil %\t\t{gg}'
                '\nLymphocyte %\t\t{hh}'
                '\nMonocyte %\t\t{ii}'
                '\nNeutrophil %\t\t{jj}'
                '\n'
                '\nRESULT\t\t\t{kk}'
                    .format(gg=gg, hh=hh, ii=ii, jj=jj, kk=kk))
        except:
            print("Edit Line Empty")


    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

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

    # ===============# VIEW ALL RUNS #===============#
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



    # ===============# LOGOUT BUTTONM#===============#
    def logout_success(self):
        msg = QMessageBox()
        msg.setText('Logged out successful')
        msg.exec_()
        ## go to login screen
        self.close()



    # ===============# RUN NEW SPECIMEN#===============#
    @QtCore.pyqtSlot()
    def button_run_new_clicked(self):
        self.run_specimen()

    def run_specimen(self):

        ####### DATA ENTRY ########
        # Inputs
        try:
            self.running_wbc_gui.close()
        except:
            print("WBC GUI is not running")
        from scripts import runnew_data
        info_list, running = runnew_data.runit(self.app)
        running.close()
        running.reject()


        if info_list[6] != True:
            print(info_list)
            print("Data Entry Closed")
            return False

        else:
            ### run the loading bar here
            accession, todays_datetime, first_name, last_name, date_of_birth, social_security = [str(info_list[i]) for i in (0, 1, 2, 3, 4, 5)]
            specinfo = [accession, todays_datetime, first_name, last_name, date_of_birth, social_security]
            specimen_images = []  # location of image to have a diff performed
            # give specimen image location
            test_dir = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/sample_specimen1")
            test_imgs = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/sample_specimen1/{}").format(i) for i in
                         os.listdir(test_dir)]
            numpred = 100  # number to predivt or output in the screen has to be divisible by 10
            dataentry = "success"

        ########## END OF DATA ENTRY ###############




        if dataentry == "success":


        ####### PREDICT RESULTS, GENERATE COUNTS, SAVE IN DATABASE,  AND RUN APPLICATION ###########
            #================# PREDICT GIVEN IMAGES  AND RUN THE LOAD BAR#================#
            print("Running WBC Differential...")
            #from scripts import wait_animate
            #waitapp, run = wait_animate.runit(self.app)
            #waitapp.show()
            #print("line1")
            from scripts.classify import classifier
            #print("line2")
            patientWBCimages1 = classifier(specinfo, test_imgs)
            specimen_info, specimen_fig, specimen_prediction  = patientWBCimages1.predict_images(numpred)
            #print("line3")
            #waitapp.close()
            #================# END OF PREDICT RESULTS  #================#




            #================# GENERATE SPECIMEN DIFFERENTIAL CLASS (the count for the WBC Differential)#================#
            from scripts.gen_diff import specimen_differential
            specimen1 = specimen_differential()
            diff_results, flagged_result = specimen1.generate_results(specimen_prediction)
            #================#END OFGENERATE SPECIMEN DIFFERENTIAL CLASS (the count for the WBC Differential)#================#




            #================# SAVE THE RECORD (RESULTS AND IMAGES) ON A DATABASE #================#
            #header = ["Accession ID","Accession Date/Time","Specimen Type","First Name","Last Name","Date of Birth (MM-DD-YYYY)","Social Security Number (XXX-XX-XXXX)","Eosinophils%","Lymphocytes%","Monocytes%","Neutrophils%"]
            row_results = specinfo + diff_results
            filename = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_allruns.csv")
            filename2 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_outofrange.csv")
            filename4 = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records_normal.csv")
            #save results to csv files
            try:                    #try this first if there is a file. if none, go to except
                with open(filename, 'a', newline='') as myfile:  # a means append, it will create a new file if it doesnt exist
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    wr.writerow(row_results)
                    print("\nPatient File Saved in All Runs Database (Initial Run)")
            except IOError:
                with open(filename, 'a', newline='') as myfile:  # a means append, it will create a new file if it doesnt exist
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    #wr.writerow(header)
                    wr.writerow(row_results)
                    print("\nPatient File Saved in All Runs Database (Initial Run)")

            # save results here if flagged result is OUT OF RANGE
            if flagged_result == "OUT OF RANGE":
                try:  # try this first if there is a file. if none, go to except
                    with open(filename2, 'a',
                              newline='') as myfile2:  # a means append, it will create a new file if it doesnt exist
                        wr2 = csv.writer(myfile2, quoting=csv.QUOTE_ALL)
                        wr2.writerow(row_results)
                        print("\nPatient File Saved in Out of Range Database")
                except IOError:
                    with open(filename2, 'a',
                              newline='') as myfile2:  # a means append, it will create a new file if it doesnt exist
                        wr2 = csv.writer(myfile2, quoting=csv.QUOTE_ALL)
                        #wr2.writerow(header)
                        wr2.writerow(row_results)
                        print("\nPatient File Saved in Out of Range Database")
            # save results here if flagged result is NORMAL
            else:
                try:  # try this first if there is a file. if none, go to except
                    with open(filename4, 'a',
                              newline='') as myfile4:  # a means append, it will create a new file if it doesnt exist
                        wr4 = csv.writer(myfile4, quoting=csv.QUOTE_ALL)
                        wr4.writerow(row_results)
                        print("\nPatient File Saved in Normal Database")
                except IOError:
                    with open(filename4, 'a',
                              newline='') as myfile2:  # a means append, it will create a new file if it doesnt exist
                        wr4 = csv.writer(myfile4, quoting=csv.QUOTE_ALL)
                        # wr2.writerow(header)
                        wr4.writerow(row_results)
                        print("\nPatient File Saved in Normal Database")

            #save the images based on unique id (accesson)
            specimen_fig.savefig(os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/images/"+str(accession)))
            #================# END OF SAVE THE RECORD (RESULTS AND IMAGES) ON A DATABASE   #================#
            saved = "yes"
            msg_box = QMessageBox()
            msg_box.setText('Auto Differential Complete')
            msg_box.exec_()



############### ========================= UNUSED EXTRA WINDOW ========================= ##################
        if saved == "yesno":
            #================#   RUN THE APPLICATION FOR VIEWING   #================#
            ## Call class for another WBC_GUI file (Will view everything)
            #includes images with subplots
            #includes generated wbc differetial results
            from scripts import tec_newrunresult
            #fig.savefig('test.png')#save the result into a picture
            self.running_wbc_gui = tec_newrunresult.runit(specimen_info, specimen_fig, diff_results, self.app)
            #running.close()
            #diff_result(specimen_info, specimen_fig, diff_results, self.app)#show info,predictions of image subplots (fig), and numeric diff results on window
            #================#  END OF RUN THE APPLICATION FOR VIEWING  #================#

