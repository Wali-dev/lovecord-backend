import datetime
import os
from flask import Flask, request, jsonify
from config import init_db, mongo
from model import MessagePost
from bson.objectid import ObjectId
import random
from flask_cors import CORS

app = Flask(__name__)

# Initialize the database connection
init_db(app)
CORS(app)


@app.route('/message', methods=['POST'])
def create_message():
    data = request.json
    
    # Validate required fields
    required_fields = ['recipient', 'message', 'songurl', 'songname', 'songimage']
    if not all(key in data for key in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        # Prepare message document
        message_data = {
            "recipient": data['recipient'],
            "message": data['message'],
            "songurl": data['songurl'],
            "songname": data['songname'],
            "songimgae": data['songimage'],
            "createdAt": datetime.utcnow()
        }
        
        # Add recipient_email only if it's present
        if 'recipient_email' in data:
            message_data['recipient_email'] = data['recipient_email']
        if 'recipient_number' in data:
            message_data['recipient_number'] = data['recipient_number']
        
        # Insert into database
        result = mongo.db.messages.insert_one(message_data)

        # Return inserted document ID
        return jsonify({
            "message": "Message created successfully",
            "id": str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/message/<id>', methods=['GET'])
def get_message_by_id(id):
   try:
       # Convert id to ObjectId
       message_id = ObjectId(id)
       
       # Find the message in the database
       message = mongo.db.messages.find_one({"_id": message_id})
       
       # Check if message exists
       if message:
           # Convert ObjectId to string for JSON serialization
           message['_id'] = str(message['_id'])
           if 'createdAt' in message:
               message['createdAt'] = message['createdAt'].isoformat()  # Convert to string for JSON
           return jsonify(message), 200
       else:
           return jsonify({"error": "Message not found"}), 404
   
   except Exception as e:
       return jsonify({"error": str(e)}), 500
   
@app.route('/messages/recipient', methods=['GET'])
def get_messages_by_recipient():
   recipient = request.args.get('recipient')
   page = int(request.args.get('page', 1))
   per_page = int(request.args.get('per_page', 10))

   if not recipient:
       return jsonify({"error": "Recipient is required"}), 400

   try:
       # Calculate skip value for pagination
       skip = (page - 1) * per_page

       # Find messages for the recipient with pagination
       messages = list(mongo.db.messages.find(
           {"recipient": recipient}
       ).skip(skip).limit(per_page))

       # Convert ObjectId to string
       for message in messages:
           message['_id'] = str(message['_id'])

       # Count total messages for this recipient
       total_messages = mongo.db.messages.count_documents({"recipient": recipient})

       return jsonify({
           "messages": messages,
           "page": page,
           "per_page": per_page,
           "total_messages": total_messages,
           "total_pages": -(-total_messages // per_page)  
       }), 200

   except Exception as e:
       return jsonify({"error": str(e)}), 500
   
@app.route('/messages/random', methods=['GET'])
def get_random_messages():
    try:
        # Fetch all message posts from the database
        messages = list(mongo.db.messages.find())
        
        # If there are more than 50 messages, randomly sample 50
        if len(messages) > 50:
            messages = random.sample(messages, 50)

        # Convert ObjectId to string for JSON serialization
        for message in messages:
            message['_id'] = str(message['_id'])

        return jsonify({"messages": messages}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)