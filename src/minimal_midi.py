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

_NOTE_ON_NYBBLE: int = const(0b1001) << 4
_NOTE_OFF_NYBBLE: int = const(0b1000) << 4
_CC_NYBBLE: int = const(0b1011) << 4
_FOUR_BIT_MASK: int = const(0b1111)

# These "ports" are not to be confused with MIDI channels, etc.
_INNIE = usb_midi.ports[0]

def generate_status_byte(ch: int, nybble: int) -> int:
    return ch | nybble

class MinimalMidi(object):
    """Tightly implementing the subset of MIDI we need."""
    
    def __init__(self, note_in_channel: int, cc_in_channel: int):
        self.note_in_channel: int = note_in_channel & _FOUR_BIT_MASK
        self.note_on_value: int = generate_status_byte(self.note_in_channel, _NOTE_ON_NYBBLE)
        self.note_off_value: int = generate_status_byte(self.note_in_channel, _NOTE_OFF_NYBBLE)
        self.cc_value: int = generate_status_byte(cc_in_channel, _CC_NYBBLE)
        self.has_cc: bool = bool(config.CC_VALUES)
        
        # Micro-cache a local pointer to the hardware readinto routine
        self._readinto = _INNIE.readinto
        
        # Pre-allocate static mutable 1-byte input buffer to eliminate heap allocations on reads
        self._in_buf: bytearray = bytearray(1)
        
        # Pre-allocate a static list container to pass parsed data back allocation-free
        # Layout: [status_byte, parameter_1 (note/function), parameter_2 (velocity/value)]
        self.parsed_event: list = [0, 0, 0]

    def clear_msgs(self) -> None:
        # Flush the UART buffer allocation-free using our static buffer slot
        while self._readinto(self._in_buf, 1):
            pass

    def process_cc(self) -> list:
        # Read the next two bytes directly into our pre-allocated array slot without ord()
        if not self._readinto(self._in_buf, 1):
            return None
        f: int = self._in_buf[0]
        
        if not self._readinto(self._in_buf, 1):
            return None
        v: int = self._in_buf[0]
        
        self.parsed_event[0] = self.cc_value
        self.parsed_event[1] = f
        self.parsed_event[2] = v
        return self.parsed_event

    def process_note(self, status_token: int) -> list:
        if not self._readinto(self._in_buf, 1):
            return None
        n: int = self._in_buf[0]
        
        if not self._readinto(self._in_buf, 1):
            return None
        v: int = self._in_buf[0]
        
        self.parsed_event[0] = status_token
        self.parsed_event[1] = n
        self.parsed_event[2] = v
        return self.parsed_event

    def get_msg(self) -> list:
        # Use readinto to drop an incoming byte directly into our pre-allocated memory slot
        if not self._readinto(self._in_buf, 1):
            return None
            
        n: int = self._in_buf[0] # Fetch the integer byte directly from the buffer
        
        if self.has_cc: # slight optimization
            if n == self.cc_value:
                return self.process_cc()
                
        if n == self.note_on_value:
            return self.process_note(self.note_on_value)
        elif n == self.note_off_value:
            return self.process_note(self.note_off_value)
        else:
            return None

    def increment_channel(self) -> None:
        '''Add one to the note channel.'''
        # AND below is equivalent to MOD 16.
        self.note_in_channel = (self.note_in_channel + 1) & _FOUR_BIT_MASK
        self.note_on_value = generate_status_byte(self.note_in_channel, _NOTE_ON_NYBBLE)
        self.note_off_value = generate_status_byte(self.note_in_channel, _NOTE_OFF_NYBBLE)
