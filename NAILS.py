import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QFont, QPainterPath
from PyQt5.QtCore import Qt, QRectF

class RoundButton(QPushButton):
    def __init__(self, label, image_path=None, width=100, height=100, parent=None):
        super().__init__(parent)
        self.label = label
        self.image_path = image_path
        self.setFixedSize(width, height)  # Set a fixed size for each button

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRectF(0, 0, self.width(), self.height())  # Use QRectF directly
        
        # Draw the ellipse (circle) shape
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(Qt.white)
        painter.drawEllipse(rect)
        
        if self.image_path:
            pixmap = QPixmap(self.image_path).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Create a circular path for masking
            path = QPainterPath()
            path.addEllipse(rect)

            # Apply transparency and draw the circular image
            painter.setClipPath(path)
            painter.setOpacity(0.6)  # Set the opacity to 60%
            painter.drawPixmap(rect.toRect(), pixmap)
            painter.setOpacity(1.0)  # Reset opacity
        
        painter.setClipping(False)  # Reset clipping
        painter.setPen(Qt.black)
        painter.setFont(QFont('Arial', 13, QFont.Bold))  # Adjust font size and weight here
        painter.drawText(rect, Qt.AlignCenter, self.label)

class NailSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nail Selection")
        self.showMaximized()  # Show the window in full screen

        main_layout = QVBoxLayout()

        # Top layout with back, minimize, and close buttons
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
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        buttons = [
            ("Gel polish", "./img/Gelpolish.jpg"), ("Hard Gel", "./img/hardgel.jpg"), ("Treatment", "./img/Treatment.jpg"), ("Acrylic", "./img/Acrylic.jpg"),
            ("Simple  \n nail design", "./img/simple_nail_design.jpg"), ("French", "./img/nails.jpg"), ("Half gel", "./img/half_jell.jpg"),
            ("Fake nails\nGel polish", "./img/Fake nails+Gel polish.jpg"), ("Cat eye", "./img/cat_eye.jpg"),
            ("Complex nail \n design", "./img/Complex_nail_design.jpg"), ("Pearl powder", "./img/Pearl_powder.jpg"),
            ("Neon powder", "./img/neon_powder.jpg"), ("Nail strass", "./img/Nail_strass.jpg"), ("Nail Sticker", "./img/NailSticker.jpg"), ("Ombre", "./img/Ombre.jpg")
        ]

        positions = [(i, j) for i in range(4) for j in range(4)]

        for position, (label, image) in zip(positions, buttons):
            button = RoundButton(label, image, width=120, height=120)  # Adjust the width and height here
            grid_layout.addWidget(button, *position)
        
        proceed_button = QPushButton("DONE PRODUCT SELECTION")
        proceed_button.setFixedSize(200, 40)
        proceed_button.setStyleSheet("background-color: black; color: white; font-size: 10px; font-weight: bold;")

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(proceed_button, 0, Qt.AlignRight)
        
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NailSelectionWindow()
    window.show()
    sys.exit(app.exec_())