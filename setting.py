import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("SettingsPage")
        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Adjust margins

        # Top layout with back, minimize and close buttons
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



        top_layout.addWidget(self.back_button)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # Title
      
        # Grid Layout for Buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)  # Adjust the spacing between buttons

        buttons = [
            ("Add User", None), ("Edit Price List", None), 
            ("Delete User", None), ("Show Price List", None), 
            ("E-mail", None), ("whatsapp", None)
        ]

        positions = [(i, j) for i in range(3) for j in range(2)]

        for position, (label, image) in zip(positions, buttons):
            button = QPushButton(label)
            button.setFixedSize(250, 40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: white; 
                    color: black; 
                    font-size: 15px; 
                    font-weight: bold; 
                    border: 2px solid black;
                    border-radius: 15px;
                }
                QPushButton::hover {
                    background-color: #DDD;
                }
            """)
            if image:
                button.setIcon(QIcon(image))
            grid_layout.addWidget(button, *position)

        main_layout.addLayout(grid_layout)
        main_layout.setAlignment(grid_layout, Qt.AlignCenter)

        self.setLayout(main_layout)

        self.back_button.clicked.connect(self.back_to_home)

    def back_to_home(self):
        self.close()
        self.parent.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsPage()
    window.show()
    sys.exit(app.exec_())
