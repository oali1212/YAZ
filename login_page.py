import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from home_page import HomePage

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YAZ Lounge")
        self.setStyleSheet("background-color: #f5f5f5;")

        self.initUI()

        self.login_button.clicked.connect(self.start_home_page) # moves from loign to home after checking user & pass


    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title Label
        title_label = QLabel("YAZ")
        title_label.setFont(QFont("Arial", 48))
        title_label.setStyleSheet("color: black;")
        title_label.setAlignment(Qt.AlignCenter)

        # button 
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("background-color: black; color: white; border: none; padding: 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; border-radius: 5px;")
        self.login_button.setFixedWidth(300)
        self.login_button.setFixedHeight(40)

        subtitle_label = QLabel("Lounge")
        subtitle_label.setFont(QFont("Arial", 24))
        subtitle_label.setStyleSheet("color: black;")
        subtitle_label.setAlignment(Qt.AlignCenter)

        # Username Label and LineEdit
        username_label = QLabel("Username")
        username_label.setFont(QFont("Arial", 14))
        username_label.setStyleSheet("color: black;")

        self.username_edit = QLineEdit()
        self.username_edit.setFixedHeight(30)
        self.username_edit.setFixedWidth(300)  # تعيين العرض لمربعات النص
        self.username_edit.setFont(QFont("Arial", 14))
        self.username_edit.setStyleSheet("background-color: white;")

        # Password Label and LineEdit
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 14))
        password_label.setStyleSheet("color: black;")

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedHeight(30)
        self.password_edit.setFixedWidth(300)  # تعيين العرض لمربعات النص
        self.password_edit.setFont(QFont("Arial", 14))
        self.password_edit.setStyleSheet("background-color: white;")

        # Center the inputs
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(username_label)
        input_layout.addWidget(self.username_edit)
        input_layout.addWidget(password_label)
        input_layout.addWidget(self.password_edit)
        input_layout.addSpacing(20)
        input_layout.addWidget(self.login_button)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addLayout(input_layout)
        
    
        self.setLayout(layout)





    def wrong_password(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText("Username and/or password value(s) can not be empty!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def start_home_page(self):
        
        if self.login_check() == True: 
            self.close()
            self.home_page = HomePage()
            self.home_page.showMaximized()


        if self.login_check() == -1: 
            self.wrong_password()

    # check login function
    def login_check(self):
        self.username = self.username_edit.text()
        self.password = self.password_edit.text()

        if self.username == '' or self.password == '': 
            return -1
        
        else: 

            return True
           



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showMaximized()  # عرض النافذة بحجم الشاشة بالكامل
    sys.exit(app.exec_())
