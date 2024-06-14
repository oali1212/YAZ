from openpyxl import Workbook, load_workbook 
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from configparser import ConfigParser
from PyQt5.QtGui import QFont
import math
from datetime import datetime
import pandas as pd


class YAZ:


    def __init__(self): 


        self.main_sheet_titles = ["Date", "Time", "Unique ID", "Transaction Type", "Transaction Description","Amount (EGP)",  "Notes",  "Logged by:"]


    def create_main_sheet(self):
        # Define the path to save the workbook
        file_path = './Customers Bills/main_sheet.xlsx'
        
        # Create a workbook and select the active worksheet
        wb = Workbook()
        ws = wb.active
        
        # Set the title of the worksheet
        ws.title = "Main Sheet"
        
        # Add the titles to the first row
        for col_num, title in enumerate(self.main_sheet_titles, 1):
            ws.cell(row=1, column=col_num, value=title)
        
        # Save the workbook
        wb.save(file_path)

    def append_row_to_main_sheet(self, row_data):
        # Define the path to save the workbook
        directory_path = './Customers Bills'
        file_path = os.path.join(directory_path, 'main_sheet.xlsx')
        
        # Check if the row has the correct length
        if len(row_data) != len(self.main_sheet_titles):
            return False
        
        # Check if the workbook exists, if not create it
        if not os.path.exists(file_path):
            self.create_main_sheet()
        
        # Load the workbook and select the active worksheet
        wb = load_workbook(file_path)
        ws = wb.active
        
        # Append the row data
        ws.append(row_data)
        
        # Save the workbook
        wb.save(file_path)
        
        return True

    def delete_row_by_id(self, value):
        # Define the path to save the workbook
        directory_path = './Customers Bills'
        file_path = os.path.join(directory_path, 'main_sheet.xlsx')
        
        # Check if the workbook exists
        if not os.path.exists(file_path):
            #print("Workbook does not exist.")
            return False
        
        # Load the workbook and select the active worksheet
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        
        # Iterate over the rows to find the value in the second column
        row_to_delete = None
        for row in ws.iter_rows(min_row=2, max_col=3, values_only=False):
            if row[1].value == value:
                row_to_delete = row[0].row
                break
        
        # If a matching row is found, delete it
        if row_to_delete:
            ws.delete_rows(row_to_delete)
            wb.save(file_path)
            return True
        else:
            #print("Value not found.")
            return False

    def create_price_table(self, ini_file, section):
        config = ConfigParser()
        config.read(ini_file)
        
        if section not in config:
            ##print(f"Section {section} not found in the INI file.")
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
                
                    ##print(config.sections())
            # Write the updated data back to the INI file
            #print(ini_file)
            with open(ini_file, 'w') as configfile:
                
                config.write(configfile)
                ##print(f"INI file '{ini_file}' updated successfully.")

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
        #print(f"File saved as {file_path}")

# yaz = YAZ() s
# yaz.create_main_sheet()
# yaz.append_row_to_main_sheet([1,2223232,3,4,5,6,7,8])
# yaz.append_row_to_main_sheet([1,2222,3,4,5,6,7,8])
# yaz.delete_row_by_id(2222)