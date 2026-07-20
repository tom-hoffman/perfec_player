# midi_controller.py
# Processing incoming MIDI messages.
# Inputs -> NoteOn, optional CC.

import gc
import cpx
import config

class MidiController(object):
    """
    Handles incoming MIDI note and CC messages.
    This MidiController does not need state.
    """
    def __init__(self, model, midi, led=cpx.led, audio=cpx.audio):
        self.model = model
        self.midi = midi
        self.led = led
        self.audio = audio

    def toggle_led(self) -> None:
        self.led.value = not(self.led.value)

    def process_cc(self, msg_list: list) -> None:
        # Index 1 is the integer value of the MIDI CC function byte.
        fun: int = msg_list[1]
        
        # if fun is in the dictionary of relevant CC values defined in config.py.
        # ignore any CC function values not in cc_keys.
        if fun in self.model.cc_keys:
            # find the strings associated with the number value as defined in config.py.
            if config.CC_VALUES[fun] == 'sample_index':
                # update the cc count in the model to the sent value (Index 2)
                self.model.sample_cc_count = msg_list[2]
                self.model.update_sample_index()
            elif config.CC_VALUES[fun] == 'bank_index':
                self.model.bank_cc_count = msg_list[2]
                # calculate the new stored bank index value
                self.model.update_bank_index()

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
                        
                elif status == self.midi.cc_value:
                    self.process_cc(msg)
                    
                elif status == self.midi.note_off_value:
                    if msg[1] == self.model.note:
                        self.audio.stop()
                        cpx.toggle_led()
                        
        # Proactive Memory Management: Explicitly clean memory right after the high-speed 
        # buffer read block finishes, absorbing any sweep cost outside the active play window.
        gc.collect()
        return self
