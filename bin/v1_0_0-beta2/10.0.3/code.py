# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT
# PERFEC Player -- PERFEC System Sample Player
# Module Description: Main runtime loop

import gc
print("Starting memory: " + str(gc.mem_free()))
import config
print("After config: " + str(gc.mem_free()))
from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))
from model import PlayerModel
print("After model: " + str(gc.mem_free()))
import midi_controller
print("After midi controller: " + str(gc.mem_free()))
import board_controller
print("After board controller: " + str(gc.mem_free()))

# Initialize core model and load initial sample file handle
tm: PlayerModel = PlayerModel()

# Pre-instantiate our MIDI parser and primary state engine context
midi: MinimalMidi = MinimalMidi(config.note_channel_in)
mc: midi_controller.MidiController = midi_controller.MidiController(tm, midi)

# Pre-instantiate ALL possible views once at boot time to prevent dynamic heap fragmentation
view_active = board_controller.ActiveView(tm, midi)
view_config = board_controller.ConfigurationView(tm, midi)

# Store pointers to the view choices right inside the view objects so they can 
# route to each other allocation-free at runtime without needing complex cross-file lookups
view_active.target_mode_view = view_config
view_config.target_mode_view = view_active

# Set our initial view layout state based on the physical switch position
if board_controller.cpx.switch_is_left():
    bc = view_config
else:
    bc = view_active
    
bc.update_pixels()

# Set garbage collection to only happen when explicitly triggered outside active playback windows.
gc.disable()
gc.collect()
print("After object creation: " + str(gc.mem_free()))

# Flush any stray startup bytes out of the UART serial ring buffer
mc.midi.clear_msgs()

while True:
    # 1. High-Priority MIDI Parsing: Drains the incoming buffer queue in a fast block
    mc = mc.main()
    
    # 2. State-Machine Synchronization & Physical Button Input Polling:
    # Check for layout changes and process human button interface clicks smoothly
    bc = bc.update_mode()
    bc = bc.main()
