import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setStyleSheet("background-color: #f4f1ea;")

        self.initUI()

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
        self.services_button.setText("Services  ")
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
        grid_layout.addWidget(self.reports_button, 0, 1)

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
        grid_layout.addWidget(self.settings_button, 1, 1)

        layout.addStretch()
        layout.addLayout(grid_layout)
        layout.addStretch()

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomePage()
    window.showMaximized()  # عرض النافذة بحجم الشاشة بالكامل
    sys.exit(app.exec_())
