import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui_loader import MainWindow
import os  # Import os to handle relative paths

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Retinal Disease Detection Tool")
    
    # Use a relative path for the icon to ensure PyInstaller compatibility
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_path, "assets", "Icon.ico")
    app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    # Set the main widget's background to transparent
    window.setStyleSheet("QWidget#RetinalDiseaseClassifier { background: transparent; }")

    # Refresh the history table on startup
    window.handlers.refresh_history_table()

    sys.exit(app.exec())

