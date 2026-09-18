from PIL import ImageGrab
import os

def capture():
    path = "screenshot.png"
    img = ImageGrab.grab()
    img.save(path)
    return path
