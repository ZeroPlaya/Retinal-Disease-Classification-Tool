from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QPainter
from bson import ObjectId
from datetime import datetime
import os

class HistoryHandler:
    def __init__(self, ui, db_manager):
        self.ui = ui
        self.db_manager = db_manager
        self.current_row = 0

        # Connect the table's selection change signal to a handler
        self.ui.historyTable.itemSelectionChanged.connect(self.on_row_selected)
        self.ui.historyTable.itemDoubleClicked.connect(self.on_row_double_clicked)

    def on_row_selected(self):
        """Handle row selection changes in the history table."""
        print("Row selection changed")
        selected_row = self.ui.historyTable.currentRow()
        if selected_row >= 0:  # Ensure a valid row is selected
            print(f"Selected row: {selected_row}")
            self.update_record(selected_row)

    @Slot()
    def on_row_double_clicked(self, item):
        """Switch to the history viewer page when a row is double-clicked and set the image, result, name, date, and remark."""
        self.current_row = item.row()  # Update the current row
        self.update_record(self.current_row)

    def refresh_history_table(self):
        """Refresh the history table with data from MongoDB."""
        if not self.db_manager.is_connected():
            QMessageBox.warning(self.ui, "Warning", "Not connected to MongoDB. Unable to load history.")
            return
        try:
            # Clear the table before populating it
            self.ui.historyTable.setRowCount(0)
            # Retrieve all records from the database
            records = self.db_manager.get_all_records()
            if not records:
                print("No records found in the database.")  # Debug print
            else:
                print(f"Retrieved {len(records)} records from the database.")  # Debug print
            
            for record in records:
                row_position = self.ui.historyTable.rowCount()
                self.ui.historyTable.insertRow(row_position)

                # Column 0: Preview (thumbnail)
                image_path = record.get("image_path", "")
                pixmap = QPixmap(image_path)
                if pixmap.isNull():
                    pixmap = QPixmap(64, 64)
                    pixmap.fill(Qt.gray)

                scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                preview_item = QTableWidgetItem()
                preview_item.setData(Qt.DecorationRole, scaled_pixmap)
                preview_item.setData(Qt.UserRole, image_path)
                self.ui.historyTable.setItem(row_position, 0, preview_item)

                # Column 1: File name
                self.ui.historyTable.setItem(row_position, 1, QTableWidgetItem(record.get("image_name", "")))

                # Column 2: Patient name
                self.ui.historyTable.setItem(row_position, 2, QTableWidgetItem(record.get("patient_name", "")))

                # Column 3: Results (disease abbreviations)
                scores = record.get("prediction_scores", {})
                diagnosis_text = ", ".join(scores.keys()) if scores else "N/A"
                self.ui.historyTable.setItem(row_position, 3, QTableWidgetItem(diagnosis_text))

                # Column 4: Date
                self.ui.historyTable.setItem(row_position, 4, QTableWidgetItem(record.get("date", "")))

                # Column 5: Comment (remarks)
                self.ui.historyTable.setItem(row_position, 5, QTableWidgetItem(record.get("remarks", "")))

                # Column 6: Record ID (hidden)
                record_id_item = QTableWidgetItem(str(record.get("_id", "")))
                record_id_item.setFlags(record_id_item.flags() & ~Qt.ItemIsEditable)
                self.ui.historyTable.setItem(row_position, 6, record_id_item)

            print(f"Number of rows added to the table: {self.ui.historyTable.rowCount()}")  # Debug print

            # Connect selection change to print database values
            self.ui.historyTable.itemSelectionChanged.connect(self.print_selected_record)

        except Exception as e:
            print(f"Error retrieving records from MongoDB: {e}")  # Debug print
            QMessageBox.critical(self.ui, "Error", f"Failed to load history data: {str(e)}")

    def print_selected_record(self):
        """Print the values of the selected record from the database."""
        selected_row = self.ui.historyTable.currentRow()
        if selected_row < 0:
            print("No row selected.")  # Debug print
            return

        # Retrieve the record ID from the hidden column
        record_id_item = self.ui.historyTable.item(selected_row, 6)
        if not record_id_item:
            print("No record ID found for the selected row.")  # Debug print
            return

        record_id = record_id_item.text()
        try:
            # Fetch the record from the database
            record = self.db_manager.collection.find_one({"_id": ObjectId(record_id)})
            if not record:
                print(f"No record found in the database for ID: {record_id}")  # Debug print
                return

            # Print the record details
            print("Selected Record Details:")
            print(f"  ID: {record_id}")
            print(f"  Patient Name: {record.get('patient_name', 'N/A')}")
            print(f"  Date: {record.get('date', 'N/A')}")
            print(f"  Remarks: {record.get('remarks', 'N/A')}")
            print(f"  Prediction Scores: {record.get('prediction_scores', {})}")
            print(f"  Image Path: {record.get('image_path', 'N/A')}")

        except Exception as e:
            print(f"Error retrieving record from database: {e}")  # Debug print

    def update_record(self, row):
        """Update the labels with the data from the specified row."""
        print(f"Updating record for row: {row}")

        # Get the file path from the custom data role in the first column
        image_path = self.ui.historyTable.item(row, 0).data(Qt.UserRole)
        print(f"Image path: {image_path}")
        if not image_path:
            print("Error: Image path is empty or invalid.")
            QMessageBox.warning(self.ui, "Warning", "Image path is missing or invalid.")
            return

        # Retrieve other data from the table
        name_text = self.ui.historyTable.item(row, 2).text()  # Patient name
        date_text = self.ui.historyTable.item(row, 4).text()  # Date
        remark_text = self.ui.historyTable.item(row, 5).text()  # Remarks
        print(f"Name: {name_text}, Date: {date_text}, Remarks: {remark_text}")

        # Retrieve prediction scores from the database using the record ID
        record_id_item = self.ui.historyTable.item(row, 6)
        if not record_id_item:
            print("Error: Record ID item is None.")
            QMessageBox.warning(self.ui, "Warning", "Record ID is missing.")
            return

        record_id = record_id_item.text()
        print(f"Record ID: {record_id}")
        try:
            record = self.db_manager.collection.find_one({"_id": ObjectId(record_id)})
        except Exception as e:
            print(f"Error retrieving record from database: {e}")
            QMessageBox.critical(self.ui, "Error", f"Failed to retrieve record: {e}")
            return

        if not record:
            print(f"Error: Record with ID {record_id} not found in the database.")
            QMessageBox.warning(self.ui, "Warning", "Record not found in the database.")
            return

        print(f"Record found: {record}")

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
        prediction_scores = record.get("prediction_scores", {})
        full_result_text = "\n\n".join(
            f"{disease_mapping.get(disease, disease)} ({confidence:.2f}%)"
            for disease, confidence in prediction_scores.items()
        )
        print(f"Formatted prediction scores: {full_result_text}")

        # Convert date to "Month Day, Year" format
        try:
            formatted_date = datetime.strptime(date_text, "%Y-%m-%d").strftime("%B %d, %Y")
        except ValueError as e:
            print(f"Error formatting date: {e}")
            QMessageBox.warning(self.ui, "Warning", f"Invalid date format: {date_text}")
            return

        print(f"Formatted date: {formatted_date}")

        # Update placeholders
        if image_path:
            self.set_image_placeholder_history(image_path)
        self.ui.resultPlaceholder_2.setText(full_result_text)
        self.ui.resultPlaceholder_2.setWordWrap(True)
        self.ui.resultPlaceholder_2.setFixedWidth(191)
        self.ui.resultPlaceholder_2.adjustSize()
        self.ui.nameValue_2.setText(name_text)
        self.ui.dateValue_2.setText(formatted_date)
        self.ui.remarkValue_2.setText(remark_text)

        # Switch to history viewer page
        self.ui.stackedWidget.setCurrentIndex(3)

        # Update navigation buttons
        self.ui.leftButton.setVisible(row > 0)
        self.ui.rightButton.setVisible(row < self.ui.historyTable.rowCount() - 1)
        
    def set_image_placeholder_history(self, image_path):
        """Set the image in the imagePlaceholder_2 QLabel for the history viewer page."""
        pixmap = QPixmap(image_path)
        label_size = self.ui.imagePlaceholder_2.size()
        scaled_pixmap = pixmap.scaledToHeight(292, Qt.SmoothTransformation)

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
        self.ui.imagePlaceholder_2.setScaledContents(False)
        self.ui.imagePlaceholder_2.setProperty("imagePath", image_path)

        # Set the image name in the imageName QLabel
        image_name = os.path.basename(image_path)
        self.ui.imageName_2.setText(image_name)

    def format_prediction_scores(self, scores):
        """Format prediction scores for display."""
        if not scores:
            return "No prediction data available"
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
        return "\n\n".join(
            f"{disease_mapping.get(disease, disease)} ({confidence:.2f}%)"
            for disease, confidence in scores.items()
        )