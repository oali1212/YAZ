import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize  

class PreLogin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #f4f1eb;") # تعيين الخلفية للون أبيض

        self.center_window() # جعل النافذة في وسط الشاشة

        # إنشاء علامة لعرض الصورة
        self.image_label = QLabel(self)
        pixmap = QPixmap("img/logo.png")  # تغيير "your_image.jpg" إلى مسار الصورة

        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("width: 200px !important; height: 200px !important;")
        pixmap = pixmap.scaled(QSize(200, 150), Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # إنشاء زر "Login"
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("background-color: black; color: white; border: none; padding: 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; border-radius: 5px;")

        # تحديد موقع وحجم العناصر
        self.set_layout()

    def center_window(self):
        # تحديد حجم النافذة ليكون بحجم شاشة الكمبيوتر
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)

    def set_layout(self):
        # تحديد موقع وحجم العناصر
        window_width = self.width()
        window_height = self.height()

        # تحديد موقع وحجم الصورة
        image_width = 400
        image_height = 200
        self.image_label.setGeometry((window_width - image_width) // 2, (window_height - image_height) // 2 - 50, image_width, image_height)

        # تحديد موقع وحجم الزر "Login"
        button_width = 100
        button_height = 30
        self.login_button.setGeometry((window_width - button_width) // 2, (window_height - button_height) // 2 + 50, button_width, button_height)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     login_page = PreLogin()
#     login_page.show()
#     sys.exit(app.exec_())
