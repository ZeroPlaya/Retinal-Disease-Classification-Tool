import os
import sys
from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from handlers import ButtonHandlers  # Import handlers for button logic
import resources_rc
from database import DatabaseManager  # Import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()

        # Adjust path resolution for PyInstaller
        if getattr(sys, 'frozen', False):  # Check if running in a PyInstaller bundle
            base_path = sys._MEIPASS  # Temporary folder created by PyInstaller
        else:
            base_path = os.path.dirname(__file__)

        # Load the .ui file and assign it to self.ui
        ui_file_path = os.path.join(base_path, "ui", "retina.ui")
        self.ui = loader.load(ui_file_path, self)

        # Set the loaded UI as the central widget
        self.setCentralWidget(self.ui)

        self.setFixedSize(720, 512)  # Set a fixed window size
        self.handlers = ButtonHandlers(self.ui)
        self.db_manager = DatabaseManager()  # Initialize DatabaseManager
        
        self.setup_table()

    def setup_table(self):
        """Configure the history table and populate it with data from MongoDB."""
        self.table = self.ui.historyTable  # Ensure this matches your .ui object name
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Preview", "File", "Patient Name", "Results", "Date", "Comment"])

        # Adjust column widths to fit within 631 pixels
        column_widths = [94, 73, 107, 123, 92, 120]  # Predefined column widths
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)

        # Disable column resizing
        header = self.table.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.Fixed)  # Prevents column resizing

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Locks row heights
        self.table.verticalHeader().setVisible(False)

        # Apply bold font to column headers
        header_font = QFont()
        header_font.setBold(True)
        self.table.horizontalHeader().setFont(header_font)

        # Set table styling
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

            QScrollBar:vertical {
                background-color: #f1f1f1;
                width: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background-color: #888;
                border-radius: 6px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #555;
            }

            QScrollBar:horizontal {
                background-color: #f1f1f1;
                height: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:horizontal {
                background-color: #888;
                border-radius: 6px;
                min-width: 20px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #555;
            }
            """
        )

        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Select full rows
        self.table.setSelectionMode(QTableWidget.SingleSelection)  # One row at a time
        self.table.setFocusPolicy(Qt.NoFocus)  # Disable focus outline

        # Make the table read-only
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Enable smooth scrolling
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)

        # Fetch data from MongoDB
        if self.db_manager.collection is not None:  # Explicitly check if collection is not None
            records = list(self.db_manager.collection.find())  # Convert cursor to list
        else:
            records = []

        self.table.setRowCount(len(records))

        for row_idx, record in enumerate(records):
            # Load and resize image for each row
            image_path = record.get("image_path", "")
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Insert image in first column
            image_item = QTableWidgetItem()
            image_item.setData(Qt.DecorationRole, scaled_pixmap)  # Set image as decoration
            image_item.setData(Qt.UserRole, image_path)  # Store the file path in a custom data role
            self.table.setItem(row_idx, 0, image_item)

            # Insert other data into columns
            file_name = record.get("file_name", "")
            patient_name = record.get("patient_name", "")
            diagnosis = ", ".join(record.get("diagnosis", {}).keys())  # Join disease names without confidence scores
            date = record.get("date", "")
            notes = record.get("notes", "")

            row_data = [file_name, patient_name, diagnosis, date, notes]
            for col_idx, text in enumerate(row_data, start=1):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)
