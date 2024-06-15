import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from backend_functions import YAZ


class ReportsPage(QWidget):
    def __init__(self,parent):
        
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Nail Selection")
        self.setStyleSheet("background-color: #F5F5DC;")
        self.showMaximized()  # Show the window in full screen

        main_layout = QVBoxLayout()

        # Top layout with back, minimize, and close buttons
        top_layout = QHBoxLayout()
        central_layout = QVBoxLayout() 
        self.back_button = QPushButton("◀")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("font-size: 35px;")       
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        self.add_button = QPushButton("Add Transaction")
        self.add_button.clicked.connect(self.add_clicked)
        central_layout.addWidget(self.add_button)
        # self.table = QTableWidget()
        # central_layout.addWidget(self.table)



        
        self.setLayout(main_layout)
        self.back_button.clicked.connect(self.back_to_home)

        self.excel_path = ".//Customers Bills//main_sheet.xlsx"
        yaz = YAZ() 
        self.table = yaz.get_table_from_excel(self.excel_path)
        central_layout.addWidget(self.table)
        main_layout.addLayout(central_layout)


    def back_to_home(self):
        self.close()
        self.parent.showMaximized()

    def add_clicked(self):
        self.table.setRowCount(self.table.rowCount() + 1) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportsPage('')
    window.show()
    sys.exit(app.exec_())
