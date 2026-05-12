# sets the name of the Circuit Playground as it appears to a PC
# from https://github.com/todbot/circuitpython-tricks#usb

# customize name here:
# Because of the limitations of the old school Microsoft format
# this MUST BE 8 CHARACTERS OR LESS
# and ALL CAPS are recommended.  
import config
import storage

storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = config.USB_NAME
storage.remount("/", readonly=True)
