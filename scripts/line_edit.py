

from PyQt5.QtWidgets import (QMainWindow, QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout,QMessageBox)
from PyQt5.QtGui import QPalette,QColor
from PyQt5 import QtWidgets
import sys

## DOB AND SSN CLASS FORMATS
class LineEditDOB(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent=parent)
        self.setPlaceholderText('MM/DD/YYYY')
    def focusInEvent(self, event):
        self.setInputMask('99/99/9999')

class LineEditSSN(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent=parent)
        self.setPlaceholderText('XXX-XX-XXXX')
    def focusInEvent(self, event):
        self.setInputMask('999-99-9999')

class LineEdit4SSN(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent=parent)
        self.setPlaceholderText('Last 4')
    def focusInEvent(self, event):
        self.setInputMask('9999')