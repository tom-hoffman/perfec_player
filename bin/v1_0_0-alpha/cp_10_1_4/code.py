# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Application Template

# Module Description:
# 

import gc
print("Starting memory: " + str(gc.mem_free()))
import config

from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))
from model import PlayerModel
print("After model: " + str(gc.mem_free()))
from midi_controller import MidiController 
print("After midi controller: " + str(gc.mem_free()))


from board_controller import ActiveView

# send MIDI messages on:
channel_out = 1

tm = PlayerModel()
tm.change_sample()

mc = MidiController(tm, MinimalMidi(config.note_channel_in, 
                                    config.cc_channel_in))
mc.midi.clear_msgs()

bc = ActiveView(tm).update_mode()
bc.update_pixels()
print("After object creation: " + str(gc.mem_free()))
while True:
    mc = mc.main()
    bc = bc.update_mode()
    bc = bc.main()
