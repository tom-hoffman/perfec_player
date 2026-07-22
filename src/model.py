# PERFEC System Sample Player
# model.py
# copyright 2026, Tom Hoffman
# MIT License

import config
import os
from audiocore import WaveFile

class PlayerModel(object):
    def __init__(self, note_index=config.DEFAULT_NOTE_INDEX, note_tuple=config.NOTE_TUPLE, bank_index=config.STARTING_BANK_INDEX, sample_index=config.DEFAULT_SAMPLE_INDEX, wav=None):
        self.note_index: int = note_index
        self.note_tuple: tuple = note_tuple
        self.note: int = note_tuple[note_index]
        
        self.bank_index: int = bank_index
        self.sample_index: int = sample_index
        
        self.wav = wav
        self.update_display: bool = False
        
        # Track our explicit file handle state to prevent RAM leaks
        self.wav_file = None
        
        # Initial baseline sample initialization
        self.change_sample()

    def increment_bank(self) -> None:
        self.bank_index = (self.bank_index + 1) % len(config.BANKS)
        self.change_sample()
        self.update_display = True

    def increment_sample(self) -> None:
        self.sample_index = (self.sample_index + 1) % config.SAMPLE_COUNT
        self.change_sample()
        self.update_display = True

    def change_sample(self) -> None:
        # Close the old file descriptor safely before opening a new one to prevent RAM leakage
        if self.wav_file is not None:
            self.wav_file.close()
        path: str = config.BANKS[self.bank_index] + '/' + str(self.sample_index)
        try:
            fileName: str = os.listdir(path)[0]
            self.wav_file = open(path + '/' + fileName, 'rb')
            self.wav = WaveFile(self.wav_file)
        except (OSError, IndexError):
            # Safe boundary catch if a laboratory folder is missing or layout is un-configured
            self.wav_file = None
            self.wav = None

    def increment_note(self) -> None:
        self.note_index = (self.note_index + 1) % len(config.NOTE_TUPLE)
        self.note = self.note_tuple[self.note_index]
        self.update_display = True
