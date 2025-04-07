from PySide6.QtWidgets import (
    QFileDialog, QLabel, QDialog, QVBoxLayout, QWidget, 
    QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Slot, Qt, QEvent
from PySide6.QtGui import QPixmap, QPainter, QCursor, QFont, QKeySequence, QShortcut
from datetime import datetime
import random
import json
import os
from database import DatabaseManager  # Import the DatabaseManager class
from history_handler import HistoryHandler  # Import the new HistoryHandler class

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked = None
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        if self.clicked:
            self.clicked(event)

class TransparentLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

class ButtonHandlers:
    def __init__(self, ui):
        self.ui = ui
        self.current_row = 0
        # Initialize the database manager
        self.db_manager = DatabaseManager()
        self.history_handler = HistoryHandler(ui, self.db_manager)  # Initialize HistoryHandler
        # Check if connected to MongoDB
        if not self.db_manager.is_connected():
            QMessageBox.warning(
                self.ui, 
                "Database Connection Error",
                "Could not connect to MongoDB. Results won't be saved."
            )
        self.connect_buttons()
        self.setup_shortcuts()
        self.setup_editable_fields()
        # Always load history data, even if the database is disconnected
        self.history_handler.refresh_history_table()

    def connect_buttons(self):
        """0 = titlepage, 1 = selectionpage, 2 = classificationpage, 3 = historyview, 4 = historypage"""
        self.ui.getStartedButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.uploadBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.historyBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.historyButton.clicked.connect(lambda: (self.history_handler.refresh_history_table(), self.ui.stackedWidget.setCurrentIndex(4)))
        self.ui.classificationBackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.xButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.leftButton.clicked.connect(self.navigate_left)
        self.ui.rightButton.clicked.connect(self.navigate_right)

        self.ui.uploadImageButton.clicked.connect(self.open_file_explorer_classification)
        self.ui.uploadNewImageButton.clicked.connect(self.upload_new_image)

        self.ui.historyTable.itemDoubleClicked.connect(self.on_row_double_clicked)

        self.ui.saveResultsButton.clicked.connect(self.save_results)
        self.ui.deleteButton.clicked.connect(self.delete_selected_record)
        self.ui.modifyRecordButton.clicked.connect(self.enable_editing)
        self.ui.saveChangesButton.clicked.connect(self.save_changes)
        

        self.replace_image_placeholder()
        self.replace_image_placeholder_classification()

        # Reset placeholders when exiting
        self.ui.uploadBackButton.clicked.connect(self.reset_placeholders)
        self.ui.classificationBackButton.clicked.connect(self.reset_placeholders)

    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.uploadBackButton, self.ui.uploadBackButton.click)
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.historyBackButton, self.ui.historyBackButton.click)
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.classificationBackButton, self.ui.classificationBackButton.click)
        QShortcut(QKeySequence(Qt.Key_Escape), self.ui.xButton, self.ui.xButton.click)
        QShortcut(QKeySequence(Qt.Key_Left), self.ui.leftButton, self.ui.leftButton.click)
        QShortcut(QKeySequence(Qt.Key_Right), self.ui.rightButton, self.ui.rightButton.click)

    def setup_editable_fields(self):
        """Setup editable fields for nameValue, dateValue, and remarkValue."""
        line_edit_stylesheet = """
        QLineEdit {
            background-color: rgb(244, 244, 244);
            color: black;
        }
        """

        # Replace nameValue QLabel with QLineEdit
        old_name_label = self.ui.nameValue
        self.ui.nameValue = QLineEdit(old_name_label.parent())
        self.ui.nameValue.setGeometry(old_name_label.geometry())
        self.ui.nameValue.setObjectName(old_name_label.objectName())
        self.ui.nameValue.setStyleSheet(line_edit_stylesheet)
        self.ui.nameValue.setAlignment(old_name_label.alignment())
        self.ui.nameValue.setFont(old_name_label.font())
        self.ui.nameValue.setPlaceholderText("Insert Name")
        self.ui.nameValue.setFrame(False)
        self.ui.nameValue.textChanged.connect(self.update_placeholder_visibility)

        # Set dateValue to the current date
        current_date = datetime.now().strftime("%B %d, %Y")
        self.ui.dateValue.setText(current_date)

        # Replace remarkValue QLabel with QLineEdit
        old_remark_label = self.ui.remarkValue
        self.ui.remarkValue = QLineEdit(old_remark_label.parent())
        self.ui.remarkValue.setGeometry(old_remark_label.geometry())
        self.ui.remarkValue.setObjectName(old_remark_label.objectName())
        self.ui.remarkValue.setStyleSheet(line_edit_stylesheet)
        self.ui.remarkValue.setAlignment(old_remark_label.alignment())
        self.ui.remarkValue.setFont(old_remark_label.font())
        self.ui.remarkValue.setPlaceholderText("Insert Remarks")
        self.ui.remarkValue.setFrame(False)
        self.ui.remarkValue.textChanged.connect(self.update_placeholder_visibility)

        # Replace nameValue_2 QLabel with QLineEdit
        old_name_label_2 = self.ui.nameValue_2
        self.ui.nameValue_2 = QLineEdit(old_name_label_2.parent())
        self.ui.nameValue_2.setGeometry(old_name_label_2.geometry())
        self.ui.nameValue_2.setObjectName(old_name_label_2.objectName())
        self.ui.nameValue_2.setStyleSheet(line_edit_stylesheet)
        self.ui.nameValue_2.setAlignment(old_name_label_2.alignment())
        self.ui.nameValue_2.setFont(old_name_label_2.font())
        self.ui.nameValue_2.setPlaceholderText("Insert Name")
        self.ui.nameValue_2.setFrame(False)
        self.ui.nameValue_2.setReadOnly(True)

        # Replace remarkValue_2 QLabel with QLineEdit
        old_remark_label_2 = self.ui.remarkValue_2
        self.ui.remarkValue_2 = QLineEdit(old_remark_label_2.parent())
        self.ui.remarkValue_2.setGeometry(old_remark_label_2.geometry())
        self.ui.remarkValue_2.setObjectName(old_remark_label_2.objectName())
        self.ui.remarkValue_2.setStyleSheet(line_edit_stylesheet)
        self.ui.remarkValue_2.setAlignment(old_remark_label_2.alignment())
        self.ui.remarkValue_2.setFont(old_remark_label_2.font())
        self.ui.remarkValue_2.setPlaceholderText("Insert Remarks")
        self.ui.remarkValue_2.setFrame(False)
        self.ui.remarkValue_2.setReadOnly(True)

    def update_placeholder_visibility(self):
        """Update the visibility of the placeholder text based on the content."""
        if not self.ui.nameValue.text():
            self.ui.nameValue.setPlaceholderText("Insert Name")
        if not self.ui.remarkValue.text():
            self.ui.remarkValue.setPlaceholderText("Insert Remarks")

    def replace_image_placeholder(self):
        """Replace the existing QLabel with ClickableLabel for imagePlaceholder_2."""
        old_label = self.ui.imagePlaceholder_2
        self.ui.imagePlaceholder_2 = ClickableLabel(old_label.parent())
        self.ui.imagePlaceholder_2.setGeometry(0, 0, 390, 292)
        self.ui.imagePlaceholder_2.setObjectName(old_label.objectName())
        self.ui.imagePlaceholder_2.setStyleSheet("background-color: transparent;")
        self.ui.imagePlaceholder_2.clicked = self.open_image_preview

        # Replace the existing QLabel with TransparentLabel for imageName_2
        old_image_name_label = self.ui.imageName_2
        self.ui.imageName_2 = TransparentLabel(old_image_name_label.parent())
        self.ui.imageName_2.setGeometry(169, 266, 211, 20)
        self.ui.imageName_2.setObjectName(old_image_name_label.objectName())
        self.ui.imageName_2.setStyleSheet("color: white; text-align: right; font: 450 italic 13pt 'SF Pro Display';")
        self.ui.imageName_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.ui.xButton.raise_()
        self.ui.leftButton.raise_()
        self.ui.rightButton.raise_()
        self.ui.imageName_2.raise_()
        self.ui.imagePlaceholder_2.setVisible(True)

    def replace_image_placeholder_classification(self):
        """Replace the existing QLabel with ClickableLabel for imagePlaceholder."""
        old_label = self.ui.imagePlaceholder
        self.ui.imagePlaceholder = ClickableLabel(old_label.parent())
        self.ui.imagePlaceholder.setGeometry(0, 0, 390, 292)
        self.ui.imagePlaceholder.setObjectName(old_label.objectName())
        self.ui.imagePlaceholder.setStyleSheet("background-color: transparent;")
        self.ui.imagePlaceholder.clicked = self.open_image_preview_classification

        # Replace the existing QLabel with TransparentLabel for imageName
        old_image_name_label = self.ui.imageName
        self.ui.imageName = TransparentLabel(old_image_name_label.parent())
        self.ui.imageName.setGeometry(169, 266, 211, 20)
        self.ui.imageName.setObjectName(old_image_name_label.objectName())
        self.ui.imageName.setStyleSheet("color: white; text-align: right; font: 450 italic 13pt 'SF Pro Display';")
        self.ui.imageName.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.ui.imageName.raise_()
        self.ui.imagePlaceholder.setVisible(True)

    @Slot()
    def open_file_explorer_classification(self):
        """Opens a file dialog and switches to the classification page if a file is selected."""
        file_path, _ = QFileDialog.getOpenFileName(None, "Select an Image", "", "Images (*.tiff *.png *.jpeg *.jpg)")
        if file_path:
            self.set_image_placeholder_classification(file_path)
            self.ui.stackedWidget.setCurrentIndex(2)
            # Store image path for saving later
            self.ui.current_image_path = file_path

    def set_image_placeholder_classification(self, image_path):
        """Set the image in the imagePlaceholder (classification page)."""
        pixmap = QPixmap(image_path)
        label_size = self.ui.imagePlaceholder.size()
        scaled_pixmap = pixmap.scaledToHeight(292, Qt.SmoothTransformation)

        final_pixmap = QPixmap(label_size)
        final_pixmap.fill(Qt.transparent)

        painter = QPainter(final_pixmap)
        x = (label_size.width() - scaled_pixmap.width()) // 2
        y = (label_size.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()

        self.ui.imagePlaceholder.setPixmap(final_pixmap)
        self.ui.imagePlaceholder.setScaledContents(False)
        self.ui.imagePlaceholder.setProperty("imagePath", image_path)

        # Set the image name
        image_name = image_path.split("/")[-1]
        self.ui.imageName.setText(image_name)

        # Reset placeholders
        self.ui.nameValue.setPlaceholderText("Insert Name")
        self.ui.remarkValue.setPlaceholderText("Insert Remarks")

        # Generate random diseases with random percentages
        diseases = [
            "DR", "NORMAL", "MH", "ODC", "TSLN", "ARMD", "MYA", "BRVO", "ODP", 
            "CRVO", "CNV", "RS", "ODE", "LS", "CSR", "HTR", "ASR", "CRS", "OTHER"
        ]
        num_diseases = random.choices([1, 2, 3], weights=[50, 30, 20], k=1)[0]
        selected_diseases = random.sample(diseases, num_diseases)
        result_dict = { disease: round(random.uniform(0.5, 1.0), 2) for disease in selected_diseases }

        # Store the prediction results for later saving
        self.ui.prediction_results = result_dict

        # Mapping to expand codes to full names
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

        # Format results
        full_result_text = "\n\n".join(
            f"{disease_mapping.get(disease, disease)} ({confidence:.2f}%)"
            for disease, confidence in result_dict.items()
        )

        self.ui.resultPlaceholder.setText(full_result_text)
        self.ui.resultPlaceholder.setWordWrap(True)
        self.ui.resultPlaceholder.setFixedWidth(191)
        self.ui.resultPlaceholder.adjustSize()

    @Slot()
    def on_row_double_clicked(self, item):
        """Handle double-clicking a row in the history table."""
        self.history_handler.update_record(item.row())

    @Slot()
    def navigate_left(self):
        """Navigate to previous record."""
        if self.current_row > 0:
            self.current_row -= 1
            record_id_item = self.ui.historyTable.item(self.current_row, 6)
            if record_id_item:
                record_id = record_id_item.text()
                self.history_handler.update_record(self.current_row, record_id)
            else:
                self.history_handler.update_record(self.current_row)

    @Slot()
    def navigate_right(self):
        """Navigate to next record."""
        if self.current_row < self.ui.historyTable.rowCount() - 1:
            self.current_row += 1
            record_id_item = self.ui.historyTable.item(self.current_row, 6)
            if record_id_item:
                record_id = record_id_item.text()
                self.history_handler.update_record(self.current_row, record_id)
            else:
                self.history_handler.update_record(self.current_row)

    @Slot()
    def open_image_preview(self, event):
        """Open a larger preview of the image (history viewer) if available."""
        image_path = self.ui.imagePlaceholder_2.property("imagePath")
        if image_path:
            pixmap = QPixmap(image_path)
            dialog = QDialog(self.ui)
            dialog.setWindowTitle("Image Preview")
            layout = QVBoxLayout(dialog)
            label = QLabel(dialog)
            max_width = 800
            scaled_pixmap = pixmap.scaled(max_width, max_width, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled_pixmap)
            layout.addWidget(label)
            dialog.setLayout(layout)
            dialog.setFixedSize(dialog.sizeHint())
            dialog.exec()

    @Slot()
    def open_image_preview_classification(self, event):
        """Open a larger preview of the image (classification) if available."""
        image_path = self.ui.imagePlaceholder.property("imagePath")
        if image_path:
            pixmap = QPixmap(image_path)
            dialog = QDialog(self.ui)
            dialog.setWindowTitle("Image Preview")
            layout = QVBoxLayout(dialog)
            label = QLabel(dialog)
            max_width = 800
            scaled_pixmap = pixmap.scaled(max_width, max_width, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled_pixmap)
            layout.addWidget(label)
            dialog.setLayout(layout)
            dialog.setFixedSize(dialog.sizeHint())
            dialog.exec()

    def save_results(self):
        """Save results to MongoDB."""
        if not self.db_manager.is_connected():
            QMessageBox.warning(self.ui, "Warning", "Not connected to MongoDB. Unable to save results.")
            return
            
        name = self.ui.nameValue.text()
        if not name:
            QMessageBox.warning(self.ui, "Warning", "Name cannot be empty!")
            return
            
        try:
            image_path = getattr(self.ui, "current_image_path", "")
            patient_name = self.ui.nameValue.text()
            date = self.ui.dateValue.text()
            remarks = self.ui.remarkValue.text()
            prediction_scores = getattr(self.ui, "prediction_results", {})
            
            inserted_id = self.db_manager.save_results(
                image_path,
                patient_name,
                prediction_scores,
                date,
                remarks
            )
            
            # Use a custom QMessageBox to have better control over styling
            success_message = QMessageBox(self.ui)
            success_message.setIcon(QMessageBox.Information)
            success_message.setWindowTitle("Success")
            success_message.setText("<span style='color: black; font-weight: bold;'>Results saved to database</span>")
            success_message.setStandardButtons(QMessageBox.Ok)
            success_message.exec()
            
            self.history_handler.refresh_history_table()
            
        except Exception as e:
            QMessageBox.critical(
                self.ui,
                "Error",
                f"Failed to save results: {str(e)}"
            )

    @Slot()
    def upload_new_image(self):
        """Handle uploading a new image, reset placeholders, go to classification page."""
        file_path, _ = QFileDialog.getOpenFileName(None, "Select an Image", "", "Images (*.tiff *.png *.jpeg *.jpg)")
        if file_path:
            self.reset_placeholders()
            self.set_image_placeholder_classification(file_path)
            self.ui.current_image_path = file_path
            self.ui.stackedWidget.setCurrentIndex(2)

    def reset_placeholders(self):
        """Reset the placeholders when leaving upload/classification."""
        self.ui.nameValue.clear()
        self.ui.remarkValue.clear()
        self.ui.resultPlaceholder.clear()
        self.ui.imagePlaceholder.clear()
        self.ui.imageName.clear()
        self.ui.current_image_path = ""
        self.ui.prediction_results = {}
        current_date = datetime.now().strftime("%B %d, %Y")
        self.ui.dateValue.setText(current_date)

    def delete_selected_record(self):
        """Delete the selected record from MongoDB using the record ID from the hidden column."""
        if not self.db_manager.is_connected():
            QMessageBox.warning(self.ui, "Warning", "Not connected to MongoDB. Unable to delete record.")
            return

        row = self.ui.historyTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.ui, "Warning", "No row selected to delete.")
            return

        record_id_item = self.ui.historyTable.item(row, 6)
        if not record_id_item or not record_id_item.text():
            QMessageBox.warning(self.ui, "Warning", "No record selected to delete.")
            return

        record_id = record_id_item.text()

        reply = QMessageBox.question(
            self.ui,
            "Confirm Deletion",
            "Are you sure you want to delete this record?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.db_manager.delete_record(record_id)
                QMessageBox.information(self.ui, "Success", "Record deleted successfully.")
                self.ui.stackedWidget.setCurrentIndex(4)
                self.history_handler.refresh_history_table()
            except Exception as e:
                QMessageBox.critical(self.ui, "Error", f"Failed to delete record: {str(e)}")

    def enable_editing(self):
        """
        Allow the user to edit `nameValue_2` and `remarkValue_2` fields on the history viewer page.
        """
        self.ui.nameValue_2.setReadOnly(False)
        self.ui.remarkValue_2.setReadOnly(False)
        self.ui.modifyRecordButton.setEnabled(False)
        self.ui.saveChangesButton.setEnabled(True)
        editable_stylesheet = """
        QLineEdit {
            background-color: #FFFFFF;
            color: black;
            border: 1px solid #999999;
        }
        """
        self.ui.nameValue_2.setStyleSheet(editable_stylesheet)
        self.ui.remarkValue_2.setStyleSheet(editable_stylesheet)

    def save_changes(self):
        """
        Save changes back to the database for the currently viewed record in the history viewer page.
        """
        if not self.db_manager.is_connected():
            QMessageBox.warning(self.ui, "Warning", "Not connected to MongoDB. Unable to save changes.")
            return

        record_id = getattr(self.ui, "current_record_id", None)
        if not record_id:
            QMessageBox.warning(self.ui, "Warning", "No record selected to update.")
            return

        try:
            updated_name = self.ui.nameValue_2.text()
            updated_remarks = self.ui.remarkValue_2.text()
            updated_fields = {
                "patient_name": updated_name,
                "remarks": updated_remarks
            }
            self.db_manager.update_record(record_id, updated_fields)
            QMessageBox.information(self.ui, "Success", "Record updated successfully.")
            self.ui.nameValue_2.setReadOnly(True)
            self.ui.remarkValue_2.setReadOnly(True)
            self.ui.modifyRecordButton.setEnabled(True)
            self.ui.saveChangesButton.setEnabled(False)
            read_only_stylesheet = """
            QLineEdit {
                background-color: rgb(244, 244, 244);
                color: black;
                border: none;
            }
            """
            self.ui.nameValue_2.setStyleSheet(read_only_stylesheet)
            self.ui.remarkValue_2.setStyleSheet(read_only_stylesheet)
            self.history_handler.refresh_history_table()
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", f"Failed to save changes: {str(e)}")