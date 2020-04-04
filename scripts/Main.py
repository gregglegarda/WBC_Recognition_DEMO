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
        from scripts import hom_gui
        homapp, run = hom_gui.runit(app)

        #medical personell
        succ, usertype = homapp.login_button()

        #patient
        #succ, usertype = homapp.login_button2()

        if succ != True:
            print("Login Closed.. Quitting..")
            hom_gui.stop(run)
        else:
            print("Home GUI Closed")
            homapp.close()


        #############################  IF LOGIN SUCCESSFUL  RUN  TERMINALS    #########################

        #======================# DOCTOR GUI #======================#
        if usertype == "Doctor":
            print("Running Doctor Terminal")
            from scripts import doc_gui
            docapp, run = doc_gui.runit(app)

        #======================# PATIENT GUI #======================#
        if usertype == "Patient":
            print("Running Patient Terminal")
            from scripts import pat_gui
            patapp, run = pat_gui.runit(app)

        #======================# TECHNICIAN GUI #======================#
        if usertype == "Technician":
            print("Running Technician Terminal")
            from scripts import tec_gui
            tecapp, run = tec_gui.runit(app)

            #if the wbc window is open
                #tecapp_open=False
                #loginapp

        initial_run = False
        start_again = True
        #### end of loop###