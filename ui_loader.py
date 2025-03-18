from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from handlers import ButtonHandlers  # Import handlers for button logic
import resources_rc
from database import sample_data, image_paths  # Import sample data and image paths

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("ui/retina.ui", self)  # Load UI from the `ui` folder
        self.setCentralWidget(self.ui)

        self.setFixedSize(720, 512)  # Set a fixed window size
        self.handlers = ButtonHandlers(self.ui)
        
        self.setup_table()

    def setup_table(self):
        """Configure the history table with a fixed layout (no resizing)."""
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

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
                width: 0px;
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

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                height: 0px;
                width: 0px;
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

        self.table.setRowCount(len(sample_data))

        for row_idx, row_data in enumerate(sample_data):
            # Load and resize image for each row
            pixmap = QPixmap(image_paths[row_idx])
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Insert image in first column
            image_item = QTableWidgetItem()
            image_item.setData(Qt.DecorationRole, scaled_pixmap)  # Set image as decoration
            image_item.setData(Qt.UserRole, image_paths[row_idx])  # Store the file path in a custom data role
            self.table.setItem(row_idx, 0, image_item)

            # Insert other data into columns
            for col_idx, text in enumerate(row_data[1:], start=1):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

