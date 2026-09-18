from flask import Flask, request, jsonify, send_file
import os
import socket
import mimetypes
from PIL import Image
import io
from pillow_heif import register_heif_opener

register_heif_opener()

app = Flask(__name__, static_folder="web", static_url_path="")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

shared = {
    "text": "",
    "file_path": None
}

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/server-info")
def server_info():
    return jsonify({"ip": get_ip(), "port": 5000})

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
# ファイル（画像含む）
# -----------------------------
@app.route("/send-file", methods=["POST"])
def send_file_api():
    file = request.files["file"]

    # ログ
    print("----- 受信したファイル情報 -----")
    print("filename:", file.filename)
    print("mimetype:", file.mimetype)
    print("content_type:", file.content_type)
    print("headers:", file.headers)
    print("------------------------------")

    # ★ 日本語ファイル名を安全に処理する
    original_filename = file.filename
    safe_filename = os.path.basename(original_filename)  # パス除去
    safe_filename_lower = safe_filename.lower()

    # HEIC → JPEG
    if safe_filename_lower.endswith(".heic"):
        heif_data = file.read()
        img = Image.open(io.BytesIO(heif_data))
        save_path = os.path.join(DATA_DIR, "received_image.jpg")
        img.save(save_path, "JPEG")
        shared["file_path"] = save_path
        return jsonify({"status": "ok"})

    # PNG / JPG / JPEG → そのまま保存
    if safe_filename_lower.endswith((".png", ".jpg", ".jpeg")):
        save_path = os.path.join(DATA_DIR, safe_filename)
        file.save(save_path)
        shared["file_path"] = save_path
        return jsonify({"status": "ok"})

    # その他 → そのまま保存
    save_path = os.path.join(DATA_DIR, safe_filename)
    file.save(save_path)
    shared["file_path"] = save_path
    return jsonify({"status": "ok"})

@app.route("/receive-file")
def receive_file():
    file_path = shared.get("file_path")
    if not file_path or not os.path.exists(file_path):
        return "No file", 404

    filename = os.path.basename(file_path)
    mime, _ = mimetypes.guess_type(filename)
    if mime is None:
        mime = "application/octet-stream"

    return send_file(
        file_path,
        mimetype=mime,
        as_attachment=True,
        download_name=filename
    )


# -----------------------------
# サーバー停止
# -----------------------------
@app.route("/stop", methods=["POST"])
def stop_server():
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if shutdown:
        shutdown()
    return jsonify({"status": "server stopped"})

def start_server():
    app.run(host="0.0.0.0", port=5000, debug=False)

if __name__ == "__main__":
    start_server()
