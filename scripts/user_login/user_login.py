import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,QInputDialog, QComboBox)

def runit():
    app = QApplication(sys.argv)
    form = LoginForm(app)
    form.show()
    run = app.exec_()
    return run
def stop(run):
    sys.exit(run)

class LoginForm(QWidget):
    def __init__(self,app):
        self.app =app
        super().__init__()
        self.setWindowTitle('User Login')
        self.resize(500, 120)

        layout = QGridLayout()

        label_name = QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        label_person = QLabel('<font size="4"> User Type </font>')
        self.combo_label_person = QComboBox()
        self.combo_label_person.addItem("Patient")
        self.combo_label_person.addItem("Doctor")
        self.combo_label_person.addItem("Technician")
        layout.addWidget(label_person, 2, 0)
        layout.addWidget(self.combo_label_person, 2, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        layout.addWidget(button_login, 3, 0, 1, 2)
        layout.setRowMinimumHeight(3, 75)
        print("Hello World!")
        self.setLayout(layout)
        #self.show()

    def check_password(self):
        msg = QMessageBox()

        if self.lineEdit_username.text() == 'Username' and self.lineEdit_password.text() == 'Password':
            msg.setText('Success')
            msg.exec_()
            self.app.quit()

        else:
            msg.setText('Incorrect Password')
            msg.exec_()



#if __name__ == '__main__':
	#app = QApplication(sys.argv)

	#form = LoginForm()
	#form.show()

	#sys.exit(app.exec_())