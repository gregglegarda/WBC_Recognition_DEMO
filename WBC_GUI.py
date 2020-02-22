
#SCROLLABLE WINDOW CLASS
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtGui import QPalette,QColor
from PyQt5 import QtCore
from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



class ScrollableWindow(QtWidgets.QMainWindow):
    ## label results

    def __init__(self, info, fig, results):
        self.qapp = QtWidgets.QApplication([])
        QtWidgets.QMainWindow.__init__(self)

        ##the main window
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        #box widget below main
        self.widget2=QtWidgets.QWidget()
        self.widget2.setLayout(QtWidgets.QHBoxLayout())
        self.widget2.layout().setContentsMargins(0,0,0,30)
        self.widget2.layout().setSpacing(0)

        #hte image figure plots of the wbcs
        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()

        # scroller
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        #toolbar
        #self.nav = NavigationToolbar(self.canvas, self.widget)

        #tab initialize layout
        self.layout = QHBoxLayout()
        self.layout2 = QHBoxLayout()

        #Qlabel results Calculations
        self.results = results
        e, l, m, n = [str(results[i]) for i in (0,1,2,3)]
        totals = int(e)+ int(l)+ int(m)+ int(n)
        ep, lp, mp, np = [str(round((results[i]/totals*100),2)) for i in (0,1,2,3)]

        #flag values
        Flag_eos = ""
        Flag_lym = ""
        Flag_mon = ""
        Flag_neu = ""

        #normal ranges of wbc
        ep_ref_range_H = 6
        ep_ref_range_L = 0
        lp_ref_range_H = 45
        lp_ref_range_L = 20
        mp_ref_range_H = 10
        mp_ref_range_L = 0
        np_ref_range_H = 75
        np_ref_range_L = 30

        # normal or abnormal
        normality = "\n\tOverall Differential Result is NORMAL. No action needed."
        abnormality = []
        if float(np) > np_ref_range_H or float(np) < np_ref_range_L:
            if float(np) > np_ref_range_H:
                Flag_neu = "H"
            else:
                Flag_neu = "L"
            normality = "\n\tOVERALL DIFFERENTIAL RESULT IS ABNORMAL!!! PLEASE RERUN"
            abnormality.append("Neutrophil")

        if float(lp) > lp_ref_range_H or float(lp) < lp_ref_range_L:
            if float(lp) > lp_ref_range_H:
                Flag_lym = "H"
            else:
                Flag_lym = "L"
            normality = "\n\tOVERALL DIFFERENTIAL RESULT IS ABNORMAL!!! PLEASE RERUN"
            abnormality.append("Lymphocyte")

        if float(mp) > mp_ref_range_H or float(mp) < mp_ref_range_L:
            if float(mp) > mp_ref_range_H:
                Flag_mon = "H"
            else:
                Flag_mon = "L"
            normality = "\n\tOVERALL DIFFERENTIAL RESULT IS ABNORMAL!!! PLEASE RERUN"
            abnormality.append("Monocyte")

        if float(ep) > ep_ref_range_H or float(ep) < ep_ref_range_L:
            if float(ep) > ep_ref_range_H:
                Flag_eos = "H"
            else:
                Flag_eos = "L"
            normality = "\n\tOVERALL DIFFERENTIAL RESULT IS ABNORMAL!!! PLEASE RERUN"
            abnormality.append("Eosinophil")

        # specimen info.... add self later to pas it in
        # self.specimen_info = info
        aa, bb, cc, dd, ee, ff, gg = [info[j] for j in (0, 1, 2, 3, 4, 5, 6)]
        self.specimen_info = QLabel()
        self.specimen_info.setAlignment(QtCore.Qt.AlignTop)
        self.specimen_info.setStyleSheet("QLabel {background-color: #25211f; color: white}")
        self.specimen_info.setText(
            '\n-----------------------------------------------------------------------------------------------'
            '\n\t\tSPECIMEN INFORMATION'
            '\n-----------------------------------------------------------------------------------------------'
            '\n\tSpecimen Accesion Number\t{aa}'
            '\n\tAccession Date/Time\t\t{bb}'
            '\n\tSpecimen Type\t\t\t{cc}'
            '\n\tPatient First Name\t\t{dd}'
            '\n\tPatient Last Name\t\t{ee}'
            '\n\tDate of Birth\t\t\t{ff}'
            '\n\tSocial Security Number\t\t{gg}'
            .format(aa=aa, bb=bb, cc=cc, dd=dd, ee=ee, ff=ff, gg=gg))




        #percent part
        self.percent = QLabel()
        self.percent.setAlignment(QtCore.Qt.AlignTop)
        self.percent.setStyleSheet("QLabel {background-color: #25211f; color: white}")
        self.percent.setText('\n-----------------------------------------------------------------------------------------------'
                            '\n\t\tWBC DIFERRENTIAL RESULTS (PERCENTAGE)'
                            '\n-----------------------------------------------------------------------------------------------'
                            '\n\tWBC Percent\t\tReference Range\t\tResult/Flags'
                            '\n\tNeutrophil Count\t\t(30-75%)\t\t{np}%  {fn}'
                            '\n\tLymphocyte Count\t(20-45%)\t\t{lp}%  {fl}'
                            '\n\tMonocyte Count\t\t(0-10%)\t\t\t{mp}%  {fm}'
                            '\n\tEosinophil Count\t\t(0-6%)\t\t\t{ep}%  {fe}'
                            .format(ep=ep, lp=lp, mp=mp, np=np,fl = Flag_lym,fm = Flag_mon,fn = Flag_neu,fe = Flag_eos ))


        # Morphology part
        self.morph = QLabel()
        self.morph.setAlignment(QtCore.Qt.AlignTop)
        self.morph.setStyleSheet("QLabel {background-color: #25211f; color: white}")
        self.morph.setText(
            '\n-----------------------------------------------------------------------------------------------'
            '\n\t\tMORPHOLOGY RESULTS'
            '\n-----------------------------------------------------------------------------------------------'
            '\n\tPlatelets\t\t\t{n}'
            '\n\tRBC Morphology\t\t{m}'
            '\n\tNRBCs\t\t\t{l}'
            '\n\tATL Lymphs \t\t{e}'
            .format(e=e, l=l, m=m, n=n))




        #Normality part
        self.normality = QLabel()
        self.normality.setAlignment(QtCore.Qt.AlignTop)
        self.normality.setStyleSheet("QLabel {background-color: #25211f; color: white}")
        self.normality.setText('\n-----------------------------------------------------------------------------------------------'
                            '\n\t\tDIFFERENTIAL CONCLUSION'
                            '\n-----------------------------------------------------------------------------------------------'
                            '{normality}'
                            '\n\tOUT OF RANGE VALUES\t{abnormality}'
                            .format(normality=normality,abnormality=abnormality))


        #Tab part add content to tabs 1
        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(self.specimen_info, "Specimen Info")

        #Tab part add content to tabs 2
        self.tabwidget2 = QTabWidget()
        self.tabwidget2.addTab(self.percent, "WBC Differential")
        self.tabwidget2.addTab(self.morph, "Morphology")
        self.tabwidget2.addTab(self.normality, "Conclusion")


        #add tab widget to 2nd widget
        self.widget2.layout().addWidget(self.tabwidget)
        self.widget2.layout().addWidget(self.tabwidget2)
        

        #add the all  items to main widget
        #self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)
        self.widget.layout().addWidget(self.widget2)



        self.setWindowTitle("WBC Classifier")
        self.showMaximized()


        #THEME COLOR
        self.palette = self.palette()
        self.palette.setColor(QPalette.Window, QColor("#25211f"))
        #self.palette.setColor(QPalette.Button, QColor('red'))
        self.setPalette(self.palette)


        self.show()
        exit(self.qapp.exec_())
#END OF SCROLLABLE WINDOW CLASS