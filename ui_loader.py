from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from handlers import ButtonHandlers  # Import handlers for button logic
import resources_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("ui/retina.ui", self)  # Load UI from the `ui` folder
        self.setCentralWidget(self.ui)

        self.setFixedSize(720, 512)  # Set a fixed window size

        # Initialize button handlers
        self.handlers = ButtonHandlers(self.ui)
        self.setup_table()

    def setup_table(self):
        """Configure the history table with a fixed layout (no resizing)."""
        self.table = self.ui.historyTable  # Ensure this matches your .ui object name
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Preview", "ID", "Patient Name", "Results", "Date", "Comment"])

        # Set a fixed width for the table
        self.table.setFixedWidth(631)  # Locks table width at 631 pixels

        # Adjust column widths to fit within 631 pixels
        column_widths = [94, 67, 107, 123, 92, 146]  # Predefined column widths
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)

        # Disable column resizing
        header = self.table.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.Fixed)  # Prevents column resizing

        # Disable row resizing
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Locks row heights

        # Apply bold font to column headers
        header_font = QFont()
        header_font.setBold(True)
        self.table.horizontalHeader().setFont(header_font)

        # Set header and row formatting
        self.table.setStyleSheet(
            """
            QHeaderView::section {
                background-color: #ffffff;
                color: black;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #dcdcdc;
            }

            QTableView {
                background-color: #ffffff;
                color: black;
                font-weight: normal;
                gridline-color: #dcdcdc;
                selection-background-color: #e0f0ff;  /* Light blue row highlight */
                selection-color: black;
            }

            QTableView::item {
                padding: 6px;
                border-left: 1px solid #dcdcdc;
            }

            QTableView::item:selected {
                background-color: #e0f0ff;
                color: black;
            }

            QTableView::selection {
                background-color: #e0f0ff;
            }

            QTableView::item:focus {
                outline: none;  /* Remove focus rectangle */
            }
            """
        )

        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Select full rows
        self.table.setSelectionMode(QTableWidget.SingleSelection)  # One row at a time
        self.table.setFocusPolicy(Qt.NoFocus)  # Disable focus outline


        # Hide row numbers
        self.table.verticalHeader().setVisible(False)

        # Make the table read-only
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Sample Data
        sample_data = [
            ["", "001", "John Doe", "DR, MYA, ARMD", "2025-03-16", "First visit"],
            ["", "002", "Jane Smith", "MYA, TSLN, CRVO", "2025-03-15", "Needs follow-up"],
            ["", "003", "Alice Johnson", "NORMAL", "2025-03-14", "Regular checkup"],
        ]

        # Insert rows with sample data
        self.table.setRowCount(len(sample_data))  # Set the number of rows
        for row_idx, row_data in enumerate(sample_data):
            for col_idx, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)  # Center-align text
                self.table.setItem(row_idx, col_idx, item)
