from PySide6.QtWidgets import QFileDialog, QLabel, QDialog, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox  # Import QTableWidget, QTableWidgetItem, and QComboBox
from PySide6.QtCore import Slot, Qt, QEvent, QDate  # Import QDate
from PySide6.QtGui import QPixmap, QPainter, QCursor, QFont, QKeySequence, QShortcut  # Import QShortcut from PySide6.QtGui
from datetime import datetime  # Import datetime for date formatting
from database import DatabaseManager  # Import only DatabaseManager
import random  # Import random for generating random diseases and percentages
import json  # Import json for writing to file
from prediction import RetinaDiseasePredictor
from fpdf import FPDF
import sys
import os
from bson import ObjectId  # Import ObjectId for MongoDB queries


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
        self.image_paths = []  # Store paths of up to two images
        self.current_image_index = 0  # Track the currently displayed image
        self.shared_name = ""  # Shared name for both images
        self.shared_date = ""  # Shared date for both images
        self.shared_remarks = ""  # Shared remarks for both images
        self.shared_dropdown_values = {}  # Store dropdown values for each image

        self.per_image_name = {}
        self.per_image_date = {}
        self.per_image_remarks = {}
        

        # Adjust path resolution for PyInstaller
        if getattr(sys, 'frozen', False):  # Check if running in a PyInstaller bundle
            base_path = sys._MEIPASS  # Temporary folder created by PyInstaller
        else:
            base_path = os.path.dirname(__file__)

        # Resolve the model path
        model_path = os.path.join(base_path, "model", "augmented_retinal_model.pth")

        self.predictor = RetinaDiseasePredictor(
            model_path=model_path, 
            threshold=0.5, 
            output_dir=os.path.join(base_path, "predictions")
        )

        self.connect_buttons()
        self.setup_shortcuts()  # Setup shortcuts
        self.setup_editable_fields()  # Setup editable fields
        self.setup_search_bar()  # Add method to set up the curved search bar
        self.setup_dropdown()  # Add method to set up the dropdown
        self.setup_dropdown_box_2()  # Add method to set up dropdownBox_2
        self.refresh_history_table()  # Populate the history table on startup

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

        self.ui.classificationLeftButton.clicked.connect(self.navigate_classification_left)
        self.ui.classificationRightButton.clicked.connect(self.navigate_classification_right)

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

        # Ensure buttons are raised to the front
        self.ui.classificationBackButton.raise_()
        self.ui.classificationLeftButton.raise_()
        self.ui.classificationRightButton.raise_()
        self.ui.dropdownBox.raise_()  # Raise the dropdown to ensure it appears on top
        self.ui.dropdownBox_2.raise_()  # Raise the dropdown to ensure it appears on top


        self.ui.leftButton.raise_()
        self.ui.rightButton.raise_()
        self.ui.imageName.raise_()  # Bring imageName QLabel to the front

        # Ensure the imagePlaceholder is visible
        self.ui.imagePlaceholder.setVisible(True)

    def setup_search_bar(self):
        """Customize the appearance of the search bar."""
        self.ui.searchBar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dcdcdc; /* Light gray border */
                border-radius: 15px; /* Rounded corners */
                padding: 8px 12px; /* Padding for text */
                background-color: #f9f9f9; /* Light background */
                font-size: 14px; /* Font size */
                color: #333; /* Text color */
            }
            QLineEdit:focus {
                background-color: #ffffff; /* White background on focus */
            }
        """)
        self.ui.searchBar.setPlaceholderText("Search...")  # Set placeholder text
        self.ui.searchBar.textChanged.connect(self.on_search_text_changed)  # Connect search bar to filter method

    def setup_dropdown(self):
        """Set up the dropdown for selecting OD (Left Eye) or OS (Right Eye)."""
        self.ui.dropdown = QComboBox(self.ui.dropdownBox)  # Create a QComboBox inside dropdownBox
        self.ui.dropdown.setGeometry(0, 0, self.ui.dropdownBox.width(), self.ui.dropdownBox.height())  # Match the size of dropdownBox
        self.ui.dropdown.addItem("Select Eye")  # Add a placeholder item
        self.ui.dropdown.addItems(["OD (Left Eye)", "OS (Right Eye)"])  # Add options to the dropdown
        self.ui.dropdown.setStyleSheet("""
            QComboBox {
                border: 2px solid #dcdcdc; /* Light gray border */
                border-radius: 15px; /* Rounded corners */
                padding: 8px 12px; /* Padding for text */
                background-color: #f9f9f9; /* Light background */
                font-size: 14px; /* Font size */
                color: #333; /* Text color */
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dcdcdc;
                selection-background-color: #f0f0f0;
            }
        """)  # Style the dropdown
        self.ui.dropdown.setCurrentIndex(0)  # Set the default selection to "Select Eye"
        self.ui.dropdown.raise_()  # Raise the dropdown to ensure it appears on top

        # Apply a similar style to the dropdownBox
        self.ui.dropdownBox.setStyleSheet("""
            QWidget {
                border: 2px solid #dcdcdc; /* Light gray border */
                border-radius: 15px; /* Rounded corners */
                background-color: #f9f9f9; /* Light background */
            }
        """)

    def setup_dropdown_box_2(self):
        """Set up the dropdown_2 for the history viewer."""
        self.ui.dropdown_2 = QComboBox(self.ui.dropdownBox_2)  # Create a QComboBox inside dropdownBox_2
        self.ui.dropdown_2.setGeometry(0, 0, self.ui.dropdownBox_2.width(), self.ui.dropdownBox_2.height())  # Match the size of dropdownBox_2
        self.ui.dropdown_2.setObjectName("dropdown_2")
        self.ui.dropdown_2.addItem("Select Eye")  # Add a placeholder item
        self.ui.dropdown_2.addItems(["OD (Left Eye)", "OS (Right Eye)"])  # Add options to the dropdown
        self.ui.dropdown_2.setStyleSheet("""
            QComboBox {
                border: 2px solid #dcdcdc; /* Light gray border */
                border-radius: 15px; /* Rounded corners */
                padding: 8px 12px; /* Padding for text */
                background-color: #f9f9f9; /* Light background */
                font-size: 14px; /* Font size */
                color: #333; /* Text color */
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dcdcdc;
                selection-background-color: #f0f0f0;
            }
        """)  # Style the dropdown
        self.ui.dropdown_2.setCurrentIndex(0)  # Set the default selection to "Select Eye"
        self.ui.dropdown_2.setEnabled(False)  # Initially lock the dropdown
        self.ui.dropdown_2.raise_()  # Ensure the dropdown appears on top

    def on_search_text_changed(self, text):
        """Filter the history table based on the search text and archived status."""
        records = self.db_manager.fetch_records(show_archived=False)  # Fetch only non-archived records
        filtered_records = [
            record for record in records
            if text.lower() in record.get("patient_name", "").lower() or
               text.lower() in record.get("notes", "").lower() or
               any(text.lower() in disease.lower() for disease in record.get("diagnosis", {}).keys())
        ]

        self.ui.historyTable.setRowCount(len(filtered_records))

        for row_idx, record in enumerate(filtered_records):
            # Load and resize image for each row
            image_path = record.get("image_path", "")
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Insert image in first column
            image_item = QTableWidgetItem()
            image_item.setData(Qt.DecorationRole, scaled_pixmap)  # Set image as decoration
            image_item.setData(Qt.UserRole, record["_id"])  # Store the unique _id in the custom data role
            self.ui.historyTable.setItem(row_idx, 0, image_item)

            # Insert other data into columns
            row_data = [
                record.get("eye", ""),  # Replace "file_name" with "eye"
                record.get("patient_name", ""),
                ", ".join(record.get("diagnosis", {}).keys()),
                record.get("date", ""),
                record.get("notes", "")
            ]
            for col_idx, text in enumerate(row_data, start=1):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.historyTable.setItem(row_idx, col_idx, item)

    def refresh_history_table(self, show_archived=False):
        """Refresh the history table to show all records, excluding archived ones by default."""
        # Define a mapping of full diagnosis names to their shortcuts
        diagnosis_shortcuts = {
            "Diabetic Retinopathy": "DR",
            "Normal": "NORMAL",
            "Media Haze": "MH",
            "Optic Disc Cupping": "ODC",
            "Tessellation": "TSLN",
            "Age-Related Macular Degeneration": "ARMD",
            "Drusen": "DN",
            "Myopia": "MYA",
            "Branch Retinal Vein Occlusion": "BRVO",
            "Optic Disc Pallor": "ODP",
            "Central Retinal Vein Occlusion": "CRVO",
            "Choroidal Neovascularization": "CNV",
            "Retinitis": "RS",
            "Optic Disc Edema": "ODE",
            "Laser Scars": "LS",
            "Central Serous Retinopathy": "CSR",
            "Hypertensive Retinopathy": "HTR",
            "Arteriosclerotic Retinopathy": "ASR",
            "Chorioretinitis": "CRS"
        }

        # Fetch all records from the database
        records = self.db_manager.fetch_records()

        # Filter records based on the archived status
        filtered_records = [
            record for record in records if record.get("archived", False) == show_archived
        ]

        self.ui.historyTable.setRowCount(len(filtered_records))

        for row_idx, record in enumerate(filtered_records):
            # Load and resize image for each row
            image_path = record.get("image_path", "")
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Insert image in first column
            image_item = QTableWidgetItem()
            image_item.setData(Qt.DecorationRole, scaled_pixmap)  # Set image as decoration
            image_item.setData(Qt.UserRole, record["_id"])  # Store the unique _id in the custom data role
            self.ui.historyTable.setItem(row_idx, 0, image_item)

            # Reverse map diagnosis names to shortcuts
            diagnosis = record.get("diagnosis", {})
            diagnosis_shortcuts_list = [
                diagnosis_shortcuts.get(name, name) for name in diagnosis.keys()
            ]

            # Insert other data into columns
            row_data = [
                record.get("eye", ""),
                record.get("patient_name", ""),
                ", ".join(diagnosis_shortcuts_list),  # Use shortcuts for diagnosis
                record.get("date", ""),
                record.get("notes", "")
            ]
            for col_idx, text in enumerate(row_data, start=1):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.historyTable.setItem(row_idx, col_idx, item)

    def archive_selected_record(self):
        """Prompt the user for confirmation before archiving the selected record."""
        selected_row = self.ui.historyTable.currentRow()
        if selected_row >= 0:
            record_id = self.ui.historyTable.item(selected_row, 0).data(Qt.UserRole)
            if record_id:
                # Confirmation prompt
                reply = QMessageBox.question(
                    self.ui,
                    "Confirm Archive",
                    "<span style='color: black;'>Are you sure you want to archive this record?</span>",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    try:
                        result = self.db_manager.collection.update_one(
                            {"_id": ObjectId(record_id)},
                            {"$set": {"archived": True}}
                        )
                        if result.modified_count > 0:
                            QMessageBox.information(
                                self.ui,
                                "Success",
                                "<span style='color: black;'>Record archived successfully!</span>",
                                QMessageBox.Ok
                            )
                        else:
                            QMessageBox.warning(
                                self.ui,
                                "Warning",
                                "<span style='color: black;'>Failed to archive the record.</span>",
                                QMessageBox.Ok
                            )
                    except Exception as e:
                        QMessageBox.critical(
                            self.ui,
                            "Error",
                            f"<span style='color: black;'>Failed to archive record: {e}</span>",
                            QMessageBox.Ok
                        )
                    # Refresh the history table
                    self.refresh_history_table()
            else:
                # Do not show a warning if the user cancels the action
                pass

    @Slot()
    def open_file_explorer_classification(self):
        """Allow selecting up to two images and display the first one."""
        # --- Clear dropdown and per-image fields before new upload ---
        self.shared_dropdown_values.clear()
        self.per_image_name.clear()
        self.per_image_date.clear()
        self.per_image_remarks.clear()
        # ------------------------------------------------------------

        file_paths, _ = QFileDialog.getOpenFileNames(
            None, "Select Images", "", "Images (*.tiff *.png *.jpeg *.jpg)"
        )
        if file_paths:
            if len(file_paths) > 2:
                QMessageBox.warning(
                    self.ui,
                    "Warning",
                    "<span style='color: black;'>You can only select up to two images.</span>",
                    QMessageBox.Ok
                )
                return

            self.image_paths = file_paths  # Store the selected images
            self.current_image_index = 0  # Start with the first image

            # Display the first image and its diagnosis
            result_dict = self.predictor.predict(self.image_paths[self.current_image_index])
            self.set_image_placeholder_classification(
                self.image_paths[self.current_image_index], result_dict["class_predictions"]
            )

            # Store shared name, date, and remarks
            self.shared_name = self.ui.nameValue.text()
            self.shared_date = self.ui.dateValue.text()
            self.shared_remarks = self.ui.remarkValue.text()

            # --- Initialize per-image fields for all images ---
            for idx, _ in enumerate(self.image_paths):
                self.per_image_name[idx] = self.shared_name
                self.per_image_date[idx] = self.shared_date
                self.per_image_remarks[idx] = self.shared_remarks
            # --------------------------------------------------

            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page
            self.update_classification_navigation_buttons()

    @Slot()
    def upload_new_image(self):
        """Handle uploading a single image and reset placeholders if successful."""
        # --- Clear dropdown and per-image fields before new upload ---
        self.shared_dropdown_values.clear()
        self.per_image_name.clear()
        self.per_image_date.clear()
        self.per_image_remarks.clear()
        # ------------------------------------------------------------

        file_path, _ = QFileDialog.getOpenFileName(None, "Select an Image", "", "Images (*.tiff *.png *.jpeg *.jpg)")
        if file_path:
            self.image_paths = [file_path]  # Replace the list with the single uploaded image
            self.current_image_index = 0  # Reset to the first image
            result_dict = self.predictor.predict(file_path)
            self.set_image_placeholder_classification(file_path, result_dict["class_predictions"])
            
            # Store shared name, date, and remarks
            self.shared_name = self.ui.nameValue.text()
            self.shared_date = self.ui.dateValue.text()
            self.shared_remarks = self.ui.remarkValue.text()

            # --- Initialize per-image fields for the single image ---
            self.per_image_name[0] = self.shared_name
            self.per_image_date[0] = self.shared_date
            self.per_image_remarks[0] = self.shared_remarks
            # -------------------------------------------------------

            # Do not save the record here; saving should only happen explicitly
            self.ui.stackedWidget.setCurrentIndex(2)  # Move to the classification page
            self.update_classification_navigation_buttons()

    def save_results(self):
        """Save all uploaded images and their respective diagnoses to the database."""
        if not self.image_paths:
            QMessageBox.warning(
                self.ui,
                "Warning",
                "<span style='color: black;'>No images to save!</span>",
                QMessageBox.Ok
            )
            return

        # --- Save current fields for the current image before saving ---
        self.shared_dropdown_values[self.current_image_index] = self.ui.dropdown.currentText()
        self.per_image_name[self.current_image_index] = self.ui.nameValue.text()
        self.per_image_date[self.current_image_index] = self.ui.dateValue.text()
        self.per_image_remarks[self.current_image_index] = self.ui.remarkValue.text()
        # --------------------------------------------------------------

        name = self.ui.nameValue.text()
        if not name.strip():  # Check if the name is empty
            QMessageBox.warning(
                self.ui,
                "Warning",
                "<span style='color: black;'>Name cannot be empty!</span>",
                QMessageBox.Ok
            )
            return

        date = self.ui.dateValue.text()
        remark = self.ui.remarkValue.text()

        if self.image_paths:
            self.shared_dropdown_values[self.current_image_index] = self.ui.dropdown.currentText()

        # Ensure each image has a corresponding dropdown value
        eye_selections = []
        for i, image_path in enumerate(self.image_paths):
            selected_eye = self.shared_dropdown_values.get(i, "Select Eye")
            if selected_eye == "Select Eye":  # Ensure a valid option is selected
                QMessageBox.warning(
                    self.ui,
                    "Warning",
                    f"<span style='color: black;'>Please select an eye (OD or OS) for image {i+1}!</span>",
                    QMessageBox.Ok
                )
                return
            eye_selections.append(selected_eye)

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

        # Save each image and its diagnosis
        for i, image_path in enumerate(self.image_paths):
            if not image_path.strip():  # Skip blank or invalid paths
                continue

            result_dict = self.predictor.predict(image_path)
            formatted_results = {
                disease_mapping.get(disease, disease): data["probability"]
                for disease, data in result_dict["class_predictions"].items() if data["prediction"] == 1
            }

            # Prepare the record to save
            record = {
                "image_path": image_path,
                "file_name": os.path.basename(image_path),
                "patient_name": self.per_image_name.get(i, self.shared_name),
                "eye": eye_selections[i],  # Use the corresponding eye selection for each image
                "diagnosis": formatted_results,
                "date": datetime.strptime(self.per_image_date.get(i, self.shared_date), "%B %d, %Y").strftime("%Y-%m-%d"),
                "notes": self.per_image_remarks.get(i, self.shared_remarks),
                "archived": False  # Set archived status to False by default
            }

            # Save the record to the database
            self.db_manager.save_record(record)

        # Refresh the history table after saving
        self.refresh_history_table()  # Ensure the table is updated after saving

        QMessageBox.information(
            self.ui,
            "Success",
            "<span style='color: black;'>All records saved successfully!</span>",
            QMessageBox.Ok
        )

    @Slot()
    def navigate_classification_left(self):
        """Navigate to the previous image in the classification view."""
        if self.current_image_index > 0:
            # --- Save current fields before switching ---
            self.shared_dropdown_values[self.current_image_index] = self.ui.dropdown.currentText()
            self.per_image_name[self.current_image_index] = self.ui.nameValue.text()
            self.per_image_date[self.current_image_index] = self.ui.dateValue.text()
            self.per_image_remarks[self.current_image_index] = self.ui.remarkValue.text()
            # --------------------------------------------

            self.current_image_index -= 1
            file_path = self.image_paths[self.current_image_index]
            result_dict = self.predictor.predict(file_path)
            self.set_image_placeholder_classification(file_path, result_dict["class_predictions"])
            self.update_classification_navigation_buttons()
            self.restore_shared_fields()

    @Slot()
    def navigate_classification_right(self):
        """Navigate to the next image in the classification view."""
        if self.current_image_index < len(self.image_paths) - 1:
            # --- Save current fields before switching ---
            self.shared_dropdown_values[self.current_image_index] = self.ui.dropdown.currentText()
            self.per_image_name[self.current_image_index] = self.ui.nameValue.text()
            self.per_image_date[self.current_image_index] = self.ui.dateValue.text()
            self.per_image_remarks[self.current_image_index] = self.ui.remarkValue.text()
            # --------------------------------------------

            self.current_image_index += 1
            file_path = self.image_paths[self.current_image_index]
            result_dict = self.predictor.predict(file_path)
            self.set_image_placeholder_classification(file_path, result_dict["class_predictions"])
            self.update_classification_navigation_buttons()
            self.restore_shared_fields()

    def restore_shared_fields(self):
        """Restore the shared name, date, remarks, and dropdown value for the current image."""
        # --- Restore per-image fields if available, else use shared values ---
        self.ui.nameValue.setText(self.per_image_name.get(self.current_image_index, self.shared_name))
        self.ui.dateValue.setText(self.per_image_date.get(self.current_image_index, self.shared_date))
        self.ui.remarkValue.setText(self.per_image_remarks.get(self.current_image_index, self.shared_remarks))
        self.ui.dropdown.setCurrentText(self.shared_dropdown_values.get(self.current_image_index, "Select Eye"))
        # ---------------------------------------------------------------------

    def reset_placeholders(self):
        """Reset the placeholders when exiting the upload or classification page."""
        self.ui.nameValue.clear()
        self.ui.remarkValue.clear()
        self.ui.resultPlaceholder.clear()
        self.ui.imagePlaceholder.clear()
        self.ui.imageName.clear()
        current_date = datetime.now().strftime("%B %d, %Y")
        self.ui.dateValue.setText(current_date)
        self.image_paths.clear()
        self.current_image_index = 0
        self.shared_name = ""
        self.shared_date = ""
        self.shared_remarks = ""
        self.shared_dropdown_values.clear()
        # --- Clear per-image fields as well ---
        self.per_image_name.clear()
        self.per_image_date.clear()
        self.per_image_remarks.clear()
        # --------------------------------------
        self.update_classification_navigation_buttons()

    def update_classification_navigation_buttons(self):
        """Update the visibility of classification navigation buttons."""
        self.ui.classificationLeftButton.setVisible(self.current_image_index > 0)
        self.ui.classificationRightButton.setVisible(self.current_image_index < len(self.image_paths) - 1)

    @Slot()
    def on_row_double_clicked(self, item):
        """Switch to the classification page when a row is double-clicked and set the image, result, name, date, and remark."""
        self.current_row = item.row()  # Update the current row
        self.update_record(self.current_row)

    def update_record(self, row):
        """Update the labels with the data from the specified row."""
        record_id = self.ui.historyTable.item(row, 0).data(Qt.UserRole)  # Get the _id from the custom data role
        print(f"Record ID for row {row}: {record_id}")  # Debug: Log the record ID

        try:
            # Fetch the record from the database using the _id
            record = self.db_manager.collection.find_one({"_id": ObjectId(record_id)})
        except Exception as e:
            print(f"Error fetching record for row {row}: {e}")
            record = None

        print(f"Record fetched for row {row}: {record}")  # Debug: Log the fetched record

        if record:
            result_dict = record.get("diagnosis", {})  # Get the result dictionary
            name_text = record.get("patient_name", "")  # Get the name text
            date_text = record.get("date", "")  # Get the date text
            remark_text = record.get("notes", "")  # Get the remark text
            eye_value = record.get("eye", "Select Eye")  # Get the eye value from the record

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
            full_result_text = ""
            for disease, probability in result_dict.items():
                if isinstance(probability, (int, float)):
                    full_result_text += f"{disease} ({probability * 100:.2f}%)\n\n"
                elif isinstance(probability, dict) and probability.get("prediction") == 1:
                    full_result_text += f"{disease} ({probability.get('probability', 0) * 100:.2f}%)\n\n"

            # Remove trailing newlines
            full_result_text = full_result_text.rstrip()

            # Convert date to "Month Day, Year" format
            formatted_date = datetime.strptime(date_text, "%Y-%m-%d").strftime("%B %d, %Y")

            # Update UI elements
            image_path = record.get("image_path", "")
            if image_path:
                self.set_image_placeholder_history(image_path)
                self.ui.resultPlaceholder_2.setText(full_result_text)
                self.ui.resultPlaceholder_2.setWordWrap(True)
                self.ui.resultPlaceholder_2.setFixedWidth(191)
                self.ui.resultPlaceholder_2.adjustSize()
                self.ui.resultPlaceholder_2.setVisible(True)
                self.ui.nameValue_2.setText(name_text)
                self.ui.dateValue_2.setText(formatted_date)
                self.ui.remarkValue_2.setText(remark_text)
                if isinstance(self.ui.dropdown_2, QComboBox):  # Ensure dropdown_2 is a QComboBox
                    self.ui.dropdown_2.setCurrentText(eye_value)  # Set the dropdown_2 value
                else:
                    print("dropdown_2 is not a QComboBox.")  # Debugging message
                self.ui.stackedWidget.setCurrentIndex(3)  # Move to history viewer

            # Update button visibility
            self.ui.leftButton.setVisible(self.current_row > 0)
            self.ui.rightButton.setVisible(self.current_row < self.ui.historyTable.rowCount() - 1)
        else:
            print(f"No record found for row {row}.")  # Debug: Log if no record is found

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

    def set_image_placeholder_classification(self, image_path, result_dict):
        """Set the image and classification results in the classification page."""
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
        image_name = os.path.basename(image_path)  # Extract the image name from the path
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

        # Format result text with full disease names and confidence scores
        result_text = "\n\n".join(
            f"{disease_mapping.get(disease, disease)} ({data['probability'] * 100:.2f}%)"
            for disease, data in result_dict.items() if data["prediction"] == 1
        )

        # Set the result text in the resultPlaceholder QLabel
        self.ui.resultPlaceholder.setText(result_text)
        self.ui.resultPlaceholder.setWordWrap(True)  # Enable word wrap
        self.ui.resultPlaceholder.setFixedWidth(191)  # Set fixed width to 191
        self.ui.resultPlaceholder.adjustSize()  # Adjust the size of the QLabel to fit the text

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

    def enable_editing(self):
        """Enable editing of nameValue_2, remarkValue_2, and dropdown_2 in the history viewer."""
        self.ui.nameValue_2.setReadOnly(False)
        self.ui.remarkValue_2.setReadOnly(False)
        self.ui.dropdown_2.setEnabled(True)  # Unlock dropdown_2 for editing

    def save_changes(self):
        """Save changes to the selected record in the history viewer."""
        name = self.ui.nameValue_2.text()
        remark = self.ui.remarkValue_2.text()
        eye_value = self.ui.dropdown_2.currentText()  # Get the selected value from dropdown_2

        selected_row = self.current_row
        if selected_row >= 0:
            record_id = self.ui.historyTable.item(selected_row, 0).data(Qt.UserRole)
            if self.db_manager.collection is not None:
                try:
                    # Update the record in the database
                    result = self.db_manager.collection.update_one(
                        {"_id": ObjectId(record_id)},
                        {"$set": {"patient_name": name, "notes": remark, "eye": eye_value}}  # Save changes to "eye"
                    )
                    if result.modified_count > 0:
                        QMessageBox.information(
                            self.ui,
                            "Success",
                            "<span style='color: black;'>Changes saved successfully!</span>",
                            QMessageBox.Ok
                        )
                    else:
                        QMessageBox.warning(
                            self.ui,
                            "Warning",
                            "<span style='color: black;'>No changes were made to the record.</span>",
                            QMessageBox.Ok
                        )
                except Exception as e:
                    QMessageBox.critical(
                        self.ui,
                        "Error",
                        f"<span style='color: black;'>Failed to save changes: {e}</span>",
                        QMessageBox.Ok
                    )
            else:
                QMessageBox.warning(
                    self.ui,
                    "Warning",
                    "<span style='color: black;'>Database connection is not established.</span>",
                    QMessageBox.Ok
                )

            # Refresh the history table
            self.refresh_history_table()

        # Disable editing
        self.ui.nameValue_2.setReadOnly(True)
        self.ui.remarkValue_2.setReadOnly(True)
        self.ui.dropdown_2.setEnabled(False)  # Lock dropdown_2 after saving

    def print_selected_record(self):
        """Prompt the user for confirmation before printing the selected record."""
        selected_row = self.ui.historyTable.currentRow()
        if selected_row >= 0:
            reply = QMessageBox.question(
                self.ui,
                "Confirm Print",
                "<span style='color: black;'>Are you sure you want to print this record?</span>",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                record_id = self.ui.historyTable.item(selected_row, 0).data(Qt.UserRole)
                record = self.db_manager.collection.find_one({"_id": ObjectId(record_id)}) if self.db_manager.collection is not None else None

                if record:
                    from fpdf import FPDF
                    import re

                    def strip_html_tags(text):
                        return re.sub(r'<[^>]+>', '', text)

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
                        "OTHER": ("Others", "Other retinal or ocular abnormalities not classified above.", "Condition")
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
                    pdf.cell(0, 10, "Ophthalmologist", ln=True)

                    # Save the PDF
                    filename = f"{record.get('patient_name', 'record').replace(' ', '_')}.pdf"
                    output_path = os.path.join(os.getcwd(), filename)
                    pdf.output(output_path)

                    # Open the PDF file
                    try:
                        if sys.platform == "win32":
                            os.startfile(output_path)
                        elif sys.platform == "darwin":
                            import subprocess
                            subprocess.run(["open", output_path])
                        else:
                            import subprocess
                            subprocess.run(["xdg-open", output_path])
                    except Exception as e:
                        QMessageBox.warning(self.ui, "Warning", f"Failed to open PDF: {e}", QMessageBox.Ok)

                    # Show success message
                    QMessageBox.information(
                        self.ui,
                        "Success",
                        f"<span style='color: black;'>PDF saved successfully at {output_path}</span>",
                        QMessageBox.Ok
                    )
                else:
                    QMessageBox.warning(
                        self.ui,
                        "Warning",
                        "<span style='color: black;'>No record found for the selected row.</span>",
                        QMessageBox.Ok
                    )
        else:
            QMessageBox.warning(
                self.ui,
                "Warning",
                "<span style='color: black;'>Please select a record to print.</span>",
                QMessageBox.Ok
            )