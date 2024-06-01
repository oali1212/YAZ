import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRectF

class Services(QPushButton):
    def __init__(self, image_path, size):
        super().__init__()
        self.size = size
        self.setFixedSize(size, size)
        self.setIcon(QIcon(self.create_circular_pixmap(image_path, size)))
        self.setIconSize(QSize(size, size))
        self.setStyleSheet("border: none;")

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
        back_button.clicked.connect(self.close)  # Close the window when the button is clicked

        top_layout.addWidget(back_button, alignment=Qt.AlignLeft)
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

        # Button 1
        self.nails_button = Services(".//img//nails.jpg", 150)
        label1 = QLabel("Nails")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("color: black; font-size: 16px;")
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.nails_button, alignment=Qt.AlignCenter)
        vbox1.addWidget(label1, alignment=Qt.AlignCenter)
        middle_layout.addLayout(vbox1)

        # Button 2
        self.pedicure_button = Services(".//img//pedicure.jpg", 150)
        label2 = QLabel("Pedicure")
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet("color: black; font-size: 16px;")
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.pedicure_button, alignment=Qt.AlignCenter)
        vbox2.addWidget(label2, alignment=Qt.AlignCenter)
        middle_layout.addLayout(vbox2)

        # Button 3
        self.facial_button = Services(".//img//facial.jpg", 150)
        label3 = QLabel("Facial")
        label3.setAlignment(Qt.AlignCenter)
        label3.setStyleSheet("color: black; font-size: 16px;")
        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.facial_button, alignment=Qt.AlignCenter)
        vbox3.addWidget(label3, alignment=Qt.AlignCenter)
        middle_layout.addLayout(vbox3)

        # Button 4
        self.eye_button = Services(".//img//eyelashes.jpg", 150)
        label4 = QLabel("Eyelashes")
        label4.setAlignment(Qt.AlignCenter)
        label4.setStyleSheet("color: black; font-size: 16px;")
        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.eye_button, alignment=Qt.AlignCenter)
        vbox4.addWidget(label4, alignment=Qt.AlignCenter)
        middle_layout.addLayout(vbox4)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServicesPage()
    window.showMaximized()  # عرض النافذة بحجم الشاشة بالكامل
    sys.exit(app.exec_())
