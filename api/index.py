from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/send-otp', methods=['GET', 'POST'])
def send_otp():
    if request.method == 'POST':
        data = request.get_json() or request.form
    else:
        data = request.args

    token = data.get('access_token')
    email = data.get('email')
    
    if not token or not email:
        return jsonify({"success": False, "message": "Missing token or email"}), 400

    headers = {
        "User-Agent": "GarenaMSDK/4.0.35 (Android; 11; FF_BYPASS)",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-GA-SDK-VERSION": "4.0.35",
        "Host": "100067.connect.garena.com"
    }

    payload = {
        "email": email,
        "access_token": token,
        "app_id": "100067",
        "region": "BD",
        "locale": "en_PK"
    }

    try:
        r = requests.post("https://100067.connect.garena.com/game/account_security/bind:send_otp", data=payload, headers=headers)
        res = r.json()
        if res.get("result") == 0:
            return jsonify({"success": True, "message": "OTP sent successfully!"})
        return jsonify({"success": False, "message": f"Error: {res.get('error')}"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/')
def home(): return "API is Live - sameerpar"

def handler(event, context):
    return app(event, context)
