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
                             QVBoxLayout,QMessageBox)
from PyQt5.QtGui import QPalette,QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
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
        ##the main widget layout
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QGridLayout())
        self.widget.layout().setContentsMargins(10, 10, 10, 10)
        self.widget.layout().setSpacing(0)
        self.setWindowTitle("Laboratory Technician Terminal")
        self.widget.layout().setColumnMinimumWidth(0, 50)
        self.widget.layout().setColumnMinimumWidth(5, 50)
        self.widget.layout().setRowMinimumHeight(0, 10)
        self.widget.layout().setRowMinimumHeight(6, 10)
        self.showMaximized()

        #THEME COLOR
        self.setStyleSheet("QMainWindow {background-image: url(background/background.jpg)}")
        print("Technician GUI Screen")

        ##LOGOUT BUTTON RUN NEW SPECIMEN BUTTON
        button_logout = QPushButton('Logout')
        button_logout.clicked.connect(self.logout_success)
        self.widget.layout().addWidget(button_logout, 2, 0)

        #RUN NEW SPECIMEN BUTTON
        button_run_new = QPushButton('Run New Specimen')
        button_run_new.clicked.connect(self.button_run_new_clicked)
        self.widget.layout().addWidget(button_run_new, 0, 0)

        # UPDATE DATABASE BUTTON
        pushButtonLoad = QtWidgets.QPushButton(self.widget)
        pushButtonLoad.setText("Update Database")
        pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
        self.widget.layout().addWidget(pushButtonLoad, 1, 0)


        #TABLE DATABASE

        filename = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records.csv")
        self.items = []
        self.fileName = filename
        self.on_pushButtonLoad_clicked
        self.model = QtGui.QStandardItemModel(self.widget)
        self.model.setHorizontalHeaderLabels(['Accession ID', 'Acc Date', 'Type', 'First Name', 'Last Name', 'DOB', 'SSN', 'EOS %', 'LYM %','MON %', 'NEU %'])

        self.tableView = QTableView(self.widget)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 160)#id
        self.tableView.setColumnWidth(1, 150)#date
        self.tableView.setColumnWidth(2, 100)#type
        self.tableView.setColumnWidth(3, 125)#first
        self.tableView.setColumnWidth(4, 125)#last
        self.tableView.setColumnWidth(5, 100)# DOB
        self.tableView.setColumnWidth(6, 100)# SSN
        self.tableView.setColumnWidth(7, 75)# E
        self.tableView.setColumnWidth(8, 75)# L
        self.tableView.setColumnWidth(9, 75)# M
        self.tableView.setColumnWidth(10, 75) # N
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.widget.layout().addWidget(self.tableView, 0, 1,0, 6)

    @QtCore.pyqtSlot()
    def button_run_new_clicked(self):
        self.run_specimen()

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

    def loadCsv(self, fileName):
        #self.tableView.clearSpans()
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


        if info_list[7] != True:
            print(info_list)
            print("Data Entry Closed")
            return False

        else:
            ### run the loading bar here
            accession, todays_datetime, specimen_type, first_name, last_name, date_of_birth, social_security = [str(info_list[i]) for i in (0, 1, 2, 3, 4, 5, 6)]
            specinfo = [accession, todays_datetime, specimen_type, first_name, last_name, date_of_birth, social_security]
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
            #================# PREDICT GIVEN IMAGES #================#
            print("Running WBC Differential...")
            from scripts.classify import patient_WBC_images
            patientWBCimages1 = patient_WBC_images(specinfo, test_imgs)
            specimen_info, specimen_fig, specimen_prediction  = patientWBCimages1.predict_images(numpred)
            #================# END OF PREDICT RESULTS  #================#




            #================# GENERATE SPECIMEN DIFFERENTIAL CLASS (the count for the WBC Differential)#================#
            from scripts.gen_diff import specimen_differential
            specimen1 = specimen_differential()
            diff_results = specimen1.generate_results(specimen_prediction)
            #================#END OFGENERATE SPECIMEN DIFFERENTIAL CLASS (the count for the WBC Differential)#================#




            #================# SAVE THE RECORD (RESULTS AND IMAGES) ON A DATABASE #================#
            #header = ["Accession ID","Accession Date/Time","Specimen Type","First Name","Last Name","Date of Birth (MM-DD-YYYY)","Social Security Number (XXX-XX-XXXX)","Eosinophils%","Lymphocytes%","Monocytes%","Neutrophils%"]
            row_results = specinfo + diff_results
            filename = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records.csv")
            #save results
            try:                    #try this first
                f = open(filename)
                with open(filename, 'a', newline='') as myfile:  # a means append, it will create a new file if it doesnt exist
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    wr.writerow(row_results)
                    print("\nPatient File Saved")
            except IOError:
                with open(filename, 'a', newline='') as myfile:  # a means append, it will create a new file if it doesnt exist
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    #wr.writerow(header)
                    wr.writerow(row_results)
                    print("\nPatient File Saved")
            #save the images based on unique id (accesson)
            specimen_fig.savefig(os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/images/"+str(accession)))
            #================# END OF SAVE THE RECORD (RESULTS AND IMAGES) ON A DATABASE   #================#
            saved = "yes"



        if saved == "yes":
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
