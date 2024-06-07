import openpyxl
import openpyxl.reader
from openpyxl.utils import get_column_letter
import os
import sys
from PyQt5.QtWidgets import *
from configparser import ConfigParser
from PyQt5.QtGui import QFont
import math


class YAZ:


    def __init__(self): 
        self.main_sheet_titles = ["Date", "Time", "Service","Sub Service", "Extras", "Price EGP", "Discount %", "Notes",  "Operator"]
        self.workers_sheet = ["worker_A", "Worker_B", "Worker_C"]
        self.services_list = ["Service_A", "Service_B", "Service_B"]
        self.main_sheet_name = "main_sheet.xlsx"

    def adjust_cell_width(self,sheet):
        
        # Autofit column width
        for column in sheet.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2  # Adjusted width with a little buffer
            sheet.column_dimensions[column_letter].width = adjusted_width

        
    def create_main_sheet(self, column_names):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Write column headers
        for idx, column_name in enumerate(column_names, start=1):
            cell = sheet.cell(row=1, column=idx, value=column_name)
            cell.font = cell.font.copy(bold=True)
            cell.fill = openpyxl.styles.fills.PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")

        # Save the file
        self.adjust_cell_width(sheet)
        workbook.save(self.main_sheet_name)


    def add_to_main_sheet(self, entry, index = None):


        if not self.main_sheet_name in os.listdir(): 
            print("Main sheet not found!")
            return False
        
        workbook = openpyxl.load_workbook(filename=self.main_sheet_name)
        sheet = workbook.active
        valid_columns = sheet.max_column
        valid_rows = sheet.max_row


        if valid_columns == 0 or valid_rows == 0 : 
            print(f"Main sheet has no data! \nrows = {valid_rows}, columns = {valid_columns}")
            return False
  
        elif len(entry) != valid_columns:
            print(f"Entry length must be equal to the number of titles! \nentry length = {len(entry)}, titles = {valid_columns}")
            return False

        else:
            for col, value in enumerate(entry, start=1):
                if not index: 
                    cell = sheet.cell(row=valid_rows+1, column=col, value=value)
                    print(f"putting {value} in row = {valid_rows+1} and column = {col}")
                else:
                    cell = sheet.cell(row=index, column = col, value = value)
                    print(f"putting {value} in row = {index} and column = {col}")
                

            self.adjust_cell_width(sheet)
            workbook.save(self.main_sheet_name)


    def remove_from_main_sheet(self, index):
        if not self.main_sheet_name in os.listdir(): 
            print("Main sheet not found!")
            return False
        
        workbook = openpyxl.load_workbook(filename=self.main_sheet_name)
        sheet = workbook.active
        valid_columns = sheet.max_column
        valid_rows = sheet.max_row

        if index > valid_rows:
            print("The row requested to delete does not exist!")
            return False
        else:
            self.add_to_main_sheet([""]*valid_columns,index = 3)


    def create_price_table(self, ini_file, section):
        config = ConfigParser()
        config.read(ini_file)
        
        if section not in config:
            print(f"Section {section} not found in the INI file.")
            return None
        
        # Assuming services are stored in a "key = value" format under section
        services = config[section]
        
        # Create Table
        tableWidget = QTableWidget()
        
        # Set table dimensions
        tableWidget.setRowCount(len(services))
        tableWidget.setColumnCount(6)
        tableWidget.setHorizontalHeaderLabels(['Service', 'Price (EGP)', 'Price -30%', 'Price -40%', "Edit", "Remove"])
        tableWidget.horizontalHeader().setStyleSheet("font-weight: bold; font-size:25px; background-color: lightgrey;")
        # Hide the vertical header (numbers column)
        tableWidget.verticalHeader().setVisible(False)

        font = QFont()
        font.setPointSize(25)
        for i, (service, price) in enumerate(services.items()):
            price = float(price)
            price_discounted_30 = math.ceil( price * 0.7 )
            price_discounted_40 = math.ceil( price * 0.6 )
            
            service = service.replace("__", " + ")
            service = service.replace("_", " ")
            service = service.upper()

            self.remove = QPushButton("🗑")
            self.remove.setStyleSheet("font-size:25px;")
            self.edit = QPushButton("🖋️") 
            self.edit.setStyleSheet("font-size: 25px;")  

            tableWidget.setItem(i, 0, QTableWidgetItem(service))
            price = str(price)
            price_discounted_30 = str(price_discounted_30)
            price_discounted_40 = str(price_discounted_40)
            tableWidget.setItem(i, 1, QTableWidgetItem(price))
            tableWidget.setItem(i, 2, QTableWidgetItem(price_discounted_30))
            tableWidget.setItem(i, 3, QTableWidgetItem(price_discounted_40))
            tableWidget.setCellWidget(i,4,self.edit)
            tableWidget.setCellWidget(i,5,self.remove)


        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        tableWidget.setStyleSheet("background-color: white;")
        # Enable resizing of columns by mouse
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # Set the horizontal header resize mode to Stretch
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set the vertical header resize mode to Stretch
        tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    


        tableWidget.setFixedWidth(1100)

        return tableWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ini_file = 'settings.ini'  # replace with the path to your INI file
    section = 'nails'
    yaz = YAZ()
    table = yaz.create_price_table(ini_file, section)
    if table:
        # If you want to test showing the table, uncomment the following lines:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(table)
        widget.setLayout(layout)
        widget.show()
        sys.exit(app.exec_())
        