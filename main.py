import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pre_login import PreLogin
from login_page import LoginWindow
from home_page import HomePage
from reports import ReportsPage
from customers import CustomersPage
from setting import SettingsPage
from services import ServicesPage


class Main():

    def __init__(self):

        
        self.app = QApplication(sys.argv)
        self.pre_login = PreLogin()
        self.pre_login.show()

        self.pre_login.login_button.clicked.connect(self.start_login) # moves from pre login to login WITHOUT CONDITIONS



        sys.exit(self.app.exec_())
        

    # Transit from pre login to login 
    def start_login(self):

        self.pre_login.close()
        self.login = LoginWindow() 
        self.login.showMaximized()

        self.login.login_button.clicked.connect(self.start_home_page) # moves from loign to home after checking user & pass

    # check login function
    def login_check(self):
        self.username = self.login.username_edit.text()
        self.password = self.login.password_edit.text()

        if self.username == '' or self.password == '': 
            return -1
        
        else: 

            return True


    def wrong_password(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText("Username and/or password value(s) can not be empty!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def start_home_page(self):
        self.login.close()
        if self.login_check() == True: 
            self.home_page = HomePage()
            self.home_page.showMaximized()

            ### bindings 
            self.home_page.services_button.clicked.connect(self.start_services_page)
            self.home_page.reports_button.clicked.connect(self.start_reports_page)
            self.home_page.customers_button.clicked.connect(self.start_customers_page)
            self.home_page.settings_button.clicked.connect(self.start_settings_page)

        if self.login_check() == -1: 
            self.wrong_password()
    
    def start_services_page(self):
        self.home_page.close()
        self.services_page = ServicesPage()
        self.services_page.showMaximized()

    def start_reports_page(self):
        self.home_page.close()
        self.reports_page = ReportsPage()
        self.reports_page.showMaximized() 

    def start_customers_page(self):
        self.home_page.close()
        self.customers_page = CustomersPage() 
        self.customers_page.showMaximized() 

    def start_settings_page(self):
        self.home_page.close()
        self.settings_page = SettingsPage() 
        self.settings_page.showMaximized() 

    def back_to_home(self):
        self.home_page.showMaximized()

    
        
main = Main()
main.start_login()



