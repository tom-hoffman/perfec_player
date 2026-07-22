# boot.py
# This module runs first on boot (before `code.py`).
# Sets the name of the Circuit Playground as it appears to a PC
# Based on guidelines from: https://github.com/todbot/circuitpython-tricks#usb

# Spams all the other USB MIDI related names to try to ensure 
# your DAW and OS will be able to differentiate between different modules.

# Because of the limitations of the old school Microsoft format,
# the base volume label name MUST BE 8 CHARACTERS OR LESS
# and ALL CAPS are recommended.

import config
import storage
import usb_midi
import supervisor

storage.remount("/", readonly=False)
m = storage.getmount("/")
n: str = config.USB_NAME
m.label = n

# Kept the suffix extensions short to prevent buffer overflows 
# when students assign multi-digit identifiers in the lab.
usb_midi.set_names(
    streaming_interface_name=n + "-S",
    audio_control_interface_name=n + "-A",
    in_jack_name=n + "-I",
    out_jack_name=n + "-O"
)

supervisor.set_usb_identification(
    manufacturer="PERFEC " + n, 
    product=n
)

storage.remount("/", readonly=True)
