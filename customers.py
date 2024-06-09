import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from configparser import ConfigParser
from backend_functions import YAZ

class CustomersPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Customers Data")
        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color

        self.config_file = 'customers.ini'
        self.config = ConfigParser()
        self.config.read(self.config_file)

        main_layout = QVBoxLayout()

        # Top layout with buttons
        top_layout = QHBoxLayout()

        self.back_button = QPushButton("◀ Back")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("font-size: 14px;")        

        self.add_button = QPushButton("Add Client")
        self.remove_button = QPushButton("Remove Client")
        self.edit_button = QPushButton("Edit Client")

        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        top_layout.addWidget(self.add_button)
        top_layout.addWidget(self.remove_button)
        top_layout.addWidget(self.edit_button)
  
        main_layout.addLayout(top_layout)

        # Title
        title = QPushButton("Customers Data")
        title.setFixedSize(400, 50)
        title.setStyleSheet("background-color: #F5F5DC; color: black; font-size: 24px; font-weight: bold; border: none;")
        title.setEnabled(False)
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        self.clients_file = "customers.ini"
        # Table
        yaz = YAZ() 

        self.table = yaz.create_customers_table(self.clients_file)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.back_button.clicked.connect(self.back_to_home)
        self.add_button.clicked.connect(self.add_client)
        self.remove_button.clicked.connect(self.remove_client)
        self.edit_button.clicked.connect(self.edit_client)



    def back_to_home(self):
        self.close()
        self.parent.showMaximized()

    def add_client(self):
        # Add your code to handle adding a new client
        pass

    def remove_client(self):
        # Add your code to handle removing a client
        pass

    def edit_client(self):
        # Add your code to handle editing a client
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomersPage('')
    window.show()
    sys.exit(app.exec_())
