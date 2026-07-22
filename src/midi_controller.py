# midi_controller.py
# Processing incoming MIDI messages.
# Inputs -> NoteOn.

import gc
import cpx
import config

class MidiController(object):
    """
    Handles incoming MIDI note messages.
    This MidiController does not need state.
    """
    def __init__(self, model, midi, led=cpx.led, audio=cpx.audio):
        self.model = model
        self.midi = midi
        self.led = led
        self.audio = audio

    def main(self) -> "MidiController":
        '''
        Main MIDI loop, calling get_msg() and calling relevant methods.
        '''
        # Optimization: Local reference caching for the tight high-frequency read loop
        get_msg = self.midi.get_msg
        
        for _ in config.ACTIVE_REPEATS:
            msg = get_msg() # get_msg() handles filtering by channel and message type
            
            if msg is not None:
                status: int = msg[0]
                
                # ordered by timing priority
                if status == self.midi.note_on_value:
                    if msg[1] == self.model.note:
                        self.audio.play(self.model.wav)
                        cpx.toggle_led()
                        
                elif status == self.midi.note_off_value:
                    if msg[1] == self.model.note:
                        self.audio.stop()
                        cpx.toggle_led()
                        
        # Proactive Memory Management: Explicitly clean memory right after the high-speed 
        # buffer read block finishes, absorbing any sweep cost outside the active play window.
        gc.collect()
        return self
