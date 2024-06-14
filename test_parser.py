import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from configparser import ConfigParser

class PriceTableWidget(QWidget):
    def __init__(self, ini_file, section):
        super().__init__()
        self.ini_file = ini_file
        self.section = section
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Price Table')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Create Table
        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)
        
        self.setLayout(layout)
        
        self.loadData()

    def loadData(self):
        config = ConfigParser()
        config.read(self.ini_file)
        
        if self.section not in config:
            ##print(f"Section {self.section} not found in the INI file.")
            return
        
        # Assuming services are stored in a "key = value" format under section
        services = config[self.section]
        
        # Set table dimensions
        self.tableWidget.setRowCount(len(services))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Service', 'Price (EGP)', 'Price -30%', 'Price -40%'])
        
        for i, (service, price) in enumerate(services.items()):
            price = float(price)
            price_discounted_30 = price * 0.7
            price_discounted_40 = price * 0.6
            
            service = service.replace("__", " & ")
            service = service.replace("_", " ")
            service = service.upper()
            self.tableWidget.setItem(i, 0, QTableWidgetItem(service))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(f"{price:.2f}"))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(f"{price_discounted_30:.2f}"))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(f"{price_discounted_40:.2f}"))

def main(ini_file, section):
    app = QApplication(sys.argv)
    ex = PriceTableWidget(ini_file, section)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    ini_file = 'settings.ini'  # replace with the path to your INI file
    section = 'nails'
    main(ini_file, section)
