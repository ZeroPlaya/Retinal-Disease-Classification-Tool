from PySide6.QtWidgets import QMainWindow
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
