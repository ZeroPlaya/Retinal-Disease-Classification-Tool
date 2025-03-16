from PySide6.QtWidgets import QFileDialog, QLabel, QDialog, QVBoxLayout
from PySide6.QtCore import Slot, Qt  # Import Qt
from PySide6.QtGui import QPixmap, QPainter

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked = None

    def mousePressEvent(self, event):
        if self.clicked:
            self.clicked(event)

class ButtonHandlers:
    def __init__(self, ui):
        self.ui = ui
        self.connect_buttons()

    def connect_buttons(self):
        """0 = titlepage, 1 = selectionpage, 2 = classificationpage, 3 = historypage""" 
        self.ui.getStartedButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.uploadBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.historyBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.historyButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.classificationBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.uploadImageButton.clicked.connect(self.open_file_explorer)
        self.ui.historyTable.itemDoubleClicked.connect(self.on_row_double_clicked)  # Connect double-click signal

        # Replace the existing QLabel with ClickableLabel
        old_label = self.ui.imagePlaceholder
        self.ui.imagePlaceholder = ClickableLabel(old_label.parent())
        self.ui.imagePlaceholder.setGeometry(10, 75, 390, 292)  # Set the geometry to the specified values
        self.ui.imagePlaceholder.setObjectName(old_label.objectName())
        self.ui.imagePlaceholder.clicked = self.open_image_preview  # Connect click event

    @Slot()
    def open_file_explorer(self):
        """Opens a file dialog and switches pages if a file is selected."""
        file_path, _ = QFileDialog.getOpenFileName(None, "Select a File", "", "All Files (*)")
        if file_path:
            print(f"Selected file: {file_path}")
            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page

    @Slot()
    def on_row_double_clicked(self, item):
        """Switch to the classification page when a row is double-clicked and set the image."""
        row = item.row()
        image_path = self.ui.historyTable.item(row, 0).data(Qt.UserRole)  # Get the file path from the custom data role
        if image_path:
            pixmap = QPixmap(image_path)
            label_size = self.ui.imagePlaceholder.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Create a new pixmap with the label's size and fill it with a transparent background
            final_pixmap = QPixmap(label_size)
            final_pixmap.fill(Qt.transparent)

            # Draw the scaled pixmap centered within the final pixmap
            painter = QPainter(final_pixmap)
            x = (label_size.width() - scaled_pixmap.width()) // 2
            y = (label_size.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
            painter.end()

            self.ui.imagePlaceholder.setPixmap(final_pixmap)
            self.ui.imagePlaceholder.setScaledContents(False)  # Ensure QLabel does not scale the pixmap further
            self.ui.imagePlaceholder.setProperty("imagePath", image_path)  # Store the image path in the QLabel
        self.ui.stackedWidget.setCurrentIndex(2)

    @Slot()
    def open_image_preview(self, event):
        """Open a larger preview of the image when the imagePlaceholder is clicked."""
        image_path = self.ui.imagePlaceholder.property("imagePath")
        if image_path:
            pixmap = QPixmap(image_path)
            dialog = QDialog(self.ui)
            dialog.setWindowTitle("Image Preview")
            layout = QVBoxLayout(dialog)
            label = QLabel(dialog)
            max_width = 800  # Set a maximum width for the preview
            scaled_pixmap = pixmap.scaled(max_width, max_width, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled_pixmap)
            layout.addWidget(label)
            dialog.setLayout(layout)
            dialog.setFixedSize(dialog.sizeHint())  # Set fixed size based on the content

            dialog.exec()
