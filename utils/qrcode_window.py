import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import qrcode
import os
import threading

ICON_PATH = os.path.join("assets", "tray_icon.ico")

def _qr_window_thread(server_url):
    # Tk をこのスレッド専用で起動
    root = tk.Tk()

    # ★ タイトルバーを消す（ウィンドウ枠なし）
    root.overrideredirect(True)

    # ウィンドウサイズ
    root.geometry("360x500")

    # アイコン設定（枠なしでも内部的には設定可能）
    if os.path.exists(ICON_PATH):
        try:
            root.iconbitmap(ICON_PATH)
        except:
            pass

    # QRコード生成
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(server_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_img = ImageTk.PhotoImage(img)

    # 画像参照保持（絶対に消えない）
    root.qr_img = qr_img

    # QRコード表示
    qr_label = ttk.Label(root, image=qr_img)
    qr_label.pack(pady=20)

    # 説明文
    text = (
        "お手持ちのスマートデバイスで\n"
        "QRコードを読み取ってください。\n\n"
        "表示されたURLへアクセスすると、\n"
        "AiroBridge に接続できます。\n"
        "(同一ローカルネットワーク内のみ)"
    )
    msg_label = ttk.Label(root, text=text, justify="center", font=("Meiryo", 11))
    msg_label.pack(pady=10)

    # 閉じるボタン（枠がないのでこれが唯一の閉じ方）
    close_btn = ttk.Button(root, text="閉じる", command=root.destroy)
    close_btn.pack(pady=10)

    # ★ このスレッド内で mainloop を回す（安定）
    root.mainloop()


def show_qr(server_url):
    # ★ Tk を別スレッドで起動する
    t = threading.Thread(target=_qr_window_thread, args=(server_url,), daemon=True)
    t.start()
