from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)   # Biến này bắt buộc tên 'app'

API_URL = "https://jwt.thug4ff.xyz/token"
OLD_CREDITS = "https://great.thug4ff.com/"
NEW_CREDITS = "https://checkmxt.top"

@app.route('/token', methods=['GET'])
def get_token():
    uid = request.args.get('uid', '').strip()
    password = request.args.get('password', '').strip()

    if not uid or not password:
        return jsonify({"error": "Thiếu uid hoặc password"}), 400

    try:
        resp = requests.get(API_URL, params={"uid": uid, "password": password}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if data.get("credits") == OLD_CREDITS:
        data["credits"] = NEW_CREDITS

    return jsonify(data)

# KHÔNG CÓ dòng app.run() ở đây
