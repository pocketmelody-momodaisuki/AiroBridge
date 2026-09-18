import pystray
from pystray import MenuItem
from PIL import Image
import requests
import os
import cgi
from urllib.parse import unquote
import mimetypes

import utils.clipboard as clipboard
import utils.screenshot as screenshot
import utils.file_dialog as file_dialog
import utils.qrcode_window as qrcode_window

SERVER = lambda: "http://127.0.0.1:5000"

def create_icon():
    icon_path = os.path.join("assets", "tray_icon.ico")
    if os.path.exists(icon_path):
        return Image.open(icon_path)
    return Image.new("RGB", (16, 16), (0, 120, 255))

# --- 各種共有機能 ---
def send_text(icon, item):
    text = clipboard.get_text()
    if text:
        requests.post(f"{SERVER()}/send-text", json={"text": text})

def receive_text(icon, item):
    r = requests.get(f"{SERVER()}/receive-text")
    clipboard.set_text(r.json().get("text", ""))

def send_screenshot(icon, item):
    img_path = screenshot.capture()
    with open(img_path, "rb") as f:
        requests.post(f"{SERVER()}/send-file", files={"file": ("screenshot.png", f, "image/png")})

def send_file(icon, item):
    path = file_dialog.select_file()
    if not path:
        return
    filename = os.path.basename(path)
    mime, _ = mimetypes.guess_type(filename)
    if mime is None:
        mime = "application/octet-stream"
    with open(path, "rb") as f:
        requests.post(f"{SERVER()}/send-file", files={"file": (filename, f, mime)})

def receive_file(icon, item):
    r = requests.get(f"{SERVER()}/receive-file", stream=True)
    cd = r.headers.get("Content-Disposition", "")
    _, params = cgi.parse_header(cd)
    filename = unquote(params.get("filename", "received_file"))
    save_path = file_dialog.save_file_dialog(filename)
    if save_path:
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

def show_qrcode(icon, item):
    qrcode_window.show_qr(SERVER())

# --- 終了処理 ---
def quit_app(icon, item):
    # サーバー停止
    try:
        requests.post(f"{SERVER()}/stop")
    except:
        pass

    # トレイアイコン非表示
    icon.visible = False

    # pystray を停止
    icon.stop()

def start_tray():
    icon = pystray.Icon(
        "AiroBridge",
        create_icon(),
        menu=pystray.Menu(
            MenuItem("QRコード表示", show_qrcode),
            MenuItem("テキスト共有", pystray.Menu(
                MenuItem("送信", send_text),
                MenuItem("受信", receive_text)
            )),
            MenuItem("スクショ共有", pystray.Menu(
                MenuItem("送信", send_screenshot)
            )),
            MenuItem("ファイル共有", pystray.Menu(
                MenuItem("送信", send_file),
                MenuItem("受信", receive_file)
            )),
            MenuItem("サーバー停止", lambda icon, item: requests.post(f"{SERVER()}/stop")),
            MenuItem("終了", quit_app)
        )
    )
    icon.run()
