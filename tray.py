# tray.py
import pystray
from pystray import MenuItem as Item
from PIL import Image
import qrcode
import tempfile
import os
import socket
import requests

import utils.clipboard as clipboard
import utils.screenshot as screenshot
import utils.file_dialog as file_dialog

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
# QRコード表示
# -----------------------------
def show_qr(icon, item):
    ip = get_ip()
    url = f"http://{ip}:5000"

    img = qrcode.make(url)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(tmp.name)

    os.startfile(tmp.name)

# -----------------------------
# サーバーURL
# -----------------------------
SERVER = lambda: f"http://{get_ip()}:5000"

# -----------------------------
# 送信系
# -----------------------------
def send_text(icon, item):
    text = clipboard.get_text()
    if not text:
        print("クリップボードが空です")
        return
    requests.post(f"{SERVER()}/send-text", json={"text": text})
    print("テキスト送信完了")

def send_url(icon, item):
    url = clipboard.get_text()
    requests.post(f"{SERVER()}/send-url", json={"url": url})
    print("URL送信完了")

def send_screenshot(icon, item):
    img_path = screenshot.capture()
    with open(img_path, "rb") as f:
        requests.post(f"{SERVER()}/send-screenshot", files={"file": f})
    print("スクショ送信完了")

def send_file(icon, item):
    path = file_dialog.select_file()
    if not path:
        return
    with open(path, "rb") as f:
        requests.post(f"{SERVER()}/send-file", files={"file": f})
    print("ファイル送信完了")

# -----------------------------
# 受信系
# -----------------------------
def receive_text(icon, item):
    r = requests.get(f"{SERVER()}/receive-text")
    text = r.json().get("text", "")
    print(f"[受信テキスト] {text}")
    clipboard.set_text(text)
    print("テキスト受信 → クリップボードへ保存")

def receive_url(icon, item):
    r = requests.get(f"{SERVER()}/receive-url")
    url = r.json().get("url", "")
    clipboard.set_text(url)
    print("URL受信 → クリップボードへ保存")

def receive_screenshot(icon, item):
    save_path = file_dialog.save_file_dialog("screenshot.png")
    if not save_path:
        return
    r = requests.get(f"{SERVER()}/receive-screenshot")
    with open(save_path, "wb") as f:
        f.write(r.content)
    print("スクショ受信 → 保存完了")

def receive_file(icon, item):
    save_path = file_dialog.save_file_dialog("received_file")
    if not save_path:
        return
    r = requests.get(f"{SERVER()}/receive-file")
    with open(save_path, "wb") as f:
        f.write(r.content)
    print("ファイル受信 → 保存完了")

# -----------------------------
# サーバー制御
# -----------------------------
def stop_server(icon, item):
    requests.post(f"{SERVER()}/stop")
    print("サーバー停止")

def quit_app(icon, item):
    try:
        requests.post(f"{SERVER()}/stop")
        print("サーバー停止要求を送信しました")
    except Exception as e:
        print(f"サーバー停止要求に失敗: {e}")

    icon.stop()
    print("AiroBridge を終了します")

# -----------------------------
# メニュー
# -----------------------------
def create_menu():
    return pystray.Menu(
        Item("QRコード表示", show_qr),
        Item("テキスト", pystray.Menu(
            Item("送信", send_text),
            Item("受信", receive_text)
        )),
        Item("URL", pystray.Menu(
            Item("送信", send_url),
            Item("受信", receive_url)
        )),
        Item("スクショ", pystray.Menu(
            Item("送信", send_screenshot),
            Item("受信", receive_screenshot)
        )),
        Item("ファイル", pystray.Menu(
            Item("送信", send_file),
            Item("受信", receive_file)
        )),
        Item("サーバー停止", stop_server),
        Item("終了", quit_app)
    )

# -----------------------------
# トレイ起動
# -----------------------------
def start_tray():
    icon_image = Image.open("assets/tray_icon.ico")
    icon = pystray.Icon("AiroBridge", icon_image, "AiroBridge", create_menu())
    icon.run()
