import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pre_login import PreLogin




class Main():

    def __init__(self):

        
        self.app = QApplication(sys.argv)
        self.pre_login = PreLogin()
        self.pre_login.show()

        self.pre_login.login_button.clicked.connect(self.start_login) # moves from pre login to login WITHOUT CONDITIONS



        sys.exit(self.app.exec_())
        






    def back_to_home(self):
        self.home_page.showMaximized()

    
        
main = Main()
main.start_login()



