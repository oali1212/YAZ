import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRectF

from facial import facialPage
from eye_lashes import eyelashesPage
from pedicure import pedicurePage
from nails import nailsPage

class CircularButton(QPushButton):
    def __init__(self, image_path, size):
        super().__init__()
        self.size = size
        self.setFixedSize(size, size)
        self.setIcon(QIcon(self.create_circular_pixmap(image_path, size)))
        self.setIconSize(QSize(size, size))
        self.setStyleSheet("border: none;")

    def create_circular_pixmap(self, image_path, size):
        if not os.path.isfile(image_path):
            #print(f"Image not found: {image_path}")
            return QPixmap()
        
        pixmap = QPixmap(image_path).scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.transparent)

        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(pixmap)
        rect = QRectF(0, 0, size, size)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect)
        painter.end()

        return circular_pixmap

class ServiceWidget(QWidget):
    def __init__(self, image_path, text, size):
        super().__init__()
        layout = QVBoxLayout()
        self.button = CircularButton(image_path, size)
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: black; font-size: 16px;")
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.setLayout(layout)

class ServicesPage(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Services Page")
        self.setStyleSheet("background-color: #f5f5f5;")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Top layout with Back button, minimize, and close buttons
        top_layout = QHBoxLayout()
        
        self.back_button = QPushButton("◀")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("font-size: 35px;")       

        self.back_button.clicked.connect(self.back_to_home)  # Close the window when the button is clicked

        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        top_layout.addStretch()

        layout.addLayout(top_layout)

        title_label = QLabel("Services")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black; font-size: 26px; font-weight: bold;")  # Adjusted font size

        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addSpacing(-20)  # Move elements up

        # Middle layout with service buttons
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(20)  # Adjust spacing between buttons

        self.style = """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                border-radius: 20px;
                background-color: rgba(0, 0, 0, 50%);
            }
        """
        # Service Widget 1
        nails_image_path = os.path.abspath(".//img//nails.jpg")
        self.nails_button = ServiceWidget(nails_image_path, "Nails", 150)
        middle_layout.addWidget(self.nails_button, alignment=Qt.AlignCenter)
        self.nails_button.button.setCursor(Qt.PointingHandCursor)
        self.nails_button.setStyleSheet(self.style)
        self.nails_button.button.clicked.connect(self.go_to_nails)  # Connect the button click event
        
        # Service Widget 2
        pedicure_image_path = os.path.abspath(".//img//pedicure.jpg")
        self.pedicure_widget = ServiceWidget(pedicure_image_path, "Pedicure", 150)
        middle_layout.addWidget(self.pedicure_widget, alignment=Qt.AlignCenter)
        self.pedicure_widget.button.setCursor(Qt.PointingHandCursor)
        self.pedicure_widget.setStyleSheet(self.style)
        self.pedicure_widget.button.clicked.connect(self.go_to_pedicure)  # Connect the button click event

        # Service Widget 3
        facial_image_path = os.path.abspath(".//img//facial.jpg")
        self.facial_widget = ServiceWidget(facial_image_path, "Facial", 150)
        middle_layout.addWidget(self.facial_widget, alignment=Qt.AlignCenter)
        self.facial_widget.button.setCursor(Qt.PointingHandCursor)
        self.facial_widget.setStyleSheet(self.style)
        self.facial_widget.button.clicked.connect(self.go_to_facial)  # Connect the button click event

        # Service Widget 4
        eyelashes_image_path = os.path.abspath(".//img//eyelashes.jpg")
        self.eye_widget = ServiceWidget(eyelashes_image_path, "Eyelashes", 150)
        middle_layout.addWidget(self.eye_widget, alignment=Qt.AlignCenter)
        self.eye_widget.button.setCursor(Qt.PointingHandCursor)
        self.eye_widget.setStyleSheet(self.style)
        self.eye_widget.button.clicked.connect(self.go_to_eyelashes)  # Connect the button click event

        layout.addLayout(middle_layout)
        
        layout.addSpacing(50)  # Move elements up

        # Bottom layout with Proceed Checkout button
        bottom_layout = QHBoxLayout()
        
 

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def back_to_home(self):
        self.close()
        self.parent.showMaximized()

    def go_to_facial(self):
        self.close()
        self.facial = facialPage(self) 
        self.facial.showMaximized()

    # Define the functions that handle the button clicks
    def go_to_nails(self):
        self.close()
        self.nails = nailsPage(self) 
        self.nails.showMaximized()

    def go_to_pedicure(self):
        self.close()
        self.pedicure = pedicurePage(self) 
        self.pedicure.showMaximized()

    def go_to_eyelashes(self):
        self.close()
        self.eye = eyelashesPage(self) 
        self.eye.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServicesPage(' ')
    window.showMaximized()  # عرض النافذة بحجم الشاشة بالكامل
    sys.exit(app.exec_())
