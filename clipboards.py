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
            if os.path.isfile(clipboards_location + clipboard + ".bmp"):
                os.remove(clipboards_location + clipboard + ".bmp")
            elif os.path.isfile(clipboards_location + clipboard + ".txt"):
                os.remove(clipboards_location + clipboard + ".txt")
    elif len(sys.argv) == 3:
        clipboard = clipboard_assist.cleanString(sys.argv[2])
        if os.path.isfile(clipboards_location + clipboard + ".bmp"):
            os.remove(clipboards_location + clipboard + ".bmp")
        elif os.path.isfile(clipboards_location + clipboard + ".txt"):
            os.remove(clipboards_location + clipboard + ".txt")
        else:
            print ("Clipboard " + sys.argv[2] + " does not exist")
    else:
        print ("Usage: python clipboards.py clear [clipboard]")

elif sys.argv[1] == "view":
    if len(sys.argv) == 2:
        clipboard_assist.view()
    elif len(sys.argv) == 3:
        if os.path.isfile(clipboards_location + sys.argv[2] + ".bmp"):
            image = Image.open(clipboards_location + sys.argv[2] + ".bmp")
            image.show()
            print ("Image displayed")
        elif os.path.isfile(clipboards_location + sys.argv[2] + ".txt"):
            print ("Clipboard text:")
            f = open(clipboards_location + sys.argv[2] + ".txt", 'r')
            print (f.read())
            f.close()
        else:
            print ("Clipboard " + sys.argv[2] + " does not exist")
    else:
        print ("Usage: python clipboards.py view [clipboard]")

else:
    print ("Usage: python clipboards.py {switch, clear, view}")
