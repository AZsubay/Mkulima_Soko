# app.py (add this section below your /ussd route)
'''
from flask import Flask, request, Response, render_template
from services.ussd import handle_ussd
from services.voice import handle_voice

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ussd", methods=["POST"])
def ussd():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")
    response = handle_ussd(session_id, service_code, phone_number, text)
    return Response(response, mimetype="text/plain")

@app.route("/voice", methods=["POST"])
def voice():
    response = handle_voice(request)
    return Response(response, mimetype='application/xml')

if __name__ == "__main__":
    app.run(debug=True)
'''
