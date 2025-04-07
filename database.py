import os
import json
import pymongo
from datetime import datetime
from bson import ObjectId
from PySide6.QtWidgets import QMessageBox

class DatabaseManager:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """Initialize the database manager with MongoDB connection string."""
        try:
            self.client = pymongo.MongoClient(connection_string)
            self.db = self.client["medical_database"]
            self.collection = self.db["prediction_records"]
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None
            self.collection = None

    def is_connected(self):
        """Check if connection to MongoDB is established."""
        if self.client is None:
            return False
        try:
            self.client.admin.command("ismaster")
            return True
        except Exception:
            return False

    def save_results(self, image_path, patient_name, prediction_scores, date, remarks):
        """Save prediction results to MongoDB."""
        if not self.is_connected():
            raise ConnectionError("Not connected to MongoDB")
        try:
            if isinstance(date, str):
                try:
                    date_obj = datetime.strptime(date, "%B %d, %Y")
                    date_str = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    date_str = date
            else:
                date_str = date.strftime("%Y-%m-%d")
            document = {
                "image_path": image_path,
                "image_name": os.path.basename(image_path),
                "patient_name": patient_name,
                "prediction_scores": prediction_scores,
                "date": date_str,
                "remarks": remarks,
                "timestamp": datetime.now()
            }
            result = self.collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            print(f"Error saving to MongoDB: {e}")
            raise

    def get_all_records(self):
        """Retrieve all records from MongoDB sorted by timestamp in descending order."""
        if not self.is_connected():
            print("Database connection is not established.")
            raise ConnectionError("Not connected to MongoDB")
        try:
            print("Querying all records from the database...")
            # Use MongoDB's native sort capability - sort by timestamp in descending order (-1)
            # This will ensure the newest records come first
            records = list(self.collection.find().sort("timestamp", -1))
            print(f"Retrieved {len(records)} records.")
            return records
        except Exception as e:
            print(f"Error retrieving records from MongoDB: {e}")
            raise

    def delete_record(self, record_id):
        """Delete a record by ID (converting the provided string to ObjectId)."""
        if not self.is_connected():
            raise ConnectionError("Not connected to MongoDB")
        try:
            # Convert the record_id string to a proper ObjectId
            obj_id = ObjectId(record_id)
        except Exception as e:
            print(f"Invalid record ID '{record_id}': {e}")
            raise ValueError("Invalid record ID provided for deletion.")
        result = self.collection.delete_one({"_id": obj_id})
        print("Deleted count:", result.deleted_count)
        return result

    def update_record(self, record_id, updated_data):
        """Update an existing record."""
        if not self.is_connected():
            raise ConnectionError("Not connected to MongoDB")
        try:
            obj_id = ObjectId(record_id)
        except Exception as e:
            print(f"Invalid record ID '{record_id}': {e}")
            raise ValueError("Invalid record ID provided for update.")
        return self.collection.update_one({"_id": obj_id}, {"$set": updated_data})

    def find_by_patient_name(self, patient_name):
        """Find records by patient name."""
        if not self.is_connected():
            raise ConnectionError("Not connected to MongoDB")
        return list(self.collection.find({"patient_name": {"$regex": patient_name, "$options": "i"}}))

    def find_by_diagnosis(self, diagnosis_key, min_confidence=0.5):
        """Find records with specific diagnosis above a confidence threshold."""
        if not self.is_connected():
            raise ConnectionError("Not connected to MongoDB")
        query = {f"prediction_scores.{diagnosis_key}": {"$gte": min_confidence}}
        return list(self.collection.find(query))

    def find_by_date_range(self, start_date, end_date):
        """Find records within a date range."""
        if not self.is_connected():
            raise ConnectionError("Not connected to MongoDB")
        query = {"date": {"$gte": start_date, "$lte": end_date}}
        return list(self.collection.find(query))

    def initialize_with_sample_data(self, sample_data):
        """
        Seed the database with sample data.
        sample_data is expected to be a list of lists, matching your record structure.
        """
        if not self.is_connected():
            raise ConnectionError("Not connected to MongoDB")
        try:
            count = 0
            for data in sample_data:
                image_path = data[0] if data[0] else f"data/{data[1]}"
                document = {
                    "image_path": image_path,
                    "image_name": data[1],
                    "patient_name": data[2],
                    "prediction_scores": data[3],
                    "date": data[4],
                    "remarks": data[5],
                    "timestamp": datetime.now()
                }
                self.collection.insert_one(document)
                count += 1
            return count
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise