# server.py
from flask import Flask, request, jsonify, send_file
import os
import socket

app = Flask(__name__, static_folder="web", static_url_path="")

# -----------------------------
# IP取得
# -----------------------------
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# -----------------------------
# Web UI 配信
# -----------------------------
@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/server-info")
def server_info():
    return jsonify({"ip": get_ip(), "port": 5000})

# -----------------------------
# 共有データ
# -----------------------------
shared = {
    "text": "",
    "url": "",
    "screenshot_path": None,
    "file_path": None
}

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# テキスト
# -----------------------------
@app.route("/send-text", methods=["POST"])
def send_text():
    shared["text"] = request.json.get("text", "")
    return jsonify({"status": "ok"})

@app.route("/receive-text", methods=["GET"])
def receive_text():
    return jsonify({"text": shared["text"]})

# -----------------------------
# URL
# -----------------------------
@app.route("/send-url", methods=["POST"])
def send_url():
    shared["url"] = request.json.get("url", "")
    return jsonify({"status": "ok"})

@app.route("/receive-url", methods=["GET"])
def receive_url():
    return jsonify({"url": shared["url"]})

# -----------------------------
# スクショ
# -----------------------------
@app.route("/send-screenshot", methods=["POST"])
def send_screenshot():
    file = request.files["file"]
    save_path = os.path.join(DATA_DIR, "screenshot.png")
    file.save(save_path)
    shared["screenshot_path"] = save_path
    return jsonify({"status": "ok"})

@app.route("/receive-screenshot", methods=["GET"])
def receive_screenshot():
    if shared["screenshot_path"] and os.path.exists(shared["screenshot_path"]):
        return send_file(shared["screenshot_path"], mimetype="image/png")
    return "No screenshot", 404

# -----------------------------
# ファイル
# -----------------------------
@app.route("/send-file", methods=["POST"])
def send_file():
    file = request.files["file"]
    save_path = os.path.join(DATA_DIR, file.filename)
    file.save(save_path)
    shared["file_path"] = save_path
    return jsonify({"status": "ok"})

@app.route("/receive-file", methods=["GET"])
def receive_file():
    if shared["file_path"] and os.path.exists(shared["file_path"]):
        return send_file(shared["file_path"], as_attachment=True)
    return "No file", 404

# -----------------------------
# サーバー停止
# -----------------------------
@app.route("/stop", methods=["POST"])
def stop_server():
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if shutdown:
        shutdown()
    return jsonify({"status": "server stopped"})

# -----------------------------
# 起動
# -----------------------------
def start_server():
    app.run(host="0.0.0.0", port=5000, debug=False)

if __name__ == "__main__":
    start_server()
