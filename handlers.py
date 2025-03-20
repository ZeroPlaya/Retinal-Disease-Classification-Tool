from PySide6.QtWidgets import QFileDialog, QLabel, QDialog, QVBoxLayout, QWidget
from PySide6.QtCore import Slot, Qt, QEvent  # Import Qt and QEvent
from PySide6.QtGui import QPixmap, QPainter, QCursor, QFont, QKeySequence, QShortcut  # Import QShortcut from PySide6.QtGui
from datetime import datetime  # Import datetime for date formatting

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked = None
        self.setCursor(QCursor(Qt.PointingHandCursor))  # Set cursor to pointing hand

    def mousePressEvent(self, event):
        if self.clicked:
            self.clicked(event)

class TransparentLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # Set transparent background

class ButtonHandlers:
    def __init__(self, ui):
        self.ui = ui
        self.current_row = 0  # Track the current row for navigation
        self.connect_buttons()
        self.setup_shortcuts()  # Setup shortcuts

    def connect_buttons(self):
        """0 = titlepage, 1 = selectionpage, 2 = classificationpage, 3 = historyview, 4 = historypage"""
        self.ui.getStartedButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.uploadBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.historyBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.historyButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.classificationBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.xButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.leftButton.clicked.connect(self.navigate_left)
        self.ui.rightButton.clicked.connect(self.navigate_right)
        
        self.ui.uploadImageButton.clicked.connect(self.open_file_explorer)
        self.ui.uploadNewImageButton.clicked.connect(self.open_file_explorer)
        self.ui.historyTable.itemDoubleClicked.connect(self.on_row_double_clicked)  # Connect double-click signal

        # Replace the existing QLabel with ClickableLabel
        self.replace_image_placeholder()

    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.xButton, self.ui.xButton.click)  # Add ESC hotkey for xButton
        QShortcut(QKeySequence(Qt.Key_Left), self.ui.leftButton, self.ui.leftButton.click)  # Add left arrow hotkey for leftButton
        QShortcut(QKeySequence(Qt.Key_Right), self.ui.rightButton, self.ui.rightButton.click)  # Add right arrow hotkey for rightButton

    def replace_image_placeholder(self):
        """Replace the existing QLabel with ClickableLabel and set transparent background for imagePlaceholder_2."""
        old_label = self.ui.imagePlaceholder_2
        self.ui.imagePlaceholder_2 = ClickableLabel(old_label.parent())
        self.ui.imagePlaceholder_2.setGeometry(0, 0, 390, 292)  # Set the geometry to the specified values
        self.ui.imagePlaceholder_2.setObjectName(old_label.objectName())
        self.ui.imagePlaceholder_2.setStyleSheet("background-color: transparent;")  # Set transparent background
        self.ui.imagePlaceholder_2.clicked = self.open_image_preview  # Connect click event

        # Replace the existing QLabel with TransparentLabel for imageName_2
        old_image_name_label = self.ui.imageName_2
        self.ui.imageName_2 = TransparentLabel(old_image_name_label.parent())
        self.ui.imageName_2.setGeometry(169, 266, 211, 20)  # Adjust the geometry as needed (x, y, width, height)
        self.ui.imageName_2.setObjectName(old_image_name_label.objectName())
        self.ui.imageName_2.setStyleSheet("color: white; text-align: right; font: 450 italic 13pt 'SF Pro Display';")  # Set text color to white, right-align, and font style
        self.ui.imageName_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Ensure text is right-aligned

        self.ui.imageName_2.raise_()  # Bring imageName_2 QLabel to the front
        self.ui.xButton.raise_()
        self.ui.leftButton.raise_()
        self.ui.rightButton.raise_()

    @Slot()
    def open_file_explorer(self):
        """Opens a file dialog and switches pages if a file is selected."""
        file_path, _ = QFileDialog.getOpenFileName(None, "Select an Image", "", "Images (*.tiff *.png *.jpeg *.jpg)")
        if file_path:
            self.set_image_placeholder(file_path)
            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page

    def set_image_placeholder(self, image_path):
        """Set the image in the imagePlaceholder_2 QLabel and update the imageName_2 QLabel."""
        pixmap = QPixmap(image_path)
        label_size = self.ui.imagePlaceholder_2.size()
        scaled_pixmap = pixmap.scaledToHeight(292, Qt.SmoothTransformation)  # Restrict height to 292 and keep aspect ratio

        # Create a new pixmap with the label's size and fill it with a transparent background
        final_pixmap = QPixmap(label_size)
        final_pixmap.fill(Qt.transparent)

        # Draw the scaled pixmap centered within the final pixmap
        painter = QPainter(final_pixmap)
        x = (label_size.width() - scaled_pixmap.width()) // 2
        y = (label_size.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()

        self.ui.imagePlaceholder_2.setPixmap(final_pixmap)
        self.ui.imagePlaceholder_2.setScaledContents(False)  # Ensure QLabel does not scale the pixmap further
        self.ui.imagePlaceholder_2.setProperty("imagePath", image_path)  # Store the image path in the QLabel

        # Set the image name in the imageName_2 QLabel
        image_name = image_path.split("/")[-1]  # Extract the image name from the path
        self.ui.imageName_2.setText(image_name)

    @Slot()
    def on_row_double_clicked(self, item):
        """Switch to the classification page when a row is double-clicked and set the image, result, name, and date."""
        self.current_row = item.row()  # Update the current row
        self.update_record(self.current_row)

    def update_record(self, row):
        """Update the labels with the data from the specified row."""
        image_path = self.ui.historyTable.item(row, 0).data(Qt.UserRole)  # Get the file path from the custom data role
        result_text = self.ui.historyTable.item(row, 3).text()  # Get the result text from the 4th column
        name_text = self.ui.historyTable.item(row, 2).text()  # Get the name text from the 3rd column
        date_text = self.ui.historyTable.item(row, 4).text()  # Get the date text from the 5th column

        # Mapping of shortened names to full names
        disease_mapping = {
            "DR": "Diabetic Retinopathy",
            "NORMAL": "Normal",
            "MH": "Media Haze",
            "ODC": "Optic Disc Cupping",
            "TSLN": "Tessellation",
            "ARMD": "Age-Related Macular Degeneration",
            "MYA": "Myopia",
            "BRVO": "Branch Retinal Vein Occlusion",
            "ODP": "Optic Disc Pallor",
            "CRVO": "Central Retinal Vein Occlusion",
            "CNV": "Choroidal Neovascularization",
            "RS": "Retinitis",
            "ODE": "Optic Disc Edema",
            "LS": "Laser Scars",
            "CSR": "Central Serous Retinopathy",
            "HTR": "Hypertensive Retinopathy",
            "ASR": "Arteriosclerotic Retinopathy",
            "CRS": "Chorioretinitis",
            "OTHER": "Others"
        }

        # Replace shortened names with full names
        full_result_text = "\n\n".join(disease_mapping.get(disease.strip(), disease.strip()) for disease in result_text.split(","))

        # Convert date to "Month Day, Year" format
        formatted_date = datetime.strptime(date_text, "%Y-%m-%d").strftime("%B %d, %Y")

        if image_path:
            self.set_image_placeholder(image_path)
            self.ui.resultPlaceholder_2.setText(full_result_text)  # Set the result text in the resultPlaceholder_2 QLabel
            self.ui.resultPlaceholder_2.adjustSize()  # Adjust the size of the QLabel to fit the text
            self.ui.nameValue_2.setText(name_text)  # Set the name text in the nameValue_2 QLabel
            self.ui.dateValue_2.setText(formatted_date)  # Set the formatted date in the dateValue_2 QLabel
            self.ui.stackedWidget.setCurrentIndex(3)  # Move to history viewer

    @Slot()
    def navigate_left(self):
        """Navigate to the previous record."""
        if self.current_row > 0:
            self.current_row -= 1
            self.update_record(self.current_row)

    @Slot()
    def navigate_right(self):
        """Navigate to the next record."""
        if self.current_row < self.ui.historyTable.rowCount() - 1:
            self.current_row += 1
            self.update_record(self.current_row)

    @Slot()
    def open_image_preview(self, event):
        """Open a larger preview of the image when the imagePlaceholder_2 is clicked."""
        image_path = self.ui.imagePlaceholder_2.property("imagePath")
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
