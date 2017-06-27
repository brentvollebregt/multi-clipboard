import clipboard_assist
import logging
import sys
import os
from PIL import Image

clipboards_location = os.getcwd() + "/clipboards/"
data = clipboard_assist.getData()

if data['logging']:
    logging_level = logging.DEBUG
else:
    logging_level = logging.ERROR
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s',
    filename='log.log',
    level=logging_level,
)

if sys.argv[1] == "switch":
    if len(sys.argv) == 3:
        clipboard = clipboard_assist.cleanString(sys.argv[2])
        clipboard_assist.saveClipboard(clipboards_location, data)
        clipboard_assist.loadClipboard(clipboards_location, clipboard)
        data["current_clipboard"] = clipboard
        clipboard_assist.setData(data)
    else:
        print ("Usage: python clipboards.py switch clipboard")

elif sys.argv[1] == "clear":
    if len(sys.argv) == 2:
        for clipboard in os.listdir(clipboards_location):
            clipboard_assist.clear(clipboards_location, clipboard)
    elif len(sys.argv) == 3:
        clipboard = clipboard_assist.cleanString(sys.argv[2])
        if not clipboard_assist.clear(clipboards_location, clipboard):
            print ("Clipboard " + clipboard + " does not exist")
    else:
        print ("Usage: python clipboards.py clear [clipboard]")

elif sys.argv[1] == "view":
    if len(sys.argv) == 2:
        clipboard_assist.view()
    elif len(sys.argv) == 3:
        if not clipboard_assist.view_single(clipboards_location, sys.argv[2]):
            print ("Clipboard " + clipboard + " does not exist")
    else:
        print ("Usage: python clipboards.py view [clipboard]")

else:
    print ("Usage: python clipboards.py {switch, clear, view}")
