import pyperclip

def get_text():
    return pyperclip.paste()

def set_text(text):
    pyperclip.copy(text)
