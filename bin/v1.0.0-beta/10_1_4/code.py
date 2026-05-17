# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Application Template

# Module Description:
# 

import gc
print("Starting memory: " + str(gc.mem_free()))
import config
print("After config: " + str(gc.mem_free()))
from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))
from model import PlayerModel
print("After model: " + str(gc.mem_free()))
from midi_controller import MidiController 
print("After midi controller: " + str(gc.mem_free()))

from board_controller import ActiveView


tm = PlayerModel()
tm.change_sample()

midi = MinimalMidi(config.note_channel_in, config.cc_channel_in)

mc = MidiController(tm, midi)
mc.midi.clear_msgs()

bc = ActiveView(tm, midi).update_mode()
bc.update_pixels()
print("After object creation: " + str(gc.mem_free()))

while True:
    mc = mc.main()
    bc = bc.update_mode()
    bc = bc.main()
