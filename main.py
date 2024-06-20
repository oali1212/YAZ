import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from backend_functions import YAZ
from pre_login import PreLogin


os.chdir(os.path.dirname(__file__))

class Main():

    def __init__(self):



        self.app = QApplication(sys.argv)
        self.pre_login = PreLogin()
        self.pre_login.show()

        # self.pre_login.login_button.clicked.connect(self.start_login) # moves from pre login to login WITHOUT CONDITIONS



        
        
        yaz = YAZ() 

        required_files = [yaz.get_relink('users.bin'), yaz.get_relink('settings.ini'), yaz.get_relink('customers.ini')] 

        missing_files = [file for file in required_files if not os.path.exists(file)]
        if missing_files:
                QMessageBox.critical(None, "Missing Files", f"The following files are missing:\n\n{', '.join(missing_files)}\n\nPlease create them to use the application.")
                sys.exit(1)
        sys.exit(self.app.exec_())

main = Main()
main.start_login()



