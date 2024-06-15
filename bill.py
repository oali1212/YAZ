from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from configparser import ConfigParser
from backend_functions import YAZ
import os
import sys
from datetime import datetime
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
    def __init__(self,parent,user):
        super().__init__()
        self.parent = parent
        self.user = user
        self.setWindowTitle("New Bill")
        self.setStyleSheet("background-color: #F5F5DC;")  # Background color
        self.timer = QTimer()  # Create a QTimer instance
        self.timer.timeout.connect(self.update_date_time)  # Connect timeout signal to update_date_time method
        self.timer.start(1000)  # Start the timer to update every 1000 ms (1 second)

        # Main Layout
        self.main_layout = QVBoxLayout()
        
        self.current_tab = "Nails"  # Set the initial tab name
        # Header Layout
        header_layout = QHBoxLayout()
        header_label = QLabel("New Bill")
        header_label.setStyleSheet("font-size: 30px; font-weight: 900; font-family: Comic Sans MS;")
        self.back_button = QPushButton("◀")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("font-size: 35px;")   
        header_layout.addWidget(self.back_button)
        header_layout.addWidget(header_label)
        self.back_button.clicked.connect(self.back_to_home)


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

        self.customers_file  = "customers.ini"
        # Right Layout
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignTop)

        self.current_customers = []
        config = ConfigParser()
        config.read(self.customers_file)
        self.current_customers = config.sections()

        self.layout_0  = QHBoxLayout()
        pixmap = QPixmap('./img/logo.png')
        pixmap = pixmap.scaled(90,70,aspectRatioMode=Qt.KeepAspectRatio)
        self.logol_label = QLabel()
        self.logol_label.setPixmap(pixmap)
        Data = QLabel("YAZ Lounge \n18 Mohammed Zaki St, El-Nozha, Cairo\nTel: +201115053137")
        Data.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.layout_0.addWidget(self.logol_label)
        self.layout_0.addWidget(Data)
        # Customer Name Input
        layout_1 = QHBoxLayout() 

        label_insert_name = QLabel("Client Name: ")
        label_insert_name.setStyleSheet("font-size: 15px; font-weight: bold;  border-radius: 5px; padding: 5px;")
        layout_1.addWidget(label_insert_name)
        self.customer_name_input = QComboBox()
        # self.customer_name_input.setFixedWidth(700)
        self.customer_name_input.addItems(['**Please Select a Customer**'] + self.current_customers)

        self.customer_name_input.setFixedHeight(40)
        self.customer_name_input.setStyleSheet("font-size: 15px; font-weight: bold; background-color: white; border: 1px solid grey; border-radius: 5px; padding: 5px;")
        # self.right_layout.addWidget(self.customer_name_input)
        self.right_layout.addLayout(self.layout_0)
        self.right_layout.addLayout(layout_1)
        
        layout_1.addWidget(self.customer_name_input)

        # Bill Table
        self.bill_table = QTableWidget()
        self.bill_table.setRowCount(0)
        self.bill_table.setColumnCount(5)
        self.bill_table.setHorizontalHeaderLabels(['Service', 'Price', 'Discount %', 'Total', ''])
        self.bill_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bill_table.setGridStyle(Qt.SolidLine)
        

        
        self.date_time_label = QLabel()
        self.date_time_label.setStyleSheet("font-size: 15px; ")
        self.date_time_label.setAlignment(Qt.AlignRight)            


        total_temp_w = QHBoxLayout() 
        # Total Price Label
        self.total_price_label = QLabel("Total Price: 0 EGP")
        self.total_price_label.setStyleSheet("font-size: 15px; ")
        self.right_layout.addLayout(total_temp_w)
        # self.right_layout.addWidget(self.total_price_label, alignment=Qt.AlignRight)
        self.right_layout.addWidget(self.bill_table)




        total_temp_w.addWidget(self.date_time_label)
        total_temp_w.addStretch() 
        total_temp_w.addWidget(self.total_price_label)


        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(200, 40)
        self.save_button.setStyleSheet("background-color: lightgrey; font-size: 20px; font-weight: bold;")
        self.right_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        self.save_button.clicked.connect(self.save_bill)
        # Combine Layouts

        container_layout = QHBoxLayout()
        container_layout.addLayout(self.main_layout)
        container_layout.addLayout(self.right_layout)

        self.setLayout(container_layout)

        self.current_bill_items = []  # To track bill items and their positions


        ## BIND 
        self.tab_widget.currentChanged.connect(self.update_current_tab)
        self.update_date_time()

    def update_date_time(self):
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.date_time_label.setText( current_datetime)

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



        self.bill_table.removeRow(row)
        self.update_total_and_items()  # Update the total price

        self.bind_new_rows()

    def update_total_and_items(self):
        self.current_bill_items = []
        for row in range(self.bill_table.rowCount()):
            item = self.bill_table.item(row,3).text()
            if item:
                item = float(item)
                self.current_bill_items.append(item)
        self.total_price = sum(self.current_bill_items)
        self.total_price_label.setText(f"Total Price: {self.total_price} EGP")

    def back_to_home(self):
        self.close()
        self.parent.showMaximized()


    def convert_image_to_pdf(self,image_path, pdf_path):
        # Create a canvas
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Draw the image on the canvas
        c.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])
        
        # Save the PDF
        c.save()
        
    def save_bill(self): 
        if self.total_price_label.text() ==  "Total Price: 0 EGP" or self.customer_name_input.currentText() == "**Please Select a Customer**":
            warning_msg = QMessageBox()
            warning_msg.setIcon(QMessageBox.Warning)
            warning_msg.setText("Please select customer and/or add at least one product")
            warning_msg.setWindowTitle("Warning")
            warning_msg.exec_()

        else:
            yaz = YAZ() 
            price = self.total_price_label.text() 

            name = self.customer_name_input.currentText() 
            name = name.replace(" ", "_")
            yaz.save_table_to_excel(self.bill_table,name)
            now = datetime.now()               
            date_str = now.strftime("%d/%m/%y")
            time_str = now.strftime("%H:%M:%S")
            unique_id = now.strftime("%d%m%y%H%M%S")
            
            retval = yaz.append_row_to_main_sheet([date_str, time_str, unique_id, "IN", f"{name.replace('_', ' ')}'s Bill", self.total_price,  self.user, "Notes"])
            if retval != True: 
                
                QMessageBox.warning(None, "Warning: File Access Error", retval + '\nPlease Close the file if it is open')
                app.exec_()
                return False
            ok_msg = QMessageBox()
            ok_msg.setIcon(QMessageBox.Information)
            ok_msg.setText(f"Bill for {name} Saved successfully")
            ok_msg.setWindowTitle("Saving")
            ok_msg.exec_()
            # Calculate screenshot dimensions and position
            combo_box_pos = self.customer_name_input.mapToGlobal(QPoint(0, 0))  # Global position of the combobox
            combo_box_size = self.customer_name_input.size()  # Size of the combobox

            total_price_pos = self.total_price_label.mapToGlobal(QPoint(0, 0))  # Global position of the total price label
            total_price_size = self.total_price_label.size()  # Size of the total price label

            table_pos = self.bill_table.mapToGlobal(QPoint(0, 0))  # Global position of the bill_table
            table_size = self.bill_table.size()  # Size of the bill_table

            logo_pos = self.logol_label.mapToGlobal(QPoint(0, 0))  # Global position of the logo label
            logo_size = self.logol_label.size()  # Size of the logo label

            # Calculate capture dimensions
            capture_x = min(combo_box_pos.x(), total_price_pos.x(), table_pos.x(), logo_pos.x())  # Leftmost edge of the widgets
            capture_y = min(combo_box_pos.y(), total_price_pos.y(), table_pos.y(), logo_pos.y())  # Topmost edge of the widgets
            capture_width = max(combo_box_pos.x() + combo_box_size.width(),
                                total_price_pos.x() + total_price_size.width(),
                                table_pos.x() + table_size.width(),
                                logo_pos.x() + logo_size.width()) - capture_x  # Width to include all widgets
            capture_height = table_pos.y() + table_size.height() - capture_y  # Height to include all widgets

            # Take a screenshot of the specified region
            screenshot = QGuiApplication.primaryScreen().grabWindow(
                QApplication.desktop().winId(), 
                capture_x, capture_y, capture_width, capture_height
            )

 

            # yaz.save_table_to_excel(self.bill_table,name)
            now = datetime.now()               
            date_str = date_str.replace("/","_")
            time_str = time_str.replace(":","_") 
            name = str(name)
            image_path = ".//" + "Customers Bills" + "//" + name +"//"+ f"{name}_{date_str}_{time_str}.jpg"
            pdf_path = ".//" + "Customers Bills" + "//" + name +"//"+ f"{name}_{date_str}_{time_str}.pdf"
            screenshot.save(image_path)
            self.convert_image_to_pdf(image_path, pdf_path)
            os.remove(image_path)
            self.bill_table.setRowCount(0)
            self.customer_name_input.setCurrentIndex(0)


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
    window = NewBillPage('','asdas')

    window.showMaximized()
    sys.exit(app.exec_())
