import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board
import audioio          # outputting the samples.

import config

class Debouncer(object):

    def __init__(self, b, current_value=None):
        self.b = b
        if current_value is None:
            self.current_value = b.value
        else:
            self.current_value = current_value

    def went_down(self):
        new = self.b.value
        changed = new and (not self.current_value)
        self.current_value = new
        return changed
        
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

def toggle_led():
    led.value = not(led.value)

a_button_raw = digitalio.DigitalInOut(board.BUTTON_A)
a_button_raw.direction = digitalio.Direction.INPUT
a_button_raw.pull = digitalio.Pull.DOWN
a_button = Debouncer(a_button_raw)

b_button_raw = digitalio.DigitalInOut(board.BUTTON_B)
b_button_raw.direction = digitalio.Direction.INPUT
b_button_raw.pull = digitalio.Pull.DOWN
b_button = Debouncer(b_button_raw)

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

def switch_is_left():
    return switch.value

pix = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

audio = audioio.AudioOut(board.A0)

spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = config.SPEAKER_ENABLE
