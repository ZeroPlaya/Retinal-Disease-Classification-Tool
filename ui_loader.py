from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from handlers import ButtonHandlers  # Import handlers for button logic
import rc_resources  # Resource file if you're using icons, etc.

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

        # Set the table to have 7 columns (the last column will store the record ID)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Preview", "File", "Patient Name", "Results", "Date", "Comment", "RecordID"
        ])

        # Optionally, hide the RecordID column so it's not visible to the user
        self.table.setColumnHidden(6, True)

        # Adjust column widths as needed (adjust the first 6 columns)
        column_widths = [94, 73, 107, 123, 92, 120]
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)

        # Disable column resizing for consistency
        header = self.table.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.Fixed)

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
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

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)

        # Start with an empty table (no rows)
        self.table.setRowCount(0)
