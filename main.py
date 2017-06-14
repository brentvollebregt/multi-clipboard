# TODO Not swapping currently

import sys
import os
import shutil
import json
import win32clipboard
from PIL import ImageGrab, Image # pip install Pillow
from io import BytesIO

if len(sys.argv) < 2:
    print ("Usage: python main.py <clipboard_number>|clear")
    exit()

clipboard = sys.argv[1]
clipboards_location = os.getcwd() + "/clipboards/"

with open('data.json') as data_file:
    data = json.load(data_file)

try:
    int(clipboard)
except:
    if clipboard == "clear":
        if os.path.exists(clipboards_location):
            shutil.rmtree(clipboards_location)
            print ("Clipboards cleared")

            data["current_clipboard"] = 1
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)

            exit()

current_clipboard = data["current_clipboard"]

# Check if clipboards have a save location
if not os.path.exists(clipboards_location):
    os.makedirs(clipboards_location)

# Save Current
try:
    win32clipboard.OpenClipboard()
    currentClipBoard = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    f = open(clipboards_location + str(current_clipboard) + ".txt", 'w')
    f.write(currentClipBoard)
    f.close()

    if os.path.isfile(clipboards_location + str(current_clipboard) + ".bmp"):
        os.remove(clipboards_location + str(current_clipboard) + ".bmp")
except TypeError:
    try:
        im = ImageGrab.grabclipboard()
        im.save(clipboards_location + str(current_clipboard) + ".bmp", 'BMP')

        if os.path.isfile(clipboards_location + str(current_clipboard) + ".txt"):
            os.remove(clipboards_location + str(current_clipboard) + ".txt")
    except:
        print ("Clipbaord contents not supported")
        exit()
except Exception as e:
    print ("Unexpected error")
    print (e)
    exit()

# Load New
if os.path.isfile(clipboards_location + str(clipboard) + ".bmp"):
    image = Image.open(clipboards_location + str(clipboard) + ".bmp")
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    clipboard_data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, clipboard_data)
    win32clipboard.CloseClipboard()
    pass
elif os.path.isfile(clipboards_location + str(clipboard) + ".txt"):
    f = open(clipboards_location + str(clipboard) + ".txt")
    clipboard_data = f.read()
    f.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(clipboard_data)
    win32clipboard.CloseClipboard()

# Write new clipboard location
data["current_clipboard"] = clipboard
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
