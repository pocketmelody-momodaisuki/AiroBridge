from tkinter import Tk, filedialog

def select_file():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename()

def save_file_dialog(default_name="received"):
    root = Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(initialfile=default_name)
