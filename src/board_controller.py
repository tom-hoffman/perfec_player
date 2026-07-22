# PERFEC System Euclidian Sequencer
# board_controller.py
# copyright 2026, Tom Hoffman
# MIT License
# handles board input and output

import cpx
import config

class View(object):
    def __init__(self, model, midi, pix=cpx.pix):
        self.model = model
        self.midi = midi
        self.pix = pix
        # Placeholder pointer to the opposite layout state to allow allocation-free swapping
        self.target_mode_view = None

    def main(self) -> "View":
        # called by code.py regularly
        self.check_buttons()
        if self.model.update_display:
            self.update_pixels()
        return self

    def check_buttons(self) -> None:
        pass

    def update_pixels(self) -> None:
        pass

class ActiveView(View):
    def update_mode(self) -> "View":
        # If the switch is left, route straight to our pre-instantiated config view layout
        if cpx.switch_is_left():
            self.model.update_display = True
            return self.target_mode_view
        else:
            return self

    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            self.model.increment_bank()
        elif cpx.b_button.went_down():
            self.model.increment_sample()

    def update_pixels(self) -> None:
        # Bounded single-pass rendering loop: Floods the ring with the active bank color 
        # while cleanly overwriting the active sample cursor (0-9) allocation-free.
        bank_color = config.BANK_COLORS[self.model.bank_index]
        active_sample: int = self.model.sample_index
        
        for i in range(10):
            if i == active_sample:
                cpx.pix[i] = config.SELECTION_COLOR
            else:
                cpx.pix[i] = bank_color
                    
        self.model.update_display = False
        cpx.pix.show()

class ConfigurationView(View):
    '''
    This view lets you change the MIDI note and channel you're listening for.
    '''
    def check_buttons(self) -> None:
        if cpx.a_button.went_down():
            self.model.increment_note()
        elif cpx.b_button.went_down():
            self.midi.increment_channel()
            self.model.update_display = True

    def update_mode(self) -> "View":
        # If the switch is right, route straight back to our live sample playback layout
        if not cpx.switch_is_left():
            self.model.update_display = True
            return self.target_mode_view
        else:
            return self

    def display_note(self) -> None:
        # Upward-growing Cyan note tracker (Green + Blue) handling 6 options (0 to 5 LEDs lit)
        idx: int = self.model.note_index
        for i in range(5):
            if i < idx:
                cpx.pix[4 - i] = (0, 32, 32)
            else:
                cpx.pix[4 - i] = (0, 0, 0)

    def display_channel(self) -> None:
        '''Uses a four bit binary number to display the active channel layout on LEDs 5-8.'''
        n: int = self.midi.note_in_channel
        for i in range(4):
            if n & (1 << i):
                # Bright Yellow/Amber color (Green + Red) representing 1
                cpx.pix[5 + i] = (32, 32, 0)
            else:
                # Dim White/Purple representing 0
                cpx.pix[5 + i] = (8, 0, 8)
                
        # Access index 9 directly to turn the last pixel off safely without breaking the object pointer
        cpx.pix[9] = (0, 0, 0)

    def update_pixels(self) -> None:
        self.display_note()
        self.display_channel()
        self.model.update_display = False
        self.pix.show()
