import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from configparser import *
from backend_functions import YAZ


class CustomersPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Customers Data")
        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color

        self.yaz = YAZ() 
        self.setting_file = "settings.ini"
        self.setting_file = self.yaz.get_relink(self.setting_file)
        self.config = ConfigParser()
        self.config.read(self.setting_file)

        main_layout = QVBoxLayout()

        # Top layout with buttons
        top_layout = QHBoxLayout()

        self.back_button = QPushButton("◀ Back")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("font-size: 14px;")        

        self.add_button = QPushButton("Add Client")
        self.save_button = QPushButton("Save All")

        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        top_layout.addWidget(self.add_button)
        top_layout.addWidget(self.save_button)

  
        main_layout.addLayout(top_layout)

        # Title
        title = QPushButton("Customers Data")
        title.setFixedSize(400, 50)
        title.setStyleSheet("background-color: #F5F5DC; color: black; font-size: 24px; font-weight: bold; border: none;")
        title.setEnabled(False)
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        self.customers_file  = "customers.ini"
        self.customers_file = self.yaz.get_relink(self.customers_file)
        # Table
        yaz = YAZ() 

        self.table = yaz.create_customers_table(self.customers_file)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.back_button.clicked.connect(self.back_to_home)
        self.add_button.clicked.connect(self.add_client)
        self.save_button.clicked.connect(self.save_all)




    def back_to_home(self):
        
        self.parent.showMaximized()
        self.close()
    def add_client(self):
        row_position = self.table.rowCount()
        # Add your code to handle adding a new client
        self.table.insertRow(self.table.rowCount())
        # Fill the new row with empty strings
        for column in range(self.table.columnCount()):
            self.table.setItem(row_position, column, QTableWidgetItem(""))


    def save_all(self):
        yaz = YAZ() 
        #print(self.clients_file)
        yaz.update_ini_from_table(self.table, self.customers_file)
        QMessageBox.information(None, "Success", "Customers saved successfully")


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = CustomersPage('')
#     window.show()
#     sys.exit(app.exec_())
