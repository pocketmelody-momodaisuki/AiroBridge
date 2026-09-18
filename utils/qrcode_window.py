import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import qrcode
import os
import threading

ICON_PATH = os.path.join("assets", "tray_icon.ico")
LOGO_PATH = os.path.join("assets", "logo.png")

def _qr_window_thread(server_url):
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry("360x600")   # ← 高さを少し増やした
    root.configure(bg="white")

    # ロゴ読み込み
    logo_tk = None
    if os.path.exists(LOGO_PATH):
        logo_img = Image.open(LOGO_PATH)
        logo_img = logo_img.resize((50, 50))  # ← 横並びなので少し小さく
        logo_tk = ImageTk.PhotoImage(logo_img)
        root.logo_tk = logo_tk  # 参照保持

    # ロゴ＋アプリ名（横並び）
    title_frame = tk.Frame(root, bg="white")
    title_frame.pack(pady=(20, 10))

    if logo_tk:
        logo_label = tk.Label(title_frame, image=logo_tk, bg="white")
        logo_label.pack(side="left", padx=8)

    title_label = tk.Label(
        title_frame,
        text="AiroBridge",
        font=("Meiryo", 22, "bold"),
        bg="white"
    )
    title_label.pack(side="left")

    # QRコード生成
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(server_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_img = ImageTk.PhotoImage(img)
    root.qr_img = qr_img  # 参照保持

    qr_label = ttk.Label(root, image=qr_img)
    qr_label.pack(pady=10)

    # 説明文
    msg = (
        "お手持ちのスマートデバイスで\n"
        "QRコードを読み取ってください。\n\n"
        "表示されたURLへアクセスすると、\n"
        "AiroBridge に接続できます。\n"
        "(同一ローカルネットワーク内のみ)"
    )
    msg_label = tk.Label(root, text=msg, font=("Meiryo", 12), bg="white", justify="center")
    msg_label.pack(pady=10)

    # 閉じるボタン
    close_btn = ttk.Button(root, text="閉じる", command=root.destroy)
    close_btn.pack(pady=20)

    root.mainloop()


def show_qr(server_url):
    t = threading.Thread(target=_qr_window_thread, args=(server_url,), daemon=True)
    t.start()
