import cpx
import config

class View(object):

    def __init__(self, model, midi, pix=cpx.pix):
        self.model = model
        self.midi = midi
        self.pix = pix

    def main(self):
        # called by code.py regularly
        self.check_buttons()
        if self.model.update_display:
            self.update_pixels()
        return self

class ActiveView(View):

    def update_mode(self):
        # Check the switch and return current mode.
        if cpx.switch_is_left():
            self.model.update_display = True
            return ConfigurationView(self.model, self.midi, self.pix)
        else:
            return self

    def check_buttons(self):
        if cpx.a_button.went_down():
            self.model.increment_bank()
        elif cpx.b_button.went_down():
            self.model.increment_sample()

    def update_background(self):
        self.pix.fill(config.BANK_COLORS[self.model.bank_index])

    def update_selection(self):
        self.pix[self.model.sample_index] = config.SELECTION_COLOR

    def update_pixels(self):
        self.update_background()
        self.update_selection()
        self.model.update_display = False
        self.pix.show()

class ConfigurationView(View):
    '''
    This view should let you change the MIDI note you're listening for.
    '''

    def check_buttons(self):
        if cpx.a_button.went_down():
            self.model.increment_note()
        elif cpx.b_button.went_down():
            self.midi.increment_channel()
            self.model.update_display = True

    def update_mode(self):
        if cpx.switch_is_left():
            return self
        else:
            self.model.update_display = True
            return ActiveView(self.model, self.midi, self.pix)

    def display_note(self):
        for i in range(6):
            if i >= (6 - self.model.note_index):
                cpx.pix[i - 1] = (0, 0, 32)

    def display_channel(self):
        '''Uses a four bit binary number.'''
        n = self.midi.note_in_channel
        for i in range(4):
            if (n & (2 ** i)):
                self.pix[5 + i] = (32, 32, 32)
            else:
                self.pix[5 + i] = (8, 0, 8)

    def update_pixels(self):
        self.pix.fill((0, 0, 0))
        self.display_note()
        self.display_channel()
        self.model.update_display = False
        self.pix.show()


