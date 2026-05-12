# midi_controller.py
# Processing incoming MIDI messages.

# Inputs -> NoteOn, optional CC.

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

    def toggle_led(self):
        self.led.value = not(self.led.value)

    def process_cc(self, msg):
        # fun is the integer value of the MIDI CC function byte.
        fun = msg['function']
        # if fun is in the dictionary of relevant CC values defined in config.py.
        # ignore any CC function values not in cc_keys.
        if fun in self.model.cc_keys:
            # find the strings associated with the number value as defined in config.py.
            if config.CC_VALUES[fun] == 'sample_index':
                # update the cc count in the model to the sent value
                self.model.sample_cc_count = msg['value']
                self.model.update_sample_index()
            elif config.CC_VALUES[fun] == 'bank_index':
                self.model.bank_cc_count = msg['value']
                # calculate the new stored bank index value
                self.model.update_bank_index()

    def main(self):
        '''
        Main MIDI loop, calling get_msg() and calling relevant methods.
        '''
        for i in range(config.MIDI_READ_REPEAT):
            msg = self.midi.get_msg()
            # get_msg() handles filtering by channel and message type
            if msg is not None:
                # ordered by timing priority
                if msg['type'] == 'NoteOn':
                    if msg['note'] == self.model.note:
                        self.audio.play(self.model.wav)
                        cpx.toggle_led()
                elif msg['type'] == 'CC':
                    self.process_cc(msg)
                elif msg['type'] == 'NoteOff':
                    if msg['note'] == self.model.note:
                        self.audio.stop()
                        cpx.toggle_led()
        return self
