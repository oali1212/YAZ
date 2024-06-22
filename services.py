import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRectF

from generic_macro import GenericServicePage

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
            ##print(f"Image not found: {image_path}")
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
    def __init__(self, parent):
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

        # Define the service information
        self.services_list = ['Nails', 'Pedicure', 'Facial', 'Eye lashes']

        services = [
            {"image": f".//img//{service.lower().replace(' ', '')}.jpg", "name": service}
            for service in self.services_list
        ]

        # Create service widgets dynamically
        for service in services:
            image_path = os.path.abspath(service["image"])
            widget = ServiceWidget(image_path, service["name"], 150)
            middle_layout.addWidget(widget, alignment=Qt.AlignCenter)
            widget.button.setCursor(Qt.PointingHandCursor)
            widget.setStyleSheet(self.style)
            widget.button.clicked.connect(lambda _, s=service: self.go_to_service(s["name"]))

        layout.addLayout(middle_layout)
        layout.addSpacing(50)  # Move elements up

        # Bottom layout with Proceed Checkout button
        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def back_to_home(self):
        self.parent.showMaximized()
        self.close()

    def go_to_service(self, service_name):
        self.generic_service_page = GenericServicePage(self, service_name)
        self.generic_service_page.showMaximized()
        self.close()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ServicesPage(' ')
#     window.showMaximized()  # Display the window in full screen
#     sys.exit(app.exec_())
