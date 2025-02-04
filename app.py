from flask import Flask
from config import init_db

app = Flask(__name__)

# Initialize the database connection
init_db(app)

if __name__ == '__main__':
    app.run(debug=True)
