import sys
from PySide6.QtWidgets import QApplication
from ui_loader import MainWindow  # Import MainWindow from ui_loader

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Refresh the table to show only non-archived records
    window.handlers.refresh_history_table(show_archived=False)

    # Set the main widget's background to transparent
    window.setStyleSheet("QWidget#RetinalDiseaseClassifier { background: transparent; }")

    sys.exit(app.exec())
    