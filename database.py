import pymongo

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

    def save_record(self, record):
        """Save a single record to the database."""
        if self.collection is not None:  # Explicitly check if collection is not None
            try:
                self.collection.insert_one(record)
                print("Record saved successfully.")
            except Exception as e:
                print(f"Error saving record: {e}")
        else:
            print("Database connection is not established.")
