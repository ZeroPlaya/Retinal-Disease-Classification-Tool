import sys
from PySide6.QtWidgets import QApplication
from ui_loader import MainWindow  # Import MainWindow from ui_loader

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
