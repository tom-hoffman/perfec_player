# PERFEC System Sample Player
# config.py
# copyright 2026, Tom Hoffman
# MIT License

# Variables and settings that might need to be changed by the user.

from micropython import const

# Assign this CPX a one digit identifier different than other modules
# of the same type.

CPX_NUMBER: int = 0

# Give each Circuit Playground a unique name so you don't get confused!

USB_NAME: str = "PLAYER" + str(CPX_NUMBER)


# Input channels for MIDI messages
# This is the "raw" 0-15 scale used in code, rather than 1-16 as is often displayed.

# channel for note messages
note_channel_in: int = 0

# channel for cc messages
cc_channel_in: int = 2


# Setting Available Notes
#
# NOTE_NUMBERS is a tuple of MIDI note values.  The active value
# can be selected directly from the CPX
# using the buttons and neopixel interface.
# The default values match that of the PERFEC Euclidian Sequencer
# and are based on the General MIDI specification
# for percussion values:

'''
 * 36/C1: bass drum
 * 40/E1: electric snare
 * 43/G1: high tom-tom
 * 41/F1: low tom-tom
 * 46/Bb1: open hi-hat
 * 42/F#1: closed hi-hat
'''

# You may want to change these numbers to match whatever source
# of MIDI NoteOn messages you're working with.  You can trigger
# your samples by playing the corresponding notes as shown above
# on a keyboard.

NOTE_NUMBERS: tuple[int] = const((36, 40, 43, 41, 46, 42))

# DEFAULT_NOTE is the index of the note this sample player
# will respond to when receiving a MIDI NoteOn message.
# Adjust this to create a pleasant default setting for
# multiple sequencers and voices.

DEFAULT_NOTE: int = 0


# CC values
# Leave this empty if you don't want/need CC control
CC_VALUES = {}

# example
# CC_VALUES = {16 : 'sample_index',
#              20 : 'bank_index'}


# Enable the onboard speaker.
# Probably True for initial testing, False once you're connected to a real speaker.

SPEAKER_ENABLE: bool = True

# Names of directories ("banks") containing (directories containing) samples.

BANKS: tuple[str] = const(("blue", "red", "green"))


# Number of directories containing samples in each bank

SAMPLE_COUNT: int = 10


# Bank which will be enabled when the CPX is booted (by index number)

STARTING_BANK_INDEX: int = 0


# Neopixel RGB colors associate with each bank.
BANK_COLORS: tuple[tuple[int]] = const(((0, 0, 16), (16, 0, 0), (0, 16, 0)))

# Color of neopixel indicating the active sample.
SELECTION_COLOR = const((16, 16, 16))




# MIDI repeat count
# this is the number of times we check and process the MIDI queue
# for every time we check and update the board buttons, neopixels, etc.
# raising this value reduces audible rhythm lag
# reducing this value decreases button and neopixel lag

MIDI_READ_REPEAT = 256


# MPK knob notes...
# start at lowest value, go up to highest 7F by default.
# so we can just add this to the current number?
# we do need to store it in the model.

