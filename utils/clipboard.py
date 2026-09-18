# utils/clipboard.py
import win32clipboard
import win32con
import time

def get_text():
    for _ in range(5):
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return data
        except:
            time.sleep(0.05)
    return ""

def set_text(text):
    for _ in range(5):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
            return
        except:
            time.sleep(0.05)
