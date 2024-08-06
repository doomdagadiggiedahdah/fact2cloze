import pyperclip
import time
import pyautogui as pya


def copy_text():
    time.sleep(.2)
    pya.hotkey('ctrl', 'c')
    return pyperclip.paste().replace("\n", " ")

def grab_link():
    pya.hotkey('ctrl', 'l')
    pya.hotkey('ctrl', 'c')
    pya.hotkey('F6')
    return pyperclip.paste().strip()


og_article_text = copy_text()
URL = grab_link()

# Don't shoot me, because kivy launches teh app when you import the module
# I want the text grab to happen before the app launches. Therefore, we have
# This Masterpiece


