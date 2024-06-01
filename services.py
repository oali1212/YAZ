import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Services(QPushButton):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("border: none;")

    def set_image(self, image_path, size):
        self.size = size
        self.setFixedSize(size, size)
        self.setIcon(QIcon(self.create_circular_pixmap(image_path, size)))
        self.setIconSize(QSize(size, size))

    def create_circular_pixmap(self, image_path, size):
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

class ServicesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Services Page")
        self.setStyleSheet("background-color: #f5f5f5;")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Top layout with Back button, minimize, and close buttons
        top_layout = QHBoxLayout()
        
        self.back_button = QPushButton("BACK")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("""
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

        services_info = [
            ("Nails", ".//img//nails.jpg"),
            ("Pedicure", ".//img//pedicure.jpg"),
            ("Facial", ".//img//facial.jpg"),
            ("Eyelashes", ".//img//eyelashes.jpg")
        ]

        for text, image_path in services_info:
            button = Services()
            button.set_image(image_path, 150)
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: black; font-size: 16px;")

            vbox = QVBoxLayout()
            vbox.addWidget(button, alignment=Qt.AlignCenter)
            vbox.addWidget(label, alignment=Qt.AlignCenter)
            middle_layout.addLayout(vbox)

        layout.addLayout(middle_layout)
        layout.addSpacing(50)  # Move elements up

        # Bottom layout with Proceed Checkout button
        bottom_layout = QHBoxLayout()
        
        proceed_button = QPushButton("PROCEED CHECK OUT")
        proceed_button.setFixedSize(200, 40)
        proceed_button.setStyleSheet("background-color: black; color: white; font-size: 16px; font-weight: bold;")

        bottom_layout.addStretch()
        bottom_layout.addWidget(proceed_button, alignment=Qt.AlignRight)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

def run_application():
    app = QApplication(sys.argv)
    window = ServicesPage()
    window.showMaximized()  # عرض النافذة بحجم الشاشة بالكامل
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_application()
