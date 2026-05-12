# minimal_midi.py
# Please note that this file is not a complete library but a
# template for a customized MIDI handling module. 
# CircuitPython on a CPX is both memory constrained and slow
# for real time MIDI processing on a busy MIDI network.  
# Customize the main loop in particular to process needed 
# messages as quickly as possible.

# Note that MinimalMidi uses 0-15 numbering for MIDI channels.
# Your MIDI device may display channels as 1-15, 
# thus you may need to subtract 1 from the displayed value
# to match the value here.

# MIDI inputs -> NoteOn, optional CC.
# MIDI outputs -> none.

import usb_midi

from micropython import const

import config

_NOTE_ON_NYBBLE = const(0b1001) << 4
_NOTE_OFF_NYBBLE = const(0b1000) << 4
_CC_NYBBLE = const(0b1011) << 4

_FOUR_BIT_MASK = const(0b1111)

# These "ports" are not to be confused with MIDI channels, etc.
_INNIE = usb_midi.ports[0]

def generate_status_byte(ch: int, nybble: int):
    return ch | nybble

class MinimalMidi(object):
    """Tightly implementing the subset of MIDI we need."""
    def __init__(self, note_in_channel, cc_in_channel):
        self.note_in_channel = note_in_channel & _FOUR_BIT_MASK
        self.note_on_value = generate_status_byte(note_in_channel, _NOTE_ON_NYBBLE)
        self.note_off_value = generate_status_byte(note_in_channel, _NOTE_OFF_NYBBLE)
        self.cc_value = generate_status_byte(cc_in_channel, _CC_NYBBLE)
        self.has_cc = bool(config.CC_VALUES)

    def clear_msgs(self):
        m = _INNIE.read(1)
        while m:
            m = _INNIE.read(1)

    def process_cc(self):
        f = ord(_INNIE.read(1))
        v = ord(_INNIE.read(1))
        return {'type' : 'CC', 'function' : f, 'value' : v}

    def process_note(self, m: str) -> dict:
        print("Hitting midi library.")
        n = ord(_INNIE.read(1))
        v = ord(_INNIE.read(1))
        return {'type' : m, 'note' : n, 'velocity' : v}
    
    def get_msg(self):
        m = _INNIE.read(1)              # grab a byte
        if m == b'':                    # drop empty bytes
            return None
        else:
            n = ord(m)                  # convert to an integer
        if self.has_cc:                 # slight optimization
            if n == self.cc_value:
                return self.process_cc()
        if n == self.note_on_value:
            return self.process_note('NoteOn')
        elif n == self.note_off_value:
            return self.process_note('NoteOff')
        else:
            return None
        
    '''
    # don't need yet...?
    # also update for different cc channel
    def switch_channel(self, ch: int):
        self.in_channel = ch & _FOUR_BIT_MASK
        self.note_on_value = generate_status_byte(ch, _NOTE_ON_NYBBLE)
        self.note_off_value = generate_status_byte(ch, _NOTE_OFF_NYBBLE)
        self.cc_value = generate_status_byte(ch, _CC_NYBBLE)       
    '''


    





    


    

