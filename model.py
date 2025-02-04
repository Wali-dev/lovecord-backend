from config import mongo

class Message:
    def __init__(self, recipient, message, songurl):
        self.recipient = recipient
        self.message = message
        self.songurl = songurl

    def save(self):
        message_collection = mongo.db.messages
        message_data = {
            "recipient": self.recipient,
            "message": self.message,
            "songurl": self.songurl
        }
        message_collection.insert_one(message_data)

    @staticmethod
    def find_by_recipient(recipient):
        message_collection = mongo.db.messages
        return message_collection.find({"recipient": recipient})

    @staticmethod
    def find_by_id(id):
        message_collection = mongo.db.messages
        return message_collection.find_one({"_id": id})  
