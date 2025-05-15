from PySide6.QtWidgets import QFileDialog, QLabel, QDialog, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem  # Import QTableWidget and QTableWidgetItem
from PySide6.QtCore import Slot, Qt, QEvent, QDate  # Import QDate
from PySide6.QtGui import QPixmap, QPainter, QCursor, QFont, QKeySequence, QShortcut  # Import QShortcut from PySide6.QtGui
from datetime import datetime  # Import datetime for date formatting
from database import DatabaseManager  # Import only DatabaseManager
import random  # Import random for generating random diseases and percentages
import json  # Import json for writing to file
import os  # Import os for file operations
import sys  # Import sys for platform detection
import subprocess  # Import subprocess for opening files
import re
from fpdf import FPDF  # Import FPDF for PDF generation

def strip_html_tags(text):
    """Remove HTML tags from a string."""
    return re.sub(r'<[^>]*>', '', text)

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
        self.db_manager = DatabaseManager()  # Initialize DatabaseManager with default connection string
        self.connect_buttons()
        self.setup_shortcuts()  # Setup shortcuts
        self.setup_editable_fields()  # Setup editable fields

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
        
        self.ui.uploadImageButton.clicked.connect(self.open_file_explorer_classification)
        self.ui.uploadNewImageButton.clicked.connect(self.upload_new_image)
        self.ui.historyTable.itemDoubleClicked.connect(self.on_row_double_clicked)  # Connect double-click signal
        self.ui.saveResultsButton.clicked.connect(self.save_results)  # Connect saveResultsButton to save_results method
        self.ui.archiveButton.clicked.connect(self.archive_selected_record)  # Connect archiveButton to archive_selected_record method
        self.ui.modifyRecordButton.clicked.connect(self.enable_editing)  # Connect modifyRecordButton to enable_editing method
        self.ui.saveChangesButton.clicked.connect(self.save_changes)  # Connect saveChangesButton to save_changes method
        self.ui.printButton.clicked.connect(self.print_selected_record)  # Connect printButton to print_selected_record method

        # Replace the existing QLabel with ClickableLabel
        self.replace_image_placeholder()
        self.replace_image_placeholder_classification()

        # Reset placeholders when exiting
        self.ui.uploadBackButton.clicked.connect(self.reset_placeholders)
        self.ui.classificationBackButton.clicked.connect(self.reset_placeholders)


    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.uploadBackButton, self.ui.uploadBackButton.click)  # Add ESC hotkey for uploadBackButton
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.historyBackButton, self.ui.historyBackButton.click)  # Add ESC hotkey for historyBackButton
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.classificationBackButton, self.ui.classificationBackButton.click)  # Add ESC hotkey for classificationBackButton
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.xButton, self.ui.xButton.click)  # Add ESC hotkey for xButton
        QShortcut(QKeySequence(Qt.Key_Left), self.ui.leftButton, self.ui.leftButton.click)  # Add left arrow hotkey for leftButton
        QShortcut(QKeySequence(Qt.Key_Right), self.ui.rightButton, self.ui.rightButton.click)  # Add right arrow hotkey for rightButton

    def setup_editable_fields(self):
        """Setup editable fields for nameValue, dateValue, and remarkValue."""
        # Define the stylesheet for QLineEdit and QLabel
        common_stylesheet = """
        QLineEdit, QLabel {
            background-color: transparent; /* Transparent background */
            color: black; /* Ensure text stays visible */
        }
        QLineEdit {
            border: 1px solid #dcdcdc; /* Add a border for the input field */
            padding: 4px; /* Add padding for better alignment */
        }
        QLabel {
            font-weight: bold; /* Make the label text bold */
        }
        """

        # Replace nameValue QLabel with QLineEdit
        old_name_label = self.ui.nameValue
        self.ui.nameValue = QLineEdit(old_name_label.parent())
        self.ui.nameValue.setGeometry(old_name_label.geometry())
        self.ui.nameValue.setObjectName(old_name_label.objectName())
        self.ui.nameValue.setStyleSheet(common_stylesheet)
        self.ui.nameValue.setAlignment(old_name_label.alignment())
        self.ui.nameValue.setFont(old_name_label.font())
        self.ui.nameValue.setPlaceholderText("Insert Name")  # Set placeholder text
        self.ui.nameValue.setFrame(False)  # Remove the frame to make it look like a QLabel
        self.ui.nameValue.textChanged.connect(self.update_placeholder_visibility)  # Connect textChanged signal

        # Set dateValue to the current date
        current_date = datetime.now().strftime("%B %d, %Y")
        self.ui.dateValue.setText(current_date)

        # Replace remarkValue QLabel with QLineEdit
        old_remark_label = self.ui.remarkValue
        self.ui.remarkValue = QLineEdit(old_remark_label.parent())
        self.ui.remarkValue.setGeometry(old_remark_label.geometry())
        self.ui.remarkValue.setObjectName(old_remark_label.objectName())
        self.ui.remarkValue.setStyleSheet(common_stylesheet)
        self.ui.remarkValue.setAlignment(old_remark_label.alignment())
        self.ui.remarkValue.setFont(old_remark_label.font())
        self.ui.remarkValue.setPlaceholderText("Insert Remarks")  # Set placeholder text
        self.ui.remarkValue.setFrame(False)  # Remove the frame to make it look like a QLabel
        self.ui.remarkValue.textChanged.connect(self.update_placeholder_visibility)  # Connect textChanged signal

        # Adjust the label's background to match the input field
        remark_label = self.ui.remarkLabel  # Assuming the label is named `remarkLabel`
        remark_label.setStyleSheet(common_stylesheet)
        remark_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Align text to the left and vertically centered

        # Replace nameValue_2 QLabel with QLineEdit
        old_name_label_2 = self.ui.nameValue_2
        self.ui.nameValue_2 = QLineEdit(old_name_label_2.parent())
        self.ui.nameValue_2.setGeometry(old_name_label_2.geometry())
        self.ui.nameValue_2.setObjectName(old_name_label_2.objectName())
        self.ui.nameValue_2.setStyleSheet(common_stylesheet)
        self.ui.nameValue_2.setAlignment(old_name_label_2.alignment())
        self.ui.nameValue_2.setFont(old_name_label_2.font())
        self.ui.nameValue_2.setPlaceholderText("Insert Name")  # Set placeholder text
        self.ui.nameValue_2.setFrame(False)  # Remove the frame to make it look like a QLabel
        self.ui.nameValue_2.setReadOnly(True)  # Initially set to read-only

        # Replace remarkValue_2 QLabel with QLineEdit
        old_remark_label_2 = self.ui.remarkValue_2
        self.ui.remarkValue_2 = QLineEdit(old_remark_label_2.parent())
        self.ui.remarkValue_2.setGeometry(old_remark_label_2.geometry())
        self.ui.remarkValue_2.setObjectName(old_remark_label_2.objectName())
        self.ui.remarkValue_2.setStyleSheet(common_stylesheet)
        self.ui.remarkValue_2.setAlignment(old_remark_label_2.alignment())
        self.ui.remarkValue_2.setFont(old_remark_label_2.font())
        self.ui.remarkValue_2.setPlaceholderText("Insert Remarks")  # Set placeholder text
        self.ui.remarkValue_2.setFrame(False)  # Remove the frame to make it look like a QLabel
        self.ui.remarkValue_2.setReadOnly(True)  # Initially set to read-only

    def update_placeholder_visibility(self):
        """Update the visibility of the placeholder text based on the content."""
        if not self.ui.nameValue.text():
            self.ui.nameValue.setPlaceholderText("Insert Name")  # Set placeholder text if empty
        if not self.ui.remarkValue.text():
            self.ui.remarkValue.setPlaceholderText("Insert Remarks")  # Set placeholder text if empty

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

        self.ui.xButton.raise_()
        self.ui.leftButton.raise_()
        self.ui.rightButton.raise_()
        self.ui.imageName_2.raise_()  # Bring imageName_2 QLabel to the front

        # Ensure the imagePlaceholder_2 is visible
        self.ui.imagePlaceholder_2.setVisible(True)

    def replace_image_placeholder_classification(self):
        """Replace the existing QLabel with ClickableLabel and set transparent background for imagePlaceholder."""
        old_label = self.ui.imagePlaceholder
        self.ui.imagePlaceholder = ClickableLabel(old_label.parent())
        self.ui.imagePlaceholder.setGeometry(0, 0, 390, 292)  # Set the geometry to the specified values
        self.ui.imagePlaceholder.setObjectName(old_label.objectName())
        self.ui.imagePlaceholder.setStyleSheet("background-color: transparent;")  # Set transparent background
        self.ui.imagePlaceholder.clicked = self.open_image_preview_classification  # Connect click event

        # Replace the existing QLabel with TransparentLabel for imageName
        old_image_name_label = self.ui.imageName
        self.ui.imageName = TransparentLabel(old_image_name_label.parent())
        self.ui.imageName.setGeometry(169, 266, 211, 20)  # Adjust the geometry as needed (x, y, width, height)
        self.ui.imageName.setObjectName(old_image_name_label.objectName())
        self.ui.imageName.setStyleSheet("color: white; text-align: right; font: 450 italic 13pt 'SF Pro Display';")  # Set text color to white, right-align, and font style
        self.ui.imageName.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Ensure text is right-aligned

        self.ui.imageName.raise_()  # Bring imageName QLabel to the front

        # Ensure the imagePlaceholder is visible
        self.ui.imagePlaceholder.setVisible(True)

    @Slot()
    def open_file_explorer_classification(self):
        """Opens a file dialog and switches to the classification page if a file is selected."""
        file_path, _ = QFileDialog.getOpenFileName(None, "Select an Image", "", "Images (*.tiff *.png *.jpeg *.jpg)")
        if file_path:
            self.set_image_placeholder_classification(file_path)
            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page

    def set_image_placeholder_classification(self, image_path):
        """Set the image in the imagePlaceholder QLabel for the classification page."""
        pixmap = QPixmap(image_path)
        label_size = self.ui.imagePlaceholder.size()
        scaled_pixmap = pixmap.scaledToHeight(292, Qt.SmoothTransformation)  # Restrict height to 292 and keep aspect ratio

        # Create a new pixmap with the label's size and fill it with a transparent background
        final_pixmap = QPixmap(label_size)
        final_pixmap.fill(Qt.transparent)

        # Draw the scaled pixmap centered within the final_pixmap
        painter = QPainter(final_pixmap)
        x = (label_size.width() - scaled_pixmap.width()) // 2
        y = (label_size.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()

        self.ui.imagePlaceholder.setPixmap(final_pixmap)
        self.ui.imagePlaceholder.setScaledContents(False)  # Ensure QLabel does not scale the pixmap further
        self.ui.imagePlaceholder.setProperty("imagePath", image_path)  # Store the image path in the QLabel

        # Set the image name in the imageName QLabel
        image_name = image_path.split("/")[-1]  # Extract the image name from the path
        self.ui.imageName.setText(image_name)

        # Ensure placeholder text is set correctly
        self.ui.nameValue.setPlaceholderText("Insert Name")
        self.ui.remarkValue.setPlaceholderText("Insert Remarks")

        # Generate random diseases with random percentages
        diseases = ["DR", "NORMAL", "MH", "ODC", "TSLN", "ARMD", "MYA", "BRVO", "ODP", "CRVO", "CNV", "RS", "ODE", "LS", "CSR", "HTR", "ASR", "CRS", "OTHER"]
        num_diseases = random.choices([1, 2, 3], weights=[50, 30, 20], k=1)[0]  # More likely to output fewer diseases
        selected_diseases = random.sample(diseases, num_diseases)  # Select random diseases
        result_dict = {disease: round(random.uniform(0.5, 1.0), 2) for disease in selected_diseases}  # Assign random percentages

        # Mapping of shortened names to full names
        disease_mapping = {
            "DR": ("Diabetic Retinopathy", "A complication of diabetes that damages the retina's blood vessels."),
            "NORMAL": ("Normal", "No detectable abnormalities in the retinal image."),
            "MH": ("Media Haze", "Clouding or opacity in the eye's media, often affecting image clarity."),
            "ODC": ("Optic Disc Cupping", "Enlargement of the optic disc cup, often associated with glaucoma."),
            "TSLN": ("Tessellation", "A retinal appearance with prominent choroidal vessels, often linked to myopia."),
            "ARMD": ("Age-Related Macular Degeneration", "Degeneration of the macula causing vision loss in older adults."),
            "MYA": ("Myopia", "Nearsightedness; distant objects appear blurry."),
            "BRVO": ("Branch Retinal Vein Occlusion", "Blockage of a small vein in the retina, causing vision issues."),
            "ODP": ("Optic Disc Pallor", "Pale appearance of the optic disc, indicating optic nerve damage."),
            "CRVO": ("Central Retinal Vein Occlusion", "Blockage of the main retinal vein, leading to vision loss."),
            "CNV": ("Choroidal Neovascularization", "Growth of abnormal blood vessels under the retina, causing leakage and vision loss."),
            "RS": ("Retinitis", "Inflammation of the retina, possibly from infection or autoimmune causes."),
            "ODE": ("Optic Disc Edema", "Swelling of the optic disc due to increased intracranial pressure or inflammation."),
            "LS": ("Laser Scars", "Scarring from previous laser treatments in the retina."),
            "CSR": ("Central Serous Retinopathy", "Fluid buildup under the retina that distorts vision."),
            "HTR": ("Hypertensive Retinopathy", "Retinal damage caused by high blood pressure."),
            "ASR": ("Arteriosclerotic Retinopathy", "Changes in the retinal arteries due to arteriosclerosis."),
            "CRS": ("Chorioretinitis", "Inflammation of both the choroid and retina, often due to infection."),
            "OTHER": ("Others", "Other retinal or ocular abnormalities not classified above.")
}


        # Format result text with disease names and confidence scores
        full_result_text = "<br><br>".join(
            f"<span style='font-size:11pt; font-weight:bold'>{disease_mapping[disease][0]} ({confidence:.2f}%)</span><br>"
            f"<span style='font-size:9pt;'>{disease_mapping[disease][1]}</span>"
            for disease, confidence in result_dict.items()
            if disease in disease_mapping
)



        # Set the result text in the resultPlaceholder QLabel
        self.ui.resultPlaceholder.setTextFormat(Qt.RichText)
        self.ui.resultPlaceholder.setText(full_result_text)
        self.ui.resultPlaceholder.setWordWrap(True)  # Enable word wrap
        self.ui.resultPlaceholder.setFixedWidth(191)  # Set fixed width to 191
        self.ui.resultPlaceholder.adjustSize()  # Adjust the size of the QLabel to fit the text
    


    @Slot()
    def on_row_double_clicked(self, item):
        """Switch to the classification page when a row is double-clicked and set the image, result, name, date, and remark."""
        record_id = self.ui.historyTable.item(item.row(), 0).data(Qt.UserRole)  # Get the _id from the custom data role
        self.update_record(record_id)

    def update_record(self, record_id):
        """Update the labels with the data from the specified record."""
        record = self.db_manager.collection.find_one({"_id": record_id})  # Fetch the record using _id
        if not record:
            QMessageBox.warning(self.ui, "Warning", "Record not found.")
            return

        image_path = record.get("image_path", "")
        result_dict = record.get("diagnosis", {})
        name_text = record.get("patient_name", "")
        date_text = record.get("date", "")
        remark_text = record.get("notes", "")

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

        # Format result text with disease names and confidence scores
        full_result_text = "\n\n".join(
            f"{disease_mapping[disease][0]} ({confidence:.2f}%)\n{disease_mapping[disease][1]}"
            if disease in disease_mapping else
            f"{disease} ({confidence:.2f}%)"
            for disease, confidence in result_dict.items()
        )

        # Convert date to "Month Day, Year" format
        formatted_date = datetime.strptime(date_text, "%Y-%m-%d").strftime("%B %d, %Y")

        if image_path:
            self.set_image_placeholder_history(image_path)
            self.ui.resultPlaceholder_2.setText(full_result_text)
            self.ui.resultPlaceholder_2.setWordWrap(True)
            self.ui.resultPlaceholder_2.setFixedWidth(191)
            self.ui.resultPlaceholder_2.adjustSize()
            self.ui.nameValue_2.setText(name_text)
            self.ui.dateValue_2.setText(formatted_date)
            self.ui.remarkValue_2.setText(remark_text)
            self.ui.stackedWidget.setCurrentIndex(3)

        # Update button visibility
        self.ui.leftButton.setVisible(self.current_row > 0)
        self.ui.rightButton.setVisible(self.current_row < self.ui.historyTable.rowCount() - 1)

    def set_image_placeholder_history(self, image_path):
        """Set the image in the imagePlaceholder_2 QLabel for the history viewer page."""
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

        # Set the image name in the imageName QLabel
        image_name = image_path.split("/")[-1]  # Extract the image name from the path
        self.ui.imageName_2.setText(image_name)

    @Slot()
    def navigate_left(self):
        """Navigate to the previous record."""
        if self.current_row > 0:
            self.current_row -= 1
            record_id = self.ui.historyTable.item(self.current_row, 0).data(Qt.UserRole)  # Get the _id from the table
            self.update_record(record_id)

    @Slot()
    def navigate_right(self):
        """Navigate to the next record."""
        if self.current_row < self.ui.historyTable.rowCount() - 1:
            self.current_row += 1
            record_id = self.ui.historyTable.item(self.current_row, 0).data(Qt.UserRole)  # Get the _id from the table
            self.update_record(record_id)

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

    @Slot()
    def open_image_preview_classification(self, event):
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

    def save_results(self):
        """Save the current data to the database."""
        name = self.ui.nameValue.text()
        date = self.ui.dateValue.text()
        remark = self.ui.remarkValue.text()
        results = self.ui.resultPlaceholder.text()
        image_path = self.ui.imagePlaceholder.property("imagePath")

        if not name:
            msg_box = QMessageBox(self.ui)
            msg_box.setWindowTitle("Warning")
            msg_box.setText("Name cannot be empty!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: white; /* Plain white background */
                    color: black; /* Ensure text is black */
                }
                QLabel {
                    color: black; /* Ensure text is black */
                }
                QPushButton {
                    background-color: white; /* Plain button background */
                    border: 1px solid #dcdcdc;
                    color: black; /* Ensure button text is black */
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0; /* Slight hover effect */
                }
                """
            )
            msg_box.exec()
            return

        # Convert results text to dictionary
        result_dict = {}
        for block in results.strip().split("\n\n"):
            lines = block.strip().split("\n")
            if not lines:
                continue

            header = lines[0]  # e.g., "Diabetic Retinopathy (92.00%)"
            match = re.match(r"(.+?)\s+\(([\d.]+)%\)", header)
            if match:
                disease_name = match.group(1)
                confidence = float(match.group(2)) / 100
                result_dict[disease_name] = confidence


        # Prepare the record to save
        record = {
            "image_path": image_path,
            "file_name": image_path.split("/")[-1] if image_path else "",
            "patient_name": name,
            "diagnosis": result_dict,
            "date": datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d"),
            "notes": remark,
            "archived": False  # Ensure the new record is not archived
        }

        # Save the record to the database
        self.db_manager.save_record(record)

        msg_box = QMessageBox(self.ui)
        msg_box.setWindowTitle("Success")
        msg_box.setText("Record Saved!")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: white; /* Plain white background */
                color: black; /* Ensure text is black */
            }
            QLabel {
                color: black; /* Ensure text is black */
            }
            QPushButton {
                background-color: white; /* Plain button background */
                border: 1px solid #dcdcdc;
                color: black; /* Ensure button text is black */
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0; /* Slight hover effect */
            }
            """
        )
        msg_box.exec()

        self.refresh_history_table()

    def refresh_history_table(self, show_archived=False):
        """Refresh the history table to show the updated records, excluding archived ones by default."""
        records = self.db_manager.fetch_records(show_archived=show_archived)  # Use fetch_records method

        self.ui.historyTable.setRowCount(len(records))

        for row_idx, record in enumerate(records):
            # Load and resize image for each row
            image_path = record.get("image_path", "")
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Insert image in first column
            image_item = QTableWidgetItem()
            image_item.setData(Qt.DecorationRole, scaled_pixmap)  # Set image as decoration
            image_item.setData(Qt.UserRole, record.get("_id"))  # Store the unique _id in the custom data role
            self.ui.historyTable.setItem(row_idx, 0, image_item)

            # Insert other data into columns
            file_name = record.get("file_name", "")
            patient_name = record.get("patient_name", "")
            diagnosis = ", ".join(record.get("diagnosis", {}).keys())  # Join disease names without confidence scores
            date = record.get("date", "")
            notes = record.get("notes", "")

            row_data = [file_name, patient_name, diagnosis, date, notes]
            for col_idx, text in enumerate(row_data, start=1):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.historyTable.setItem(row_idx, col_idx, item)

    @Slot()
    def upload_new_image(self):
        """Handle uploading a new image and reset placeholders if successful."""
        file_path, _ = QFileDialog.getOpenFileName(None, "Select an Image", "", "Images (*.tiff *.png *.jpeg *.jpg)")
        if file_path:
            self.reset_placeholders()
            self.set_image_placeholder_classification(file_path)
            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page

    def reset_placeholders(self):
        """Reset the placeholders when exiting the upload or classification page."""
        self.ui.nameValue.clear()
        self.ui.remarkValue.clear()
        self.ui.resultPlaceholder.clear()
        self.ui.imagePlaceholder.clear()
        self.ui.imageName.clear()
        current_date = datetime.now().strftime("%B %d, %Y")
        self.ui.dateValue.setText(current_date)

    def archive_selected_record(self):
        """Mark the selected record as archived in the database and hide it from the table."""
        selected_row = self.ui.historyTable.currentRow()
        if selected_row >= 0:
            record_id = self.ui.historyTable.item(selected_row, 0).data(Qt.UserRole)  # Get the _id from the table
            if record_id:
                try:
                    # Update the 'archived' field to True in the database
                    result = self.db_manager.collection.update_one(
                        {"_id": record_id},
                        {"$set": {"archived": True}}
                    )
                    if result.modified_count > 0:
                        msg_box = QMessageBox(self.ui)
                        msg_box.setWindowTitle("Success")
                        msg_box.setText("Record archived successfully!")
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setStyleSheet(
                            """
                            QMessageBox {
                                background-color: white; /* Plain white background */
                                color: black; /* Ensure text is black */
                            }
                            QLabel {
                                color: black; /* Ensure text is black */
                            }
                            QPushButton {
                                background-color: white; /* Plain button background */
                                border: 1px solid #dcdcdc;
                                color: black; /* Ensure button text is black */
                                padding: 5px;
                            }
                            QPushButton:hover {
                                background-color: #f0f0f0; /* Slight hover effect */
                            }
                            """
                        )
                        msg_box.exec()
                    else:
                        QMessageBox.warning(self.ui, "Warning", "Failed to archive the record. It may not exist.")
                except Exception as e:
                    QMessageBox.critical(self.ui, "Error", f"Failed to archive record: {e}")
            else:
                QMessageBox.warning(self.ui, "Warning", "Unable to find the record's unique identifier.")

            # Refresh the history table
            self.refresh_history_table()

    def enable_editing(self):
        """Enable editing of nameValue_2 and remarkValue_2 in the history viewer."""
        self.ui.nameValue_2.setReadOnly(False)
        self.ui.remarkValue_2.setReadOnly(False)

    def save_changes(self):
        """Save changes to the selected record in the history viewer."""
        name = self.ui.nameValue_2.text()
        remark = self.ui.remarkValue_2.text()

        if not name:
            msg_box = QMessageBox(self.ui)
            msg_box.setWindowTitle("Warning")
            msg_box.setText("Name cannot be empty!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: white; /* Plain white background */
                    color: black; /* Ensure text is black */
                }
                QLabel {
                    color: black; /* Ensure text is black */
                }
                QPushButton {
                    background-color: white; /* Plain button background */
                    border: 1px solid #dcdcdc;
                    color: black; /* Ensure button text is black */
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0; /* Slight hover effect */
                }
                """
            )
            msg_box.exec()
            return

        selected_row = self.current_row
        if selected_row >= 0:
            record_id = self.ui.historyTable.item(selected_row, 0).data(Qt.UserRole)
            if self.db_manager.collection is not None:
                try:
                    self.db_manager.collection.update_one(
                        {"_id": record_id},
                        {"$set": {"patient_name": name, "notes": remark}}
                    )
                    msg_box = QMessageBox(self.ui)
                    msg_box.setWindowTitle("Success")
                    msg_box.setText("Changes saved successfully!")
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setStyleSheet(
                        """
                        QMessageBox {
                            background-color: white; /* Plain white background */
                            color: black; /* Ensure text is black */
                        }
                        QLabel {
                            color: black; /* Ensure text is black */
                        }
                        QPushButton {
                            background-color: white; /* Plain button background */
                            border: 1px solid #dcdcdc;
                            color: black; /* Ensure button text is black */
                            padding: 5px;
                        }
                        QPushButton:hover {
                            background-color: #f0f0f0; /* Slight hover effect */
                        }
                        """
                    )
                    msg_box.exec()
                except Exception as e:
                    QMessageBox.critical(self.ui, "Error", f"Failed to save changes: {e}")
            else:
                QMessageBox.warning(self.ui, "Warning", "Database connection is not established.")

            # Refresh the history table
            self.refresh_history_table()

        # Disable editing
        self.ui.nameValue_2.setReadOnly(True)
        self.ui.remarkValue_2.setReadOnly(True)

    def print_selected_record(self):
        """Generate a professional-looking PDF of the selected record with its details and image."""
        selected_row = self.ui.historyTable.currentRow()
        if selected_row >= 0:
            record_id = self.ui.historyTable.item(selected_row, 0).data(Qt.UserRole)
            record = self.db_manager.collection.find_one({"_id": record_id}) if self.db_manager.collection is not None else None

            if record:
                class PDF(FPDF):
                    def header(self):
                        self.set_font("Arial", "B", 16)
                        self.cell(0, 10, "Fundus Analysis Report ", border=False, ln=True, align="C")
                        self.ln(2)
                        self.set_draw_color(0, 0, 0)
                        self.set_line_width(0.5)
                        self.line(10, self.get_y(), 200, self.get_y())
                        self.ln(5)

                    def footer(self):
                        self.set_y(-15)
                        self.set_font("Arial", "I", 8)
                        self.cell(0, 10, f"Page {self.page_no()}", align="C")

                # Disease Description Dictionary
                disease_description = {
                    "DR": ("Diabetic Retinopathy", "A complication of diabetes that damages the retina's blood vessels.", "Disease"),
                    "NORMAL": ("Normal", "No detectable abnormalities in the retinal image.", "Condition"),
                    "MH": ("Media Haze", "Clouding or opacity in the eye's media, often affecting image clarity.", "Condition"),
                    "ODC": ("Optic Disc Cupping", "Enlargement of the optic disc cup, often associated with glaucoma.", "Condition"),
                    "TSLN": ("Tessellation", "A retinal appearance with prominent choroidal vessels, often linked to myopia.", "Condition"),
                    "ARMD": ("Age-Related Macular Degeneration", "Degeneration of the macula causing vision loss in older adults.", "Disease"),
                    "MYA": ("Myopia", "Nearsightedness; distant objects appear blurry.", "Condition"),
                    "BRVO": ("Branch Retinal Vein Occlusion", "Blockage of a small vein in the retina, causing vision issues.", "Disease"),
                    "ODP": ("Optic Disc Pallor", "Pale appearance of the optic disc, indicating optic nerve damage.", "Condition"),
                    "CRVO": ("Central Retinal Vein Occlusion", "Blockage of the main retinal vein, leading to vision loss.", "Disease"),
                    "CNV": ("Choroidal Neovascularization", "Growth of abnormal blood vessels under the retina, causing leakage and vision loss.", "Disease"),
                    "RS": ("Retinitis", "Inflammation of the retina, possibly from infection or autoimmune causes.", "Disease"),
                    "ODE": ("Optic Disc Edema", "Swelling of the optic disc due to increased intracranial pressure or inflammation.", "Condition"),
                    "LS": ("Laser Scars", "Scarring from previous laser treatments in the retina.", "Condition"),
                    "CSR": ("Central Serous Retinopathy", "Fluid buildup under the retina that distorts vision.", "Condition"),
                    "HTR": ("Hypertensive Retinopathy", "Retinal damage caused by high blood pressure.", "Disease"),
                    "ASR": ("Arteriosclerotic Retinopathy", "Changes in the retinal arteries due to arteriosclerosis.", "Disease"),
                    "CRS": ("Chorioretinitis", "Inflammation of both the choroid and retina, often due to infection.", "Disease"),
                    "OTHER": ("Others", "Other retinal or ocular abnormalities not classified above.")
                }

                pdf = PDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Patient Name and Record Date
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Name: {record.get('patient_name', 'N/A')}", ln=False, align="L")
                pdf.cell(0, 10, f"Record Date: {record.get('date', 'N/A')}", ln=True, align="R")

                # Timestamp of Printing
                pdf.set_font("Arial", size=10)
                pdf.cell(0, 10, f"Printed On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="R")
                pdf.ln(5)

                # Diagnosis
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "Diagnosis:", ln=True, align="L")
                pdf.set_font("Arial", size=12)
                diagnosed_conditions = []
                
                for disease, confidence in record.get("diagnosis", {}).items():
                    clean_disease = strip_html_tags(disease)
                    pdf.cell(0, 10, f"- {clean_disease}: {confidence * 100:.2f}%", ln=True, align="L")
                    diagnosed_conditions.append(clean_disease)
                    
                pdf.ln(5)

                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "Disease Descriptions:", ln=True, align="L")
                pdf.set_font("Arial", size=12)
                
                for condition in diagnosed_conditions:
                    for desc_code, (name, description, category) in disease_description.items():
                        if name.lower() in condition.lower():
                            pdf.set_font("Arial", "B", 11)
                            pdf.cell(0, 10, f"- {name} ({category}):", ln=True)
                            pdf.set_font("Arial", size=11)
                            pdf.multi_cell(0, 10, f"  {description}")
                            pdf.ln(1)
                            break


            # Disease Descriptions Section
                #pdf.set_font("Arial", "B", 10)
                #pdf.cell(0, 10, "Disease Descriptions:", ln=True, align="L")
                #pdf.set_font("Arial", size=12)
                #for code, (name, description) in disease_description.items():
                    #pdf.set_font("Arial", "B", 11)
                    #pdf.cell(0, 10, f"- {name}:", ln=True)
                    #pdf.set_font("Arial", size=11)
                    #pdf.multi_cell(0, 10, f"  {description}")
                    #pdf.ln(1)

                # Remarks
                remarks = record.get("notes", "").strip()
                if remarks:
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, "Remarks:", ln=True, align="L")
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, remarks)
                    pdf.ln(5)

                # Uploaded Image
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "Uploaded Image", ln=True, align="C")
                image_path = record.get("image_path", "")
                if os.path.exists(image_path):
                    current_y = pdf.get_y()
                    image_width = 80
                    x_center = (210 - image_width) // 2
                    pdf.image(image_path, x=x_center, y=current_y, w=image_width)
                    pdf.set_y(current_y + 80)  # Move cursor below image
                    pdf.ln(10)

                # Doctor Name
                pdf.set_y(-70)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "Doctor's Name:", ln=True)
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 10, "______________________________", ln=True)
                pdf.cell(0,10, "Ophthalmologist", ln=True) 
                


                # Save PDF
                filename = f"{record.get('patient_name', 'record').replace(' ', '_')}.pdf"
                output_path = os.path.join(os.getcwd(), filename)
                pdf.output(output_path)

                # Open PDF
                try:
                    if sys.platform == "win32":
                        os.startfile(output_path)
                    elif sys.platform == "darwin":
                        subprocess.run(["open", output_path])
                    else:
                        subprocess.run(["xdg-open", output_path])
                except Exception as e:
                    QMessageBox.warning(self.ui, "Warning", f"Failed to open PDF: {e}")

                # Show Success Message
                msg_box = QMessageBox(self.ui)
                msg_box.setWindowTitle("Success")
                msg_box.setText(f"PDF saved successfully at {output_path}")
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStyleSheet(
                    """
                    QMessageBox {
                        background-color: white;
                        color: black;
                    }
                    QLabel {
                        color: black;
                    }
                    QPushButton {
                        background-color: white;
                        border: 1px solid #dcdcdc;
                        color: black;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                    """
                )
                msg_box.exec()