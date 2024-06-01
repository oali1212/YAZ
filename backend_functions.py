import openpyxl
import openpyxl.reader
from openpyxl.utils import get_column_letter
import datetime
import os
import configparser
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

    def create_performance_sheet():
        pass
    def add_to_performance_sheet():
        pass
    def remove_from_performance_sheet():
        pass
    


    def add_worker():
        pass

    def remove_worker():
        pass
    
    def add_service():
        pass
    
    def remove_service():
        pass

yaz = YAZ()
yaz.create_main_sheet(yaz.main_sheet_titles)
yaz.add_to_main_sheet([1,2,3,4,5,6,1,8,9])
yaz.add_to_main_sheet([1,1,3,4,5,1,7,1,9])
yaz.add_to_main_sheet([1,2,1,4,1,6,7,8,9])
yaz.add_to_main_sheet([1,2,3,'safagvdsavgdasvgdasf',5,6,7,8,9])
yaz.remove_from_main_sheet(12)