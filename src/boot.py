# This module runs first on boot (before `code.py`).
# sets the name of the Circuit Playground as it appears to a PC
# from https://github.com/todbot/circuitpython-tricks#usb

# Also essentially spamming all the other USB MIDI related names
# to try to ensure your DAW and OS will be able to differentiate
# between different modules.

# Because of the limitations of the old school Microsoft format
# this MUST BE 8 CHARACTERS OR LESS
# and ALL CAPS are recommended.

import config
import storage
import usb_midi
import supervisor

storage.remount("/", readonly=False)
m = storage.getmount("/")
n = config.USB_NAME
m.label = n
usb_midi.set_names(streaming_interface_name = n + "-STR",
				   audio_control_interface_name =n  + "-AUD",
				   in_jack_name = n + "-IN",
				   out_jack_name = n + "-OUT")
supervisor.set_usb_identification(manufacturer="PERFEC", 
                                  product=n)
storage.remount("/", readonly=True)
