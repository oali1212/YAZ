import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Customers(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Customers Data")
        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color

        main_layout = QVBoxLayout()

        # Top layout with back, minimize and close buttons
        top_layout = QHBoxLayout()

        back_button = QPushButton("BACK")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: black; 
                color: white; 
                font-size: 12px; 
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #333;
            }
        """)        

        minimize_button = QPushButton("_")
        minimize_button.setFixedSize(40, 40)
        minimize_button.setStyleSheet("background-color: black; color: white;")
        minimize_button.clicked.connect(self.showMinimized)

        close_button = QPushButton("X")
        close_button.setFixedSize(40, 40)
        close_button.setStyleSheet("background-color: black; color: white;")
        close_button.clicked.connect(self.close)

        top_layout.addWidget(back_button)
        top_layout.addStretch()
        top_layout.addWidget(minimize_button)
        top_layout.addWidget(close_button)

        main_layout.addLayout(top_layout)

        # Title
        title = QPushButton("Customers Data")
        title.setFixedSize(400, 50)
        title.setStyleSheet("background-color: #F5F5DC; color: black; font-size: 24px; font-weight: bold; border: none;")
        title.setEnabled(False)
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Table
        self.table = QTableWidget(10, 6)
        self.table.setHorizontalHeaderLabels(["#", "Name", "Mobile", "E-mail", "Visit Date", "Follow", "How I Heard About"])
        self.table.setFont(QFont('Arial', 12))
        self.table.horizontalHeader().setFont(QFont('Arial', 12, QFont.Bold))
        self.table.setStyleSheet("QHeaderView::section {background-color: #4682B4; color: white;} QTableWidget {gridline-color: #D3D3D3;}")
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 200)

        # Adding some example data
        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(0, 1, QTableWidgetItem("ahmed hassan"))
        self.table.setItem(0, 2, QTableWidgetItem("01018566506"))

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Customers()
    window.show()
    sys.exit(app.exec_())
