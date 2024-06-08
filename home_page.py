import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize


from reports import ReportsPage
from customers import CustomersPage
from setting import SettingsPage
from services import ServicesPage


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setStyleSheet("background-color: #f4f1ea;")

        self.initUI()

    
        # ### bindings 
        self.services_button.clicked.connect(self.start_services_page)
        self.reports_button.clicked.connect(self.start_reports_page)
        self.customers_button.clicked.connect(self.start_customers_page)
        self.settings_button.clicked.connect(self.start_settings_page)
    
    def initUI(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)

        # Grid Layout for buttons with images and text
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)  # Adjust spacing between buttons

        # Button 1
        self.services_button = QPushButton()
        self.services_button.setIcon(QIcon(".//img//Services.png"))
        self.services_button.setIconSize(QSize(400, 150))
        self.services_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                border-radius: 20px;
                background-color: rgba(0, 0, 0, 50%);
            }
        """)
        self.services_button.setText("Services")
        self.services_button.setFont(QFont("Arial", 15, QFont.Bold))
        self.services_button.setCursor(Qt.PointingHandCursor)
        grid_layout.addWidget(self.services_button, 0, 0)

        # Button 2
        self.reports_button = QPushButton()
        self.reports_button.setIcon(QIcon(".//img//Reports.png"))
        self.reports_button.setIconSize(QSize(400, 150))
        self.reports_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                border-radius: 20px;
                background-color: rgba(0, 0, 0, 50%);
            }
        """)
        self.reports_button.setText("Reports")
        self.reports_button.setFont(QFont("Arial", 15, QFont.Bold))
        self.reports_button.setCursor(Qt.PointingHandCursor)
        grid_layout.addWidget(self.reports_button, 0, 2)

        # Button 3
        self.customers_button = QPushButton()
        self.customers_button.setIcon(QIcon(".//img//Customers Data.png"))
        self.customers_button.setIconSize(QSize(400, 150))
        self.customers_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                border-radius: 20px;
                background-color: rgba(0, 0, 0, 50%);
            }
        """)
        self.customers_button.setText("Customers")
        self.customers_button.setFont(QFont("Arial", 15, QFont.Bold))
        self.customers_button.setCursor(Qt.PointingHandCursor)
        grid_layout.addWidget(self.customers_button, 1, 0)

        # Button 4
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(".//img//setting.png"))
        self.settings_button.setIconSize(QSize(400, 150))
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                border-radius: 20px;
                background-color: rgba(0, 0, 0, 50%);
            }
        """)
        self.settings_button.setText("Settings")
        self.settings_button.setFont(QFont("Arial", 15, QFont.Bold))
        self.settings_button.setCursor(Qt.PointingHandCursor)
        grid_layout.addWidget(self.settings_button, 1, 2)

        # button 5
  
        self.bill_button = QPushButton()
        self.bill_button.setIcon(QIcon(".//img//cart.jpeg"))
        self.bill_button.setIconSize(QSize(400, 150))
        self.bill_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                border-radius: 20px;
                background-color: rgba(0, 0, 0, 50%);
            }
        """)
        self.bill_button.setText("New Bill")
        self.bill_button.setFont(QFont("Arial", 15, QFont.Bold))
        self.bill_button.setCursor(Qt.PointingHandCursor)
        grid_layout.addWidget(self.bill_button, 2, 1)       

        layout.addStretch()
        layout.addLayout(grid_layout)
        layout.addStretch()

        self.setLayout(layout)



    
    def start_services_page(self):
        self.close()
        self.services_page = ServicesPage(self)
        self.services_page.showMaximized()

    def start_reports_page(self):
        self.close()
        self.reports_page = ReportsPage(self)
        self.reports_page.showMaximized() 

    def start_customers_page(self):
        self.close()
        self.customers_page = CustomersPage(self) 
        self.customers_page.showMaximized() 

    def start_settings_page(self):
        self.close()
        self.settings_page = SettingsPage(self) 
        self.settings_page.showMaximized() 



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomePage()
    window.showMaximized()  # عرض النافذة بحجم الشاشة بالكامل
    sys.exit(app.exec_())
