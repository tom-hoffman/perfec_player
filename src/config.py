# PERFEC System Sample Player
# config.py
# copyright 2026, Tom Hoffman
# MIT License
# Variables and settings that might need to be changed by the user.

from micropython import const

# Enable the tiny speaker built into the Circuit Playground Express.
# Probably True for initial testing, False once you're connected to a real speaker.
SPEAKER_ENABLE: bool = True

# Assign this CPX a one digit identifier different than other modules
# of the same type.
CPX_NUMBER: int = 0
# By default, the device name will be PLAYER + the CPX_NUMBER.
USB_NAME: str = "PLAYER" + str(CPX_NUMBER)


# STARTING VALUES

# Input channels for incoming MIDI messages.
# This is the "raw" 0-15 scale used in code, rather than 1-16 as is often displayed.
# "Raw" channel 9 corresponds to Channel 10 on commercial synthesizers.
note_channel_in: int = 9

# Starting Indexed Values
# These are all settings which are based on selecting one
# value out of a list. 

# DEFAULT_NOTE_INDEX (range 0 - 5)
# The pitch index this sampler listens for to trigger audio.
# Change on CPX by pressing A in config mode while clock is stopped.
# Represented by cyan neopixels.
DEFAULT_NOTE_INDEX: int = CPX_NUMBER

# STARTING_BANK_INDEX (range 0 - 2)
# The starting folder directory ("bank") loaded at boot time.
# Change on CPX by pressing A in live mode.
# Displays a background a distinct color (blue, red, or green).
STARTING_BANK_INDEX: int = 0

# DEFAULT_SAMPLE_INDEX (range 0 - 9)
# The starting individual sample slot number activated at boot.
# Change on CPX by pressing B in live mode.
# Highlighted on the ring by a single white cursor.
DEFAULT_SAMPLE_INDEX: int = 0


# Value lists
# Generally you won't need to change these, 
# unless you want a special distribution, EXCEPT:

# Setting Available Notes
# This list maps the 6 index choices to standard MIDI pitches.
# Incoming NoteOn messages matching your choice will strike the sampler.
NOTE_TUPLE: tuple = const((36, 40, 43, 41, 46, 42))

# Names of directories ("banks") containing sample files.
BANKS: tuple = const(("blue", "red", "green"))

# Neopixel RGB colors associated with each corresponding folder bank.
BANK_COLORS: tuple = const(((0, 0, 16), (16, 0, 0), (0, 16, 0)))

# Color of the single neopixel cursor tracking the active sample slot choice.
SELECTION_COLOR = const((16, 16, 16))

# Total number of sample sub-directories mapped inside each audio bank.
SAMPLE_COUNT: int = 10


# MIDI repeat count
# this is the number of times we check and process the MIDI queue
# for every time we check and update the board buttons, neopixels, etc.
# raising this value reduces audible rhythm lag
# reducing this value decreases button and neopixel lag
MIDI_READ_REPEAT: int = 256

# Pre-allocated range loop based on the configuration setting 
# to optimize execution speed without allocating RAM at runtime
# Do not change this.
ACTIVE_REPEATS = range(MIDI_READ_REPEAT)
