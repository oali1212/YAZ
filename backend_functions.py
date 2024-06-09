import openpyxl
import openpyxl.reader
from openpyxl.utils import get_column_letter
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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
        tableWidget.setColumnCount(5)
        tableWidget.setHorizontalHeaderLabels(['Service', 'Price (EGP)', 'Price -30%', 'Price -40%', "Remove"])
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


            tableWidget.setItem(i, 0, QTableWidgetItem(service))
            price = str(price)
            price_discounted_30 = str(price_discounted_30)
            price_discounted_40 = str(price_discounted_40)
            tableWidget.setItem(i, 1, QTableWidgetItem(price))
            tableWidget.setItem(i, 2, QTableWidgetItem(price_discounted_30))
            tableWidget.setItem(i, 3, QTableWidgetItem(price_discounted_40))
            tableWidget.setCellWidget(i,4,self.remove)


        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        tableWidget.setStyleSheet("background-color: white;")
        # Enable resizing of columns by mouse
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # Set the horizontal header resize mode to Stretch
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set the vertical header resize mode to Stretch
        tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    


        tableWidget.setFixedWidth(1100)
        self.disable_modification(tableWidget)
        return tableWidget
    

    def create_customers_table(self, ini_file):
        tableWidget = QTableWidget()
        tableWidget.setStyleSheet("background-color: white;")

        # Load data from ini file
        config = ConfigParser()
        config.read(ini_file)

        # Set table properties
        tableWidget.setColumnCount(6)
        tableWidget.horizontalHeader().setFont(QFont('Arial', 12, QFont.Bold))
        tableWidget.horizontalHeader().setStyleSheet("background-color: lightgrey; font-weight: bold; font-size: 12px;")
        tableWidget.verticalHeader().setVisible(False)

        # Iterate over each section (customer) in the INI file
        for section in config.sections():
            # Retrieve all options for the current section
            options = [section] + [config[section][option] for option in config[section]]
            # Append options to the table as a new row
            row_position = tableWidget.rowCount()
            tableWidget.insertRow(row_position)
            for j, option in enumerate(options):
                item = QTableWidgetItem(option)
                tableWidget.setItem(row_position, j, item)

        # Set table dimensions and properties
        tableWidget.setRowCount(tableWidget.rowCount())  # Ensure proper row count
        tableWidget.setHorizontalHeaderLabels(["Name", "#", "Last Date Vistied", "Phone Number", "Total Paid", "Email", "Heard about us from:"])
        tableWidget.setFixedWidth(1100)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        return tableWidget


    def disable_modification(self, table):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)


    def add_service(self, ini_file, section, name, price):

        config = ConfigParser()
        config.read(ini_file)
        
        if not config.has_section(section):
            config.add_section(section)
        
        if name[-1] == "_":
            name = name[:-2]

        config.set(section, name, str(price))
        
        with open(ini_file, 'w') as config_file:
            config.write(config_file)




    def delete_service(self, file_path, section, index):
        index = int(index)
        config = ConfigParser()
        config.read(file_path)

        if section not in config:
            raise ValueError(f"Section '{section}' not found in the INI file.")

        options = list(config[section])
        if index < 1 or index > len(options):
            raise ValueError("Invalid index.")

        option_to_delete = options[index - 1]  # Adjust index to 0-based index
        del config[section][option_to_delete]

        with open(file_path, 'w') as configfile:
            config.write(configfile)

    def save_services(self, file_path, section, prices_list: list):
        config = ConfigParser()
        config.read(file_path)

        if section not in config:
            raise ValueError(f"Section '{section}' not found in the INI file.")
        
        options = list(config[section])
        
        if len(options) != len(prices_list):
            raise ValueError("Length of prices list does not match the number of options in the section.")
        
        for index, price in enumerate(prices_list):
            option_to_edit = options[index]  # Zero-based index
            config[section][option_to_edit] = str(price)
        
        # Write changes back to the file
        with open(file_path, 'w') as configfile:
            config.write(configfile)