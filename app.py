# app.py
from flask import Flask, request
from services.ussd import handle_ussd
#from services.voice import handle_voice
import os
from dotenv import load_dotenv
import africastalking

#DB initialization
from database import init_db
init_db()

# Load environment variables
load_dotenv()

# Initialize Africa's Talking
AT_USERNAME = os.getenv("AT_USERNAME")
AT_API_KEY = os.getenv("AT_API_KEY")
africastalking.initialize(AT_USERNAME, AT_API_KEY)
sms = africastalking.SMS

app = Flask(__name__)


@app.route("/ussd", methods=["POST"])
def ussd():
    session_id = request.values.get("sessionId", "")
    service_code = request.values.get("serviceCode", "")
    phone_number = request.values.get("phoneNumber", "")
    text = request.values.get("text", "")

    response = handle_ussd(session_id, service_code, phone_number, text)
    return response

'''
@app.route("/voice", methods=["POST"])
def voice():
    return handle_voice()
'''

@app.route("/")
def home():
    return "Mkulima Soko USSD is Running!"


if __name__ == "__main__":
    app.run(debug=True)
