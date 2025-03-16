from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Slot

class ButtonHandlers:
    def __init__(self, ui):
        self.ui = ui
        self.connect_buttons()

    def connect_buttons(self):
        """Connect all button actions."""
        self.ui.getStartedButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.uploadBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.historyBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.historyButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.classificationBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.uploadImageButton.clicked.connect(self.open_file_explorer)

    @Slot()
    def open_file_explorer(self):
        """Opens a file dialog and switches pages if a file is selected."""
        file_path, _ = QFileDialog.getOpenFileName(None, "Select a File", "", "All Files (*)")
        if file_path:
            print(f"Selected file: {file_path}")
            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page
