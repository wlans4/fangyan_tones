from speechbrain.pretrained import SepformerSeparation as separator
import torchaudio
from pathlib import Path
import os


def load_separator_model(gpu=False):
    if gpu:
        return separator.from_hparams(source="speechbrain/sepformer-whamr", savedir='pretrained_models/sepformer-whamr',  run_opts={"device":"cuda"})
    return separator.from_hparams(source="speechbrain/sepformer-whamr", savedir='pretrained_models/sepformer-whamr')

def get_wavs(directory):
    wavs_paths = [directory + file for file in os.listdir(directory) if ".wav" in file[-4:]]
    return wavs_paths

def convert_wav(wave_file_path, model):
    return model.separate_file(path=wave_file_path)

def save_wav(output_name, converted_wav, sample_rate=8000):
    torchaudio.save(output_name, converted_wav[:, :, 0].detach().cpu(), sample_rate)

