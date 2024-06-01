import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFormLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

class ServicesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Services Page")
        self.setStyleSheet("background-color: #f5f5f5;")

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Top layout with back, minimize and close buttons
        top_layout = QHBoxLayout()

        back_button = QPushButton("BACK")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("background-color: black; color: white;")
        back_button.clicked.connect(self.close)  # Close the window when the button is clicked

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

        # Main content layout
        layout = QHBoxLayout()

        # Left side with the service button
        left_layout = QVBoxLayout()

        service_button = QPushButton()
        service_button.setIcon(QIcon(".//img//Services.png"))
        service_button.setIconSize(QSize(480, 150))
        service_button.setFixedSize(400, 150)
        service_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-size:cover;
            }
        """)
        service_label = QLabel("Services")
        service_label.setAlignment(Qt.AlignCenter)
        service_label.setStyleSheet("color: black; font-size: 16px;")

        left_layout.addStretch()
        left_layout.addWidget(service_button, alignment=Qt.AlignCenter)
        left_layout.addWidget(service_label, alignment=Qt.AlignCenter)
        left_layout.addStretch()

        # Right side with the form and save button
        right_layout = QVBoxLayout()

        form_layout = QFormLayout()

        name_input = QLineEdit()
        mobile_input = QLineEdit()
        address_input = QLineEdit()
        email_input = QLineEdit()
        visit_date_input = QLineEdit()

        form_layout.addRow("Name:", name_input)
        form_layout.addRow("Mobile No.:", mobile_input)
        form_layout.addRow("Address:", address_input)
        form_layout.addRow("Email:", email_input)
        form_layout.addRow("Visit Date:", visit_date_input)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setStyleSheet("""
            QWidget {
                font-size: 16px;
                padding: 10px;
                background-color: white;
            }
        """)

        save_button = QPushButton("SAVE")
        save_button.setFixedSize(100, 40)
        save_button.setStyleSheet("background-color: black; color: white;border-radius: 20px")

        right_layout.addStretch()
        right_layout.addWidget(form_widget)
        right_layout.addWidget(save_button, alignment=Qt.AlignCenter)
        right_layout.addStretch()

        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 2)

        main_layout.addLayout(layout)

        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServicesPage()
    window.showMaximized()  # عرض النافذة بحجم الشاشة بالكامل
    sys.exit(app.exec_())
