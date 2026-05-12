# config.py

# Put starting variables here that might need to be changed by the user.

# Assign this CPX a unique integer identifier (1 - 9) for its type in your system.
CPX_NUMBER = 0

# Enable the onboard speaker 
# probably True for initial testing, False once you're connected to a real speaker.
SPEAKER_ENABLE = True

# Give each Circuit Playground a unique name so you don't get confused!
USB_NAME = "PLAYER" + str(CPX_NUMBER)

BANKS = ("kick", "snare", "perc")
SAMPLE_COUNT = 10

# Bank which will be enabled when the CPX is booted (by index number)
STARTING_BANK_INDEX = 0

_BANK_COLORS = ((0, 0, 16), (16, 0, 0), (0, 16, 0))
_SELECTION_COLOR = (16, 16, 16)

# Listen for MIDI messages on:
# this is the "raw" 0-15 scale
# channel for note messages
note_channel_in = 0
# channel for cc messages 
cc_channel_in = 2


# MIDI repeat count
# this is the number of times we check and process the MIDI queue 
# for every time we check and update the board buttons, neopixels, etc.
# raise this value if you are getting audible rhythm lag
# which will in turn increase button and neopixel lag
MIDI_READ_REPEAT = 256

# This is the note values each sequencer will listen for.
note_number = 36

# CC values
# Leave this empty if you don't want/need CC control
# CC_VALUES = {}
CC_VALUES = {16 : 'sample_index',
             20 : 'bank_index'}


# MPK knob notes...
# start at lowest value, go up to highest 7F by default.
# so we can just add this to the current number?
# we do need to store it in the model.

