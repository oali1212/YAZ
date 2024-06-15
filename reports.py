import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from backend_functions import YAZ
from datetime import datetime

class ReportsPage(QWidget):
    def __init__(self,parent,user):
        
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Nail Selection")
        self.setStyleSheet("background-color: #F5F5DC;")
        self.showMaximized()  # Show the window in full screen
        self.user = user 
        main_layout = QVBoxLayout()

        # Top layout with back, minimize, and close buttons
        top_layout = QHBoxLayout()
        self.central_layout = QVBoxLayout() 
        self.back_button = QPushButton("◀")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("font-size: 35px;")       
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        self.add_button = QPushButton("Add Transaction")
        self.add_button.clicked.connect(self.add_clicked)
        self.add_button.setFixedWidth(100)
        self.central_layout.addWidget(self.add_button)

        self.now = datetime.now()




        
        self.setLayout(main_layout)
        self.back_button.clicked.connect(self.back_to_home)

        self.excel_path = ".//Customers Bills//main_sheet.xlsx"
        yaz = YAZ() 
        self.table = yaz.get_table_from_excel(self.excel_path)
        if self.table:
            self.central_layout.addWidget(self.table)
            main_layout.addLayout(self.central_layout)
            self.table.setColumnCount(self.table.columnCount() + 1)
            for row in range(1, self.table.rowCount() ):
                del_button = QPushButton("🗑️")
                del_button.setStyleSheet("font-size:20px;")
                self.table.setCellWidget(row,8,del_button)
                del_button.clicked.connect(lambda _, r=row : self.delete_clicked(r))
                    
                
     
                
    
    def back_to_home(self):
        self.close()
        self.parent.showMaximized()

    def rebind_delete_buttons(self):
        self.table.setColumnCount(self.table.columnCount() + 1)
        for row in range( 1, self.table.rowCount() ):
            del_button = QPushButton("🗑️")
            del_button.setStyleSheet("font-size:20px;")
            self.table.setCellWidget(row,8,del_button)
            del_button.clicked.connect(lambda _, r=row : self.delete_clicked(r))
  


    def delete_clicked(self,row):
        yaz = YAZ()
        id = self.table.item(row,2)
        if id: 
            id = id.text() 
        else:
            return False
        print(id)
        yaz.delete_row_by_id(id)
        temp_table = yaz.get_table_from_excel(self.excel_path)
        self.table.deleteLater()
        self.table = temp_table
        self.central_layout.addWidget(self.table)
        self.rebind_delete_buttons()
      

    def add_clicked(self):
   
        
        date = self.now.strftime("%d/%m/%y")
        time = self.now.strftime("%H%M%S")
        
        dialog = AddEntryDialog(self.user)
        if dialog.exec_() == QDialog.Accepted:
            self.table.setRowCount(self.table.rowCount() + 1) 
            data = dialog.get_data()
            list_entry = [
                date,
                time,
                date.replace("/", "") + time.replace(":", ""),
                data["transaction_type"],
                data["description"],
                str(data["price"]),
                self.user,
                data["notes"]
            ]
            
            yaz = YAZ()
            retval = yaz.append_row_to_main_sheet(list_entry)
            if retval == True: 
                temp_table = yaz.get_table_from_excel(self.excel_path)
                self.table.deleteLater()
                self.table = temp_table
                self.central_layout.addWidget(self.table)
                self.rebind_delete_buttons()
            else: 
                QMessageBox.warning(None, "Warning: File Access Error", retval + '\nPlease Close the file if it is open')
                app.exec_()

class AddEntryDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        
        self.user = user
        
        self.setWindowTitle("Add New Transaction")
        layout = QVBoxLayout(self)
        
        self.transaction_type_label = QLabel("Transaction Type:")
        self.transaction_type_input = QComboBox()
        self.transaction_type_input.addItems(["IN", "OUT"])
        layout.addWidget(self.transaction_type_label)
        layout.addWidget(self.transaction_type_input)
        
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        
        self.price_label = QLabel("Price:")
        self.price_input = QLineEdit()
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)
        
        self.notes_label = QLabel("Notes:")
        self.notes_input = QTextEdit()
        layout.addWidget(self.notes_label)
        layout.addWidget(self.notes_input)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
    
    def validate_and_accept(self):
        transaction_type = self.transaction_type_input.currentText()
        description = self.description_input.text()
        price = self.price_input.text()
        notes = self.notes_input.toPlainText()
        
        if not description or not price:
            QMessageBox.warning(self, "Input Error", "Description and Price cannot be empty.")
            return
        
        try:
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price must be a valid number.")
            return
        
        self.transaction_type = transaction_type
        self.description = description
        self.price = price
        self.notes = notes
        
        self.accept()
    
    def get_data(self):
        return {
            "transaction_type": self.transaction_type,
            "description": self.description,
            "price": self.price,
            "notes": self.notes
        }        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportsPage('',"safas")
    window.show()
    sys.exit(app.exec_())
