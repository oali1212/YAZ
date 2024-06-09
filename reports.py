import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



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

        self.table = QTableWidget()
        central_layout.addWidget(self.table)
        main_layout.addLayout(central_layout)


        
        self.setLayout(main_layout)
        self.back_button.clicked.connect(self.back_to_home)


    def back_to_home(self):
        self.close()
        self.parent.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportsPage('')
    window.show()
    sys.exit(app.exec_())
