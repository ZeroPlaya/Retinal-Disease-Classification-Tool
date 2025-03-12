import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import Slot
from PySide6.QtUiTools import QUiLoader  # To load .ui file
import resources_rc  # Ensure this is imported in your main script

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("retina.ui", self)  # Ensure retina.ui is in the correct path
        self.setCentralWidget(self.ui)

        self.setFixedSize(720, 512)  # Set a fixed window size

        # Connect button actions
        self.ui.getStartedButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.uploadBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.historyBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.historyButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.classificationBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))

        # Connect file upload button to file explorer (and only switch pages if a file is selected)
        self.ui.uploadImageButton.clicked.connect(self.open_file_explorer)


        # Image embeds


    @Slot()
    def open_file_explorer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "All Files (*)")
        if file_path:  # Only switch pages if a file is chosen
            print(f"Selected file: {file_path}")
            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
