# server.py
from flask import Flask, request, jsonify, send_file
import os
import threading

app = Flask(__name__)

# 共有データ（PC ⇄ iPhone）
shared = {
    "text": "",
    "url": "",
    "screenshot_path": None,
    "file_path": None
}

# 保存フォルダ
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
# URL（テキスト扱い）
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
# サーバー起動関数
# -----------------------------
def start_server():
    app.run(host="0.0.0.0", port=5000, debug=False)

if __name__ == "__main__":
    start_server()
