import sys
import pickle
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QInputDialog, QMessageBox, QDialog, QComboBox, QDialogButtonBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from backend_functions import YAZ

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color

        self.users = self.load_users()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Adjust margins

        # Top layout with back, minimize, and close buttons
        top_layout = QHBoxLayout()

        self.back_button = QPushButton("◀")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("font-size: 35px;")       

        top_layout.addWidget(self.back_button)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # Title
        title_label = QLabel("Password Management Tool")
        title_label.setFont(QFont('Arial', 24))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Grid Layout for Buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)  # Adjust the spacing between buttons

        buttons = [
            ("Add User", self.add_user), 
            ("Delete User", self.delete_user), 
            ("Show Users", self.show_users)
        ]

        positions = [(i, j) for i in range(2) for j in range(2)]

        for position, (label, handler) in zip(positions, buttons):
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
            button.clicked.connect(handler)
            grid_layout.addWidget(button, *position)

        main_layout.addLayout(grid_layout)
        main_layout.setAlignment(grid_layout, Qt.AlignCenter)

        self.setLayout(main_layout)

        self.back_button.clicked.connect(self.back_to_home)

    def back_to_home(self):
        
        if self.parent:
            self.parent.showMaximized()
        self.close()
    def load_users(self):
        try:
            yaz = YAZ()
            users_file = 'users.bin'
            users_file = yaz.get_relink(users_file)
            with open(users_file, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}

    def save_users(self):
        yaz = YAZ()
        users_file = 'users.bin'
        users_file = yaz.get_relink(users_file)
        with open(users_file, 'wb') as f:
            pickle.dump(self.users, f)

    def add_user(self):
        username, ok = QInputDialog.getText(self, 'Add User', 'Enter username:')
        if ok and username:
            if username in self.users:
                QMessageBox.warning(self, 'Error', 'User already exists!')
            else:
                password, ok = QInputDialog.getText(self, 'Add User', 'Enter password:')
                if ok and password:
                    self.users[username] = password
                    self.save_users()
                    QMessageBox.information(self, 'Success', 'User added successfully!')

    def delete_user(self):
        if len(self.users) == 1:
            QMessageBox.warning(self, 'Error', 'At least one user must be registerd!')
            return
        if not self.users:
            QMessageBox.warning(self, 'Error', 'No users to delete!')
            return

        dialog = QDialog(self)
        dialog.setWindowTitle('Delete User')
        layout = QVBoxLayout(dialog)

        combo = QComboBox(dialog)
        combo.addItems(self.users.keys())
        layout.addWidget(combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            username = combo.currentText()
            if username in self.users:
                del self.users[username]
                self.save_users()
                QMessageBox.information(self, 'Success', 'User deleted successfully!')
            else:
                QMessageBox.warning(self, 'Error', 'User does not exist!')

    def show_users(self):
        user_list = '\n'.join(self.users.keys())
        QMessageBox.information(self, 'Users', f'Existing Users:\n{user_list}')

    def validate_user(self, username, password):
        return self.users.get(username) == password
    
    
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = SettingsPage('')
#     window.show()
#     sys.exit(app.exec_())
