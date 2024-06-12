import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pickle
from home_page import HomePage

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YAZ Lounge")
        self.setStyleSheet("background-color: #f5f5f5;")

        self.initUI()

        self.users = self.load_users()
        self.login_button.clicked.connect(self.start_home_page)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title Label
        title_label = QLabel("YAZ")
        title_label.setFont(QFont("Arial", 48))
        title_label.setStyleSheet("color: black;")
        title_label.setAlignment(Qt.AlignCenter)

        # Subtitle Label
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
        self.username_edit.setFixedWidth(300)
        self.username_edit.setFont(QFont("Arial", 14))
        self.username_edit.setStyleSheet("background-color: white;")

        # Password Label and LineEdit
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 14))
        password_label.setStyleSheet("color: black;")

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedHeight(30)
        self.password_edit.setFixedWidth(300)
        self.password_edit.setFont(QFont("Arial", 14))
        self.password_edit.setStyleSheet("background-color: white;")

        # Login Button
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("background-color: black; color: white; border: none; padding: 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; border-radius: 5px;")
        self.login_button.setFixedWidth(300)
        self.login_button.setFixedHeight(40)

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

    def wrong_password(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def load_users(self):
        try:
            with open('users.bin', 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}

    def start_home_page(self):
        login_status = self.login_check()
        if login_status == True:
            self.close()
            self.home_page = HomePage()
            self.home_page.showMaximized()
        elif login_status == -1:
            self.wrong_password("Username and/or password value(s) cannot be empty!")
        elif login_status == False:
            self.wrong_password("Incorrect username or password!")

    def validate_user(self, username, password):
        return self.users.get(username) == password

    def login_check(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if username == '' or password == '':
            return -1
        elif self.validate_user(username, password):
            return True
        else:
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showMaximized()
    sys.exit(app.exec_())
