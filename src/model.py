# PERFEC System Sample Player
# model.py
# copyright 2026, Tom Hoffman
# MIT License

import config
import os
from audiocore import WaveFile

def update_index(button_count: int, cc_count: int, mod: int) -> int:
    return (button_count + cc_count) % mod

class PlayerModel(object):
    def __init__(self, note_index=config.DEFAULT_NOTE_INDEX, note_tuple=config.NOTE_TUPLE, bank_button_count=config.STARTING_BANK_INDEX, bank_cc_count=0, sample_button_count=0, sample_cc_count=0, wav=None):
        self.note_index: int = note_index
        self.note_tuple: tuple = note_tuple
        self.note: int = note_tuple[note_index]
        self.bank_button_count: int = bank_button_count
        self.bank_cc_count: int = bank_cc_count
        self.bank_index: int = update_index(bank_button_count, bank_cc_count, len(config.BANKS))
        self.sample_button_count: int = sample_button_count
        self.sample_cc_count: int = sample_cc_count
        self.sample_index: int = update_index(sample_button_count, sample_cc_count, config.SAMPLE_COUNT)
        self.cc_keys: list = list(config.CC_VALUES)
        self.wav = wav
        self.update_display: bool = False
        
        # Track our explicit file handle state to prevent RAM leaks
        self.wav_file = None

    def update_bank_index(self) -> None:
        self.bank_index = update_index(self.bank_button_count, self.bank_cc_count, len(config.BANKS))
        self.change_sample()
        self.update_display = True

    def update_sample_index(self) -> None:
        self.sample_index = update_index(self.sample_button_count, self.sample_cc_count, config.SAMPLE_COUNT)
        self.change_sample()
        self.update_display = True

    def increment_bank(self) -> None:
        self.bank_button_count += 1
        self.update_bank_index()
        self.update_display = True

    def increment_sample(self) -> None:
        self.sample_button_count += 1
        self.update_sample_index()
        self.update_display = True

    def change_sample(self) -> None:
        # --- EXPLICIT RESOURCE CLEANUP ---
        # If an old file handle is currently open, safely close it first.
        # This prevents hidden file-descriptor leaks and avoids sudden MemoryErrors!
        if self.wav_file is not None:
            self.wav_file.close()
            
        path: str = config.BANKS[self.bank_index] + '/' + str(self.sample_index)
        fileName: str = os.listdir(path)[0]
        self.wav_file = open(path + '/' + fileName, 'rb')
        self.wav = WaveFile(self.wav_file)

    def increment_note(self) -> None:
        self.note_index = (self.note_index + 1) % len(config.NOTE_TUPLE)
        self.note = self.note_tuple[self.note_index]
        self.update_display = True
