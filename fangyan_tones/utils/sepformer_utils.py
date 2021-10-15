from speechbrain.pretrained import SepformerSeparation as separator
import torchaudio
import os


def load_separator_model(gpu=False):
    if gpu:
        return separator.from_hparams(source="speechbrain/sepformer-whamr", savedir='pretrained_models/sepformer-whamr',  run_opts={"device":"cuda"})
    return separator.from_hparams(source="speechbrain/sepformer-whamr", savedir='pretrained_models/sepformer-whamr')

def get_wavs(directory):
    return [os.path.abspath(file) for file in os.listdir(directory) if ".wav" in file[-4:]]

def convert_wav(wave_file_path, model):
    return model.separate_file(path=wave_file_path)

def save_wav(output_name, converted_wav):
    torchaudio.save(output_name, converted_wav[:, :, 0].detach().cpu(), 8000)

