#!/usr/bin/env python3
import csv
import numpy as np
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore

#######################################    CREATE ONE QAPPLICATION    #######################################
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
app = QApplication([])
start_again = False
initial_run = True
loginapp_open = False
docapp_open = False
tecapp_open = False
patapp_open = False

while True:

    if (start_again == True) or (initial_run == True):

        #======================# LOG IN #=======================#
        #if loginapp_open == True:
            #loginapp.close()
            #loginapp_open = False
        #if docapp_open == True:
            #docapp.close()
            #docapp_open = False
        #if patapp_open == True:
            #patapp.close()
            #patapp_open = False
        #if tecapp_open == True:
            #tecapp.close()
            #tecapp_open = False
        from scripts import hom_gui
        homapp,run = hom_gui.runit(app)
        #loginapp_open = True
        succ, usertype = homapp.login_button()
        #succ, usertype = homapp.login_button()
        if succ != True:
            print("Login Closed.. Quitting..")
            hom_gui.stop(run)
        else:
            print("Home GUI Closed")
            homapp.close()






        ############################################     RUN  TERMINALS    ######################################


        #======================# DOCTOR GUI #======================#
        #if loginapp_open == True:
            #loginapp.close()
        #if docapp_open == True:
            #docapp.close()
        #if patapp_open == True:
            #patapp.close()
        #if tecapp_open == True:
            #tecapp.close()
        if usertype == "Pathologist":
            print("Running Doctor Terminal")
            from scripts import doc_gui
            docapp, run = doc_gui.runit(app)
            #docapp_open = True


        #======================# PATIENT GUI #======================#
        #if loginapp_open == True:
            #loginapp.close()
        #if docapp_open == True:
            #docapp.close()
        #if patapp_open == True:
            #patapp.close()
        #if tecapp_open == True:
            #tecapp.close()
        if usertype == "Patient":
            print("Running Patient Terminal")
            from scripts import pat_gui
            patapp, run = pat_gui.runit(app)
            #patapp_open = True

        #======================# TECHNICIAN GUI #======================#
        #if loginapp_open == True:
            #loginapp.close()
        #if docapp_open == True:
            #docapp.close()
        #if patapp_open == True:
            #patapp.close()
        #if tecapp_open == True:
            #tecapp.close()
        if usertype == "Technician":
            print("Running Technician Terminal")
            from scripts import tec_gui
            tecapp, run = tec_gui.runit(app)
            #tecapp_open = True

            #if the wbc window is open
                #tecapp_open=False
                #loginapp





        initial_run = False
        start_again = True
        #### end of loop###