from config import mongo

class MessagePost:
    def __init__(self, recipient, message, songurl, songname, songimage, recipient_email, recipient_number):
        self.recipient = recipient
        self.message = message
        self.songurl = songurl
        self.songname = songname
        self.songimage = songimage
        self.recipient_email = recipient_email
        self.recipient_number = recipient_number


    def save(self):
        message_collection = mongo.db.messagePosts
        message_data = {
            "recipient": self.recipient,
            "message": self.message,
            "songurl": self.songurl,
            "songname": self.songname,
            "songimage": self.songimage,
            "recipient_email": self.recipient_email,
            "recipient_number": self.recipient_number
        }
        message_collection.insert_one(message_data)

    @staticmethod
    def find_by_recipient(recipient):
        message_collection = mongo.db.messagePosts
        return message_collection.find({"recipient": recipient})

    @staticmethod
    def find_by_id(id):
        message_collection = mongo.db.messagePosts
        return message_collection.find_one({"_id": id})  
