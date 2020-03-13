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
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QGridLayout())
        self.widget.layout().setContentsMargins(50, 50, 50, 50)
        self.widget.layout().setSpacing(5)
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
        # ==================# END OF MAIN WIDGET LAYOUT #==================#


        #==================# BUTTONS #==================#
        #RUN NEW SPECIMEN BUTTON
        button_run_new = QPushButton('Run New Specimen')
        button_run_new.clicked.connect(self.button_run_new_clicked)
        self.widget.layout().addWidget(button_run_new, 0, 0,1,1)

        # UPDATE DATABASE BUTTON
        pushButtonLoad = QtWidgets.QPushButton(self.widget)
        pushButtonLoad.setText("Update Database")
        pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
        self.widget.layout().addWidget(pushButtonLoad, 0, 1,1,1)

        #==================# END OF BUTTONS #==================#

        #==================# TABLE DATABASE #==================#
        filename = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/records/diff_records.csv")
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
        self.widget.layout().addWidget(self.tableView, 1, 0,1, 2)
        # ==================# END OF TABLE DATABASE #==================#


        # ==================# VIEW IMAGE DATABASE #==================#

        #Qlineedit
        self.line_edit_viewImage = QLineEdit()
        self.line_edit_viewImage.setPlaceholderText('Enter Accession ID')
        self.widget.layout().addWidget(self.line_edit_viewImage, 2, 0)
        self.line_edit_viewImage.mousePressEvent = lambda _: self.line_edit_viewImage.selectAll()

        #view button
        viewImage_button = QPushButton('View Differential')
        viewImage_button.clicked.connect(self.button_find_image_clicked)
        self.widget.layout().addWidget(viewImage_button, 2, 1)

        #image box
        self.imageView = QLabel(self.widget)
        self.pixmap = QPixmap("background/image.png")
        self.imageView.setPixmap(self.pixmap)
        # scroller
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.imageView)
        self.widget.layout().addWidget(self.scroll, 3, 0, 1, 2)

        # ==================# END VIEW IMAGE DATABASE #==================#

        ##LOGOUT BUTTON RUN NEW SPECIMEN BUTTON
        button_logout = QPushButton('Logout')
        button_logout.clicked.connect(self.logout_success)
        self.widget.layout().addWidget(button_logout, 4, 1)



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
    def button_run_new_clicked(self):
        self.run_specimen()

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
            from scripts.classify import classifier
            patientWBCimages1 = classifier(specinfo, test_imgs, self.app)
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
            try:                    #try this first if there is a file. if none, go to except
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

