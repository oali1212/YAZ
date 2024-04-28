import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QToolBar, QAction

class MyApp(QMainWindow):  # Changed to inherit from QMainWindow to support adding a toolbar
    def __init__(self):
        super().__init__()

        # Create a central widget
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        # Create the main layout
        mainLayout = QVBoxLayout(centralWidget)

        # Create two horizontal layouts for the button rows
        topRowLayout = QHBoxLayout()
        bottomRowLayout = QHBoxLayout()

        # Create and add buttons to the top row layout
        for i in range(1, 4):  # Services A, B, C
            button = QPushButton(f"Service {chr(64+i)}")  # ASCII 65 is 'A'
            button.setFixedSize(100, 100)  # Makes the buttons square
            topRowLayout.addWidget(button)

        # Create and add buttons to the bottom row layout
        --------p
        for i in range(4, 7):  # Services D, E, F
            button = QPushButton(f"Service {chr(64+i)}")  # Continuing ASCII for 'D'
            button.setFixedSize(100, 100)  # Makes the buttons square
            bottomRowLayout.addWidget(button)

        # Add the two rows of buttons to the main layout
        mainLayout.addLayout(topRowLayout)
        mainLayout.addLayout(bottomRowLayout)

        # Create the QTableWidget for the bottom part
        tableWidget = QTableWidget()
        tableWidget.setRowCount(10)  # 10 rows
        tableWidget.setColumnCount(3)  # Example column count
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(tableWidget.rowCount()):
            for j in range(tableWidget.columnCount()):
                tableWidget.setItem(i, j, QTableWidgetItem(f"Item {i+1},{j+1}"))

        # Add the table widget to the main layout
        mainLayout.addWidget(tableWidget)

        # Create a toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Create actions for the toolbar
        manageUsersAction = QAction("Manage Users", self)
        manageServicesAction = QAction("Manage Services", self)

        # Optionally, connect the actions to methods
        manageUsersAction.triggered.connect(self.manageUsers)
        manageServicesAction.triggered.connect(self.manageServices)

        # Add actions to the toolbar
        self.toolbar.addAction(manageUsersAction)
        self.toolbar.addAction(manageServicesAction)

    def manageUsers(self):
        # Placeholder method for managing users
        print("Manage Users clicked")

    def manageServices(self):
        # Placeholder method for managing services
        print("Manage Services clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
