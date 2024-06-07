import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QPainter, QFont, QPainterPath
from PyQt5.QtCore import Qt, QRectF
from configparser import ConfigParser
from backend_functions import YAZ
from PyQt5.QtGui import QFont


class NailSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eye Lashes Selection")
        
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color


        main_layout = QVBoxLayout()

        back_button = QPushButton("◀")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("font-size: 35px;")       

        self.add_button_button = QPushButton("New Service ➕")
        self.add_button_button.setFixedSize(200, 40)
        self.add_button_button.setStyleSheet("background-color: black; color: white; font-size: 25px; font-weight: bold;")

        main_layout.addWidget(back_button)

        yaz = YAZ()
        ini_file = 'settings.ini'  # Replace with your actual ini file path
        section = 'eye lashes'  # Replace with your actual section
        table = yaz.create_price_table(ini_file, section)

        if table:

            main_layout.addWidget(table)

        main_layout.addWidget(self.add_button_button, 0, Qt.AlignRight)

        self.setLayout(main_layout)
        self.showMaximized()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NailSelectionWindow()
    window.show()
    sys.exit(app.exec_())
