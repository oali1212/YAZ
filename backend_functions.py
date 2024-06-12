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
from datetime import datetime
import pandas as pd


class YAZ:


    def __init__(self): 
        self.main_sheet_titles = ["Date", "Time", "Transaction Type", "Transaction Description","Amount (EGP)",  "Notes",  "Logged by:"]

        self.main_sheet_directory = "Main Report and Performance"
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
        excel_path = os.path.join(self.main_sheet_directory, self.main_sheet_name)
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for idx, column_name in enumerate(column_names, start=1):
            cell = sheet.cell(row=1, column=idx, value=column_name)
            cell.font = cell.font.copy(bold=True)
            cell.fill = openpyxl.styles.fills.PatternFill(start_color="DDDDDD", end_color="DDDDDD",
                                                           fill_type="solid")

        self.adjust_cell_width(sheet)
        workbook.save(self.main_sheet_name)


    def add_to_main_sheet(self, entry, index=None):
        excel_path = os.path.join(self.main_sheet_directory, self.main_sheet_name)

        if not os.path.exists(excel_path):
            self.create_main_sheet(self.main_sheet_titles)

        workbook = openpyxl.load_workbook(filename=excel_path)
        sheet = workbook.active
        valid_columns = sheet.max_column
        valid_rows = sheet.max_row

        if valid_columns == 0 or valid_rows == 0:
            print(f"Main sheet has no data! Rows: {valid_rows}, Columns: {valid_columns}")
            return False

        elif len(entry) != valid_columns:
            print(f"Entry length must be equal to the number of titles! Entry length: {len(entry)}, Titles: {valid_columns}")
            return False

        else:
            if not index:
                row = valid_rows + 1
            else:
                row = index

            for col, value in enumerate(entry, start=1):
                sheet.cell(row=row, column=col, value=value)

            self.adjust_cell_width(sheet)
            workbook.save(excel_path)
            print("Entry appended successfully.")
            return True


    def remove_from_main_sheet(self, index):
        if not self.main_sheet_name in os.listdir(): 
            #print("Main sheet not found!")
            return False
        
        workbook = openpyxl.load_workbook(filename=self.main_sheet_name)
        sheet = workbook.active
        valid_columns = sheet.max_column
        valid_rows = sheet.max_row

        if index > valid_rows:
            #print("The row requested to delete does not exist!")
            return False
        else:
            self.add_to_main_sheet([""]*valid_columns,index = 3)


    def create_price_table(self, ini_file, section):
        config = ConfigParser()
        config.read(ini_file)
        
        if section not in config:
            #print(f"Section {section} not found in the INI file.")
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
        tableWidget.setColumnCount(7)
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

    def update_ini_from_table(self,tableWidget, ini_file):
        # Initialize ConfigParser
        config = ConfigParser()
        
        # Iterate over each row in the table
        for row in range(tableWidget.rowCount()):
            # Get the section name (first column)
            if tableWidget.item(row,0):
                section = tableWidget.item(row, 0).text()
                if section != '' and section != ' ':
                    config[section] = {}

                    # Populate the rest of the options
                    config[section]['Index'] = tableWidget.item(row, 1).text()
                    config[section]['date_registered'] = tableWidget.item(row, 2).text()
                    config[section]['phone_number'] = tableWidget.item(row, 3).text()
                    config[section]['total_paid'] = tableWidget.item(row, 4).text()
                    config[section]['email'] = tableWidget.item(row, 5).text()
                    config[section]['heard_about_us'] = tableWidget.item(row, 6).text()
                
                    #print(config.sections())
            # Write the updated data back to the INI file
            with open(ini_file, 'w') as configfile:
                config.write(configfile)
                #print(f"INI file '{ini_file}' updated successfully.")



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



    def save_table_to_excel(self, table: QTableWidget, name: str):
        # Convert QTableWidget to pandas DataFrame
        data = []
        for row in range(table.rowCount()):
            row_data = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                row_data.append(item.text() if item is not None else '')
            data.append(row_data)
        
        headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
        df = pd.DataFrame(data, columns=headers)
        
        # Check if folder for Customers Bills exists, if not create it
        customers_bills_folder = "Customers Bills"
        if not os.path.exists(customers_bills_folder):
            os.makedirs(customers_bills_folder)
        
        # Check if folder for the customer exists, if not create it
        customer_folder = os.path.join(customers_bills_folder, name)
        if not os.path.exists(customer_folder):
            os.makedirs(customer_folder)
        
        # Save with a timestamped name
        timestamp = datetime.now().strftime("%d_%m_%y_%H_%M")
        file_name = f"{name}_{timestamp}.xlsx"
        file_path = os.path.join(customer_folder, file_name)
        df.to_excel(file_path, index=False)
        print(f"File saved as {file_path}")

# yaz = YAZ() 
# yaz.add_to_main_sheet("main_sheet",["01/01/2022","22:22", "IN", "Mohamed Ahmed's bill", "", "moh"])