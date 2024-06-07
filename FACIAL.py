import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from configparser import ConfigParser
from backend_functions import YAZ
from PyQt5.QtGui import *


class NailSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Facial Selection")
        
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color

        self.settings_file = "settings.ini"
        self.section = "facial"
        self.main_layout = QVBoxLayout()
        
        label = QLabel("Facial Services")
        label.setStyleSheet("font-size: 30px; font-weight: 900; font-family: Comic Sans MS;")
          
        self.main_layout.addWidget(label)
        self.main_layout.addWidget(QLabel())
        back_button = QPushButton("◀")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("font-size: 35px;")       

        self.add_button = QPushButton("New Service ➕")
        self.add_button.setFixedSize(200, 40)
        self.add_button.setStyleSheet(" color: black; font-size: 25px; ")

        self.edit_button = QPushButton("Edit Services ✎")
        self.edit_button.setFixedSize(200, 40)
        self.edit_button.setStyleSheet(" color: black; font-size: 25px;")        
        

        self.save_button = QPushButton("Save ✅")
        self.save_button.setFixedSize(200, 40)
        self.save_button.setStyleSheet(" color: black; font-size: 25px; ")
        

        yaz = YAZ()
        ini_file = 'settings.ini'  # Replace with your actual ini file path
        section = 'facial'  # Replace with your actual section
        self.table = yaz.create_price_table(ini_file, section)

        self.table_layout = QHBoxLayout()
        self.table_layout.setAlignment(Qt.AlignCenter) 
        
        if self.table:

            self.table_layout.addWidget(self.table)
            self.main_layout.addLayout(self.table_layout)

        self.main_layout.addWidget(self.add_button, 0, Qt.AlignRight)
        self.main_layout.addWidget(self.edit_button, 1, Qt.AlignRight)
        self.main_layout.addWidget(self.save_button, 2, Qt.AlignRight)

        self.setLayout(self.main_layout)
        self.showMaximized()

        self.add_button.clicked.connect(self.show_add_service_dialog)

        for row in range(self.table.rowCount() ): 

            remove_button = self.table.cellWidget(row,4)
            remove_button.clicked.connect(lambda _,row = row: self.delete_selected(row))

    def show_add_service_dialog(self):
        dialog = AddServiceDialog(self)
        if dialog.exec_():
            name, price = dialog.get_service_info()
            name = name.replace(" ", "_")
            name = name.replace("+", "__")
            yaz = YAZ() 

            yaz.add_service(self.settings_file, self.section, name, price)
            self.new_table = yaz.create_price_table(self.settings_file, self.section)
            if self.new_table: 
                
                self.table.setParent(None)
                self.table = self.new_table
                self.table_layout.addWidget(self.table)

   
    def delete_selected(self,index):
 
        name = self.table.item(int(index), 0).text()
        name = name.lower()
        name = name.replace("&", "__")
        name = name.replace(" ", "_")

        yaz = YAZ()
        yaz.delete_service(self.settings_file,self.section,name)
        
        print(f"i am trying to delete {name}")
        self.new_table = yaz.create_price_table(self.settings_file, self.section)
        if self.new_table: 
            
            self.table.setParent(None)
            self.table = self.new_table
            self.table_layout.addWidget(self.table)        



class AddServiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Service")
        
        layout = QVBoxLayout()
        
        self.name_edit = QLineEdit()
        self.price_edit = QLineEdit()
        
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_edit)
        form_layout.addWidget(QLabel("Price:"))
        form_layout.addWidget(self.price_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.check_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

    def get_service_info(self):
        name = self.name_edit.text()
        price = self.price_edit.text()
        return name, price

    def check_and_accept(self):
        name, price = self.get_service_info()
        if not name or not price:
            self.show_error_dialog("Name and price must not be empty.")
        elif not price.isnumeric():
            self.show_error_dialog("Price must be numerical.")
        else:
            self.accept()

    def show_error_dialog(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NailSelectionWindow()
    window.show()
    sys.exit(app.exec_())
