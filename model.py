from pymongo import MongoClient
from config import Config
from jsonschema import validate, ValidationError

class SongModel:
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client[Config.MONGO_DB_NAME]
            self.songs_collection = self.db["post"]

            self.post_schema = {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "required": True},
                    "recipient_name": {"type": "string", "required": True},
                    "message": {"type": "string"},
                    "song_url": {"type": "string", "required": True},
                },
                "required": ["user_id", "recipient_name", "song_name"],
                "additionalProperties": False  
            }
            print("Successfully connected to MongoDB and schema loaded!")
        except Exception as e:
            print(f"Error initializing SongModel: {e}")
            raise  

    def save_song(self, song_data):
        try:
            validate(instance=song_data, schema=self.song_schema)
            return self.songs_collection.insert_one(song_data)
        except ValidationError as e:
            print(f"Schema validation error: {e}")
            raise
        except Exception as e:
            print(f"Database error: {e}")
            raise
        
        
    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")