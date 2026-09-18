import tkinter as tk
from tkinter import filedialog
import threading
import os

# ダイアログ結果を受け取るための変数
_dialog_result = None

def _open_dialog_select():
    global _dialog_result
    root = tk.Tk()
    root.withdraw()

    path = filedialog.askopenfilename(
        filetypes=[
            ("All Files", "*.*"),
            ("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.heic")
        ]
    )
    _dialog_result = path
    root.destroy()

def select_file():
    global _dialog_result
    _dialog_result = None

    t = threading.Thread(target=_open_dialog_select)
    t.start()
    t.join()

    return _dialog_result


# -----------------------------
# 保存ダイアログ（拡張子に応じて動的に filetypes を変更）
# -----------------------------
def _open_dialog_save(default_name):
    global _dialog_result
    root = tk.Tk()
    root.withdraw()

    ext = os.path.splitext(default_name)[1].lower()

    if ext == ".pdf":
        filetypes = [("PDF Document", "*.pdf"), ("All Files", "*.*")]
    elif ext == ".xlsx":
        filetypes = [("Excel Workbook", "*.xlsx"), ("All Files", "*.*")]
    elif ext == ".docx":
        filetypes = [("Word Document", "*.docx"), ("All Files", "*.*")]
    elif ext == ".zip":
        filetypes = [("ZIP Archive", "*.zip"), ("All Files", "*.*")]
    elif ext == ".png":
        filetypes = [("PNG Image", "*.png"), ("All Files", "*.*")]
    elif ext in [".jpg", ".jpeg"]:
        filetypes = [("JPEG Image", "*.jpg;*.jpeg"), ("All Files", "*.*")]
    else:
        filetypes = [("All Files", "*.*")]

    path = filedialog.asksaveasfilename(
        initialfile=default_name,
        filetypes=filetypes
    )
    _dialog_result = path
    root.destroy()

def save_file_dialog(default_name):
    global _dialog_result
    _dialog_result = None

    t = threading.Thread(target=_open_dialog_save, args=(default_name,))
    t.start()
    t.join()

    return _dialog_result
