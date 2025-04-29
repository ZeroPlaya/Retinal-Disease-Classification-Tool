from PySide6.QtWidgets import QFileDialog, QLabel, QDialog, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem  # Import QTableWidget and QTableWidgetItem
from PySide6.QtCore import Slot, Qt, QEvent, QDate  # Import QDate
from PySide6.QtGui import QPixmap, QPainter, QCursor, QFont, QKeySequence, QShortcut  # Import QShortcut from PySide6.QtGui
from datetime import datetime  # Import datetime for date formatting
from database import DatabaseManager  # Import only DatabaseManager
import random  # Import random for generating random diseases and percentages
import json  # Import json for writing to file
from prediction import RetinaDiseasePredictor

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
        self.predictor = RetinaDiseasePredictor(
                            model_path="non_augment_retinal_model_.pth", 
                            threshold=0.5, 
                            output_dir="predictions"
                            )      
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
        self.ui.deleteButton.clicked.connect(self.delete_selected_record)  # Connect deleteButton to delete_selected_record method
        self.ui.modifyRecordButton.clicked.connect(self.enable_editing)  # Connect modifyRecordButton to enable_editing method
        self.ui.saveChangesButton.clicked.connect(self.save_changes)  # Connect saveChangesButton to save_changes method

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
            # Get prediction results from the predictor
            result_dict = self.predictor.predict(file_path)

            # Display the image and results in the UI
            self.set_image_placeholder_classification(file_path, result_dict["class_predictions"])
            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page

    def set_image_placeholder_classification(self, image_path, result_dict):
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

        # Mapping of shortened names to full names
        disease_mapping = {
            "DR": "Diabetic Retinopathy",
            "NORMAL": "Normal",
            "MH": "Media Haze",
            "ODC": "Optic Disc Cupping",
            "TSLN": "Tessellation",
            "ARMD": "Age-Related Macular Degeneration",
            "DN": "Drusen",
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
            "CRS": "Chorioretinitis"
        }

        # Format result text with disease names and confidence scores
        full_result_text = "\n\n".join(
            f"{disease_mapping.get(disease, disease)} ({data['probability'] * 100:.2f}%)"
            for disease, data in result_dict.items() if data["prediction"] == 1
        )

        # Set the result text in the resultPlaceholder QLabel
        self.ui.resultPlaceholder.setText(full_result_text)
        self.ui.resultPlaceholder.setWordWrap(True)  # Enable word wrap
        self.ui.resultPlaceholder.setFixedWidth(191)  # Set fixed width to 191
        self.ui.resultPlaceholder.adjustSize()  # Adjust the size of the QLabel to fit the text

    @Slot()
    def on_row_double_clicked(self, item):
        """Switch to the classification page when a row is double-clicked and set the image, result, name, date, and remark."""
        self.current_row = item.row()  # Update the current row
        self.update_record(self.current_row)

    def update_record(self, row):
        """Update the labels with the data from the specified row."""
        image_path = self.ui.historyTable.item(row, 0).data(Qt.UserRole)  # Get the file path from the custom data role
        record = list(self.db_manager.collection.find())[row]  # Fetch the record from the database
        result_dict = record.get("diagnosis", {})  # Get the result dictionary
        print(result_dict)  # Print the result dictionary for debugging
        name_text = record.get("patient_name", "")  # Get the name text
        date_text = record.get("date", "")  # Get the date text
        remark_text = record.get("notes", "")  # Get the remark text

        # Mapping of shortened names to full names
        disease_mapping = {
            "DR": "Diabetic Retinopathy",
            "NORMAL": "Normal",
            "MH": "Media Haze",
            "ODC": "Optic Disc Cupping",
            "TSLN": "Tessellation",
            "ARMD": "Age-Related Macular Degeneration",
            "DN": "Drusen",
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
            "CRS": "Chorioretinitis"
        }

        # Format result text with disease names and confidence scores
        # The structure of result_dict from the database is different from prediction results
        full_result_text = ""
        for disease, probability in result_dict.items():
            if isinstance(probability, (int, float)):
                # For records saved in the new format where probability is directly a number
                full_result_text += f"{disease} ({probability * 100:.2f}%)\n\n"
            elif isinstance(probability, dict) and probability.get("prediction") == 1:
                # For records saved in the old format where probability is a dict with prediction and probability keys
                full_result_text += f"{disease} ({probability.get('probability', 0) * 100:.2f}%)\n\n"

        # Remove trailing newlines
        full_result_text = full_result_text.rstrip()

        # Convert date to "Month Day, Year" format
        formatted_date = datetime.strptime(date_text, "%Y-%m-%d").strftime("%B %d, %Y")

        if image_path:
            self.set_image_placeholder_history(image_path)
            self.ui.resultPlaceholder_2.setText(full_result_text)  # Set the result text in the resultPlaceholder_2 QLabel
            self.ui.resultPlaceholder_2.setWordWrap(True)  # Enable word wrap
            self.ui.resultPlaceholder_2.setFixedWidth(191)  # Set fixed width to 191
            self.ui.resultPlaceholder_2.adjustSize()  # Adjust the size of the QLabel to fit the text
            self.ui.resultPlaceholder_2.setVisible(True)  # Ensure the QLabel is visible
            self.ui.nameValue_2.setText(name_text)  # Set the name text in the nameValue_2 QLabel
            self.ui.dateValue_2.setText(formatted_date)  # Set the formatted date in the dateValue_2 QLabel
            self.ui.remarkValue_2.setText(remark_text)  # Set the remark text in the remarkValue_2 QLabel
            self.ui.stackedWidget.setCurrentIndex(3)  # Move to history viewer

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

        # Mapping of shortened names to full names
        disease_mapping = {
            "DR": "Diabetic Retinopathy",
            "NORMAL": "Normal",
            "MH": "Media Haze",
            "ODC": "Optic Disc Cupping",
            "TSLN": "Tessellation",
            "ARMD": "Age-Related Macular Degeneration",
            "DN": "Drusen",
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
            "CRS": "Chorioretinitis"
        }

        # Convert results text to dictionary with full disease names
        result_dict = {}
        for line in results.split("\n\n"):
            if line:
                disease, confidence = line.rsplit(" (", 1)
                confidence = float(confidence.rstrip("%)"))
                full_disease_name = disease_mapping.get(disease, disease)  # Map to full name
                result_dict[full_disease_name] = confidence / 100

        # Prepare the record to save
        record = {
            "image_path": image_path,
            "file_name": image_path.split("/")[-1] if image_path else "",
            "patient_name": name,
            "diagnosis": result_dict,
            "date": datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d"),
            "notes": remark
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

    def refresh_history_table(self):
        """Refresh the history table to show the updated records."""
        if self.db_manager.collection is not None:  # Explicitly check if collection is not None
            records = list(self.db_manager.collection.find())  # Fetch records from MongoDB
        else:
            records = []

        self.ui.historyTable.setRowCount(len(records))

        for row_idx, record in enumerate(records):
            # Load and resize image for each row
            image_path = record.get("image_path", "")
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Insert image in first column
            image_item = QTableWidgetItem()
            image_item.setData(Qt.DecorationRole, scaled_pixmap)  # Set image as decoration
            image_item.setData(Qt.UserRole, image_path)  # Store the file path in a custom data role
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
            # Get prediction results from the predictor
            result_dict = self.predictor.predict(file_path)
            
            # Display the image and results in the UI
            self.set_image_placeholder_classification(file_path, result_dict["class_predictions"])
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

    def delete_selected_record(self):
        """Delete the selected record from the history table and database."""
        selected_row = self.ui.historyTable.currentRow()
        if selected_row >= 0:
            if self.db_manager.collection is not None:
                # Fetch the record to delete
                record_id = self.ui.historyTable.item(selected_row, 0).data(Qt.UserRole)
                try:
                    self.db_manager.collection.delete_one({"image_path": record_id})
                    msg_box = QMessageBox(self.ui)
                    msg_box.setWindowTitle("Success")
                    msg_box.setText("Record deleted successfully!")
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
                    QMessageBox.critical(self.ui, "Error", f"Failed to delete record: {e}")
            else:
                QMessageBox.warning(self.ui, "Warning", "Database connection is not established.")

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
                        {"image_path": record_id},
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
