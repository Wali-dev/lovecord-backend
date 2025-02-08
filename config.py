import os
from flask_pymongo import PyMongo
from dotenv import load_dotenv


load_dotenv()

mongo = PyMongo()

def init_db(app):
    mongo_uri = os.getenv("MONGO_URI")
    if mongo_uri:
        app.config["MONGO_URI"] = mongo_uri
    else:
        print("Mongo URI not found in .env file")
        return

    mongo.init_app(app)
    
    try:
        mongo.db.client.server_info() 
        print("Successfully connected to the MongoDB database")
    except Exception as e:
        print(f"Error connecting to the MongoDB database: {e}")
