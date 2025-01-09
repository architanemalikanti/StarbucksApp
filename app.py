from db import db
from flask import Flask, request
from db import db
from db import Barista, ShiftLead, PastryPull
import json





app = Flask(__name__)
db_filename = "starbucks.db"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///starbucks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQALCHEMY_ECHO"] = True

# Initialize the database
db.init_app(app)

#helper functions

def success_response(body, status=200):
    return json.dumps(body), status

def failure_response(error, status=404):
    return json.dumps({"error": error}), status

def extract_token(request):
    pass #TODO: implement this function

#register barista route:
@app.route("/registerBarista/", methods=["POST"])
def register_barista():
    body = json.loads(request.data)
    fullName=body.get('fullName')
    userName = body.get('userName')
    password = body.get('password')
    starbucksLocation = body.get('starbucksLocation')

    created, user=create_barista(userName, password, fullName, starbucksLocation)

    if not created:
        return failure_response("User already exists", 403)
    
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token

    })


#register log in route:
@app.route("/registerShiftLead/", methods=["POST"])
def register_ShiftLead():
    pass #TODO: implement this function 

#log in user route:
@app.route("/login/", methods=["POST"])
def login():
    pass #TODO: implement this function 








if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host="0.0.0.0", port=8000, debug=True)