from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

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
        resp.raise_for_status()  # nếu status >= 400, ném ngoại lệ
        data = resp.json()
    except requests.exceptions.HTTPError as e:
        # Bắt riêng lỗi HTTP (400, 401, 403...)
        return jsonify({"error": "Yêu cầu không hợp lệ, vui lòng kiểm tra uid và password"}), 400
    except requests.exceptions.RequestException as e:
        # Lỗi kết nối, timeout, v.v.
        return jsonify({"error": "Lỗi kết nối đến máy chủ"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Dữ liệu trả về không đúng định dạng"}), 500

    # Sửa trường credits
    if data.get("credits") == OLD_CREDITS:
        data["credits"] = NEW_CREDITS

    return jsonify(data)

# Không có app.run() khi chạy trên Vercel
