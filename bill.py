from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from configparser import ConfigParser
from backend_functions import YAZ
import sys
class TabWindow(QWidget):
    def __init__(self, name):
        super().__init__()

        self.setting_file = "settings.ini"
        self.name = name 
        self.section = self.name.lower() 
        self.setWindowTitle(f"{name} Selection")
        self.setStyleSheet("background-color: #F5F5DC;")

        self.main_layout = QVBoxLayout()
        
        label = QLabel(f"{name} Services")
        label.setStyleSheet("font-size: 30px; font-weight: 900; font-family: Comic Sans MS;")
          
        self.main_layout.addWidget(label)
        self.main_layout.addWidget(QLabel())
        
        yaz = YAZ()

        self.table = yaz.create_price_table(self.setting_file, self.section)

        self.table.setHorizontalHeaderLabels(['Service', 'Price (EGP)', 'Price -30%', 'Price -40%', "Add to Cart"])




        self.table_layout = QHBoxLayout()
        self.table_layout.setAlignment(Qt.AlignCenter)
        
        if self.table:
            self.table_layout.addWidget(self.table)
            self.main_layout.addLayout(self.table_layout)

        self.setLayout(self.main_layout)



class NewBillPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Bill")
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color

        # Main Layout
        self.main_layout = QVBoxLayout()
        
        self.current_tab = "Nails"  # Set the initial tab name
        # Header Layout
        header_layout = QHBoxLayout()
        header_label = QLabel("New Bill")
        header_label.setStyleSheet("font-size: 30px; font-weight: 900; font-family: Comic Sans MS;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()

        self.cart_button = QPushButton()
        self.cart_button.setIcon(QIcon("./path_to_cart_icon.png"))  # Set the cart icon path
        self.cart_button.setFixedSize(40, 40)
        self.cart_button.setStyleSheet("background-color: transparent; border: none;")
        header_layout.addWidget(self.cart_button)

        self.main_layout.addLayout(header_layout)

        # Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.nails_tab = TabWindow("Nails")
        self.tab_widget.addTab(self.nails_tab, "Nails")

        self.eye_lashes_tab = TabWindow("Eye lashes")
        self.tab_widget.addTab(self.eye_lashes_tab, "Eye Lashes")

        self.facial_tab = TabWindow("Facial")
        self.tab_widget.addTab(self.facial_tab, "Facial")

        self.pedicure_tab = TabWindow("Pedicure")
        self.tab_widget.addTab(self.pedicure_tab, "Pedicure")


        self.nails_table = self.nails_tab.table
        self.eye_lashes_table = self.eye_lashes_tab.table
        self.facial_table = self.facial_tab.table
        self.pedicure_table = self.pedicure_tab.table

        self.main_layout.addWidget(self.tab_widget)


        for table in [self.nails_table, self.eye_lashes_table, self.facial_table,  self.pedicure_table ]:
            for row in range(table.rowCount()): 
                add_button = QPushButton("➕🛒")
                add_button.setStyleSheet("font-size:26px;")
                table.setCellWidget(row,4,add_button)               
                add_button.clicked.connect(lambda _, row=row,: self.add_button_clicked(row, self.current_tab))


        # Right Layout
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignTop)

        # Customer Name Input
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Enter customer name")
        self.customer_name_input.setFixedHeight(40)
        self.customer_name_input.setStyleSheet("font-size: 20px; font-weight: bold; background-color: white; border: 1px solid grey; border-radius: 5px; padding: 5px;")
        self.right_layout.addWidget(self.customer_name_input)

        # Bill Table
        self.bill_table = QTableWidget()
        self.bill_table.setRowCount(0)
        self.bill_table.setColumnCount(5)
        self.bill_table.setHorizontalHeaderLabels(['Service', 'Price', 'Discount %', 'Total', 'Delete'])
        self.bill_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bill_table.setGridStyle(Qt.SolidLine)
        self.right_layout.addWidget(self.bill_table)


                    


        # Total Price Label
        self.total_price_label = QLabel("Total Price: 0 EGP")
        self.total_price_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.right_layout.addWidget(self.total_price_label, alignment=Qt.AlignRight)

        save_button = QPushButton("Save")
        save_button.setFixedSize(200, 40)
        save_button.setStyleSheet("background-color: lightgrey; font-size: 20px; font-weight: bold;")
        self.right_layout.addWidget(save_button, alignment=Qt.AlignCenter)

        # Combine Layouts
        container_layout = QHBoxLayout()
        container_layout.addLayout(self.main_layout)
        container_layout.addLayout(self.right_layout)

        self.setLayout(container_layout)

        self.current_bill_items = []  # To track bill items and their positions


        ## BIND 
        self.tab_widget.currentChanged.connect(self.update_current_tab)


    def bind_new_rows(self):
        for row in range(self.bill_table.rowCount()):
            delete_button = QPushButton("🗑")
            self.bill_table.setCellWidget(row, 4, delete_button)  # Set the button in the second column
            delete_button.clicked.connect(lambda _, r=row: self.remove_from_bill(r))

    def add_button_clicked(self, index, tab):
        current_table = None
        price_list = []

        if tab == 'Nails':
            current_table = self.nails_table
        elif tab == "Eye Lashes":
            current_table = self.eye_lashes_table
        elif tab == "Pedicure":
            current_table = self.pedicure_table
        else:
            current_table = self.facial_table

        service_name = current_table.item(index, 0).text()
        price = float(current_table.item(index, 1).text())

        # Create a DiscountDialog instance
        dialog = DiscountDialog()
        dialog.exec_()
        # Execute the dialog to get the discount
        discount_selected = dialog.get_discount()
        
        if discount_selected:

            discount_value = int(discount_selected.strip('%'))
            discounted_price = price - (price * discount_value / 100)

            # Create widgets for discount input
            discount_spinbox = QSpinBox()
            discount_spinbox.setRange(0, 90)  # Set the range of discount from 0% to 90%
            discount_spinbox.setSuffix('%')  # Add '%' symbol after the number
            discount_spinbox.setValue(discount_value)  # Set default value to selected discount

            # Create dropdown menu for selecting discount rate
            discount_combo_box = QComboBox()
            discount_combo_box.addItems([f"{i}%" for i in range(0, 91, 5)])  # Add options from 0% to 90% in steps of 5%

            # Connect the discount_spinbox to update_discount_price when its value changes
            discount_spinbox.valueChanged.connect(lambda value, row=index: self.update_discount_price(row, price, value))

            price_list.extend([service_name, price, discount_value, discounted_price])
         

            row_position = self.bill_table.rowCount()  # Get the last row position
            self.bill_table.insertRow(row_position)  # Insert a new row

            # Set items for each column in the new row
            for column, item in enumerate(price_list):
                self.bill_table.setItem(row_position, column, QTableWidgetItem(str(item)))

            self.update_total_and_items()
            self.bind_new_rows()

    def update_current_tab(self, index):
        self.current_tab = self.tab_widget.tabText(index)
   

    def remove_from_bill(self, row):


        self.current_bill_items.pop(row)
        self.bill_table.removeRow(row)
        self.update_total_and_items()  # Update the total price


    def update_total_and_items(self):
        
        for row in range(self.bill_table.rowCount()):
            item = self.bill_table.item(row,3).text()
            if item:
                item = float(item)
                self.current_bill_items.append(item)
        total_price = sum(self.current_bill_items)
        self.total_price_label.setText(f"Total Price: {total_price} EGP")




class DiscountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Discount")
        layout = QVBoxLayout()
        self.label = QLabel("Select discount rate:")
        layout.addWidget(self.label)
        self.combobox = QComboBox()
        self.combobox.addItems([f"{i}%" for i in range(0, 91, 5)])  # Add options from 0% to 90% in steps of 5%
        layout.addWidget(self.combobox)
        self.button = QPushButton("OK")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.accept)
        self.setLayout(layout)

    def get_discount(self):
        return self.combobox.currentText()  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NewBillPage()

    window.showMaximized()
    sys.exit(app.exec_())
