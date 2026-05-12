
import config
import os
from audiocore import WaveFile

def update_index(button_count: int, cc_count: int, mod: int):
    return (button_count + cc_count) % mod

class PlayerModel(object):
    def __init__(self, note=config.note_number, 
                 bank_button_count=config.STARTING_BANK_INDEX, bank_cc_count=0, 
                 sample_button_count=0, sample_cc_count=0, wav=None):
        self.note = note
        self.bank_button_count = bank_button_count
        self.bank_cc_count = bank_cc_count
        self.bank_index = update_index(bank_button_count, bank_cc_count, len(config.BANKS))
        self.sample_button_count = sample_button_count
        self.sample_cc_count = sample_cc_count
        self.sample_index = update_index(sample_button_count, 
                                         sample_cc_count, config.SAMPLE_COUNT)
        self.cc_keys = list(config.CC_VALUES)
        self.wav = wav
        self.update_display = False

    def update_bank_index(self):
        self.bank_index = update_index(self.bank_button_count, 
                                       self.bank_cc_count, len(config.BANKS))
        self.change_sample()
        self.update_display = True

    def update_sample_index(self):
        self.sample_index = update_index(self.sample_button_count, 
                                         self.sample_cc_count, config.SAMPLE_COUNT)
        self.change_sample()
        self.update_display = True

    def increment_bank(self):
        self.bank_button_count += 1
        self.update_bank_index()
        self.update_display = True

    def increment_sample(self):
        self.sample_button_count += 1
        self.update_sample_index()
        self.update_display = True

    def change_sample(self):
        path = config.BANKS[self.bank_index] + '/' + str(self.sample_index)
        fileName = os.listdir(path)[0]
        self.wav_file = open(path + '/' + fileName, 'rb')
        self.wav = WaveFile(self.wav_file)

