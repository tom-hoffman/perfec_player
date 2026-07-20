# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT
# Modular Playground Application Template
# Module Description: Main runtime coordinator loop

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
tm.change_sample()

# Pre-instantiate our MIDI parser and primary state engine context
midi: MinimalMidi = MinimalMidi(config.note_channel_in, config.cc_channel_in)
mc: midi_controller.MidiController = midi_controller.MidiController(tm, midi)

# Pre-instantiate ALL possible views once at boot time to prevent dynamic heap fragmentation
view_active = board_controller.ActiveView(tm, midi)
view_config = board_controller.ConfigurationView(tm, midi)

# Fast dictionary map to swap active view modes allocation-free based on the slide switch state
# True (Switch Left) -> Configuration Menu | False (Switch Right) -> Live Sample Player
view_map: dict = {
    False: view_active,
    True: view_config
}

# Determine our initial view layout state based on the physical switch position
bc = view_map[board_controller.cpx.switch_is_left()].update_mode()
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
    
    # 2. State-Machine Synchronization & Input Polling: 
    # Only updates modes and polls physical button inputs if a state change is flagged,
    # keeping the execution loop focused entirely on real-time MIDI audio playback!
    if tm.update_display:
        bc = view_map[board_controller.cpx.switch_is_left()].update_mode()
        bc = bc.main()
