import torchaudio

from fangyan_tones.utils import (
#     load_separator_model,
    get_wavs,
#     convert_wav,
#     save_wav
)
import argparse
import os

import cv2
import librosa
import numpy as np
import soundfile as sf
import torch
from tqdm import tqdm

from lib import dataset
from lib import nets
from lib import spec_utils

from fangyan_tones.scripts import VocalRemover

#TODO figure out how to run on gpu so we can mass run these on my desktop
if __name__ == "__main__":
    # sepformer = load_separator_model(gpu=False)
    example_wavs = get_wavs("fangyan_tones/raw_wavs/")
    # for wav in example_wavs:
    #     print(wav)
    #     waveform, sample_rate = torchaudio.load(wav, format="wav")
    #     processed_audio = convert_wav(wav, sepformer)
    #     save_wav("fangyan_tones/fangyan_tones/processed_wavs/" + wav.split("/")[-1], processed_audio)
    
    print('loading model...', end=' ')
    device = torch.device('cpu')
    model = nets.CascadedASPPNet(2048)
    model.load_state_dict(torch.load("pretrained_models/vocal_separator_baseline.pth", map_location=device))
    # if torch.cuda.is_available():
    #     device = torch.device('cuda:{}'.format(args.gpu))
    #     model.to(device)
    print('done')
    print(os.getcwd())
    for wav in example_wavs:
        print('loading wave source...', end=' ')
        X, sr = librosa.load(
            wav, 44100, False, dtype=np.float32, res_type='kaiser_fast')
        basename = os.path.splitext(os.path.basename(wav))[0]
        print('done')

        if X.ndim == 1:
            X = np.asarray([X, X])

        print('stft of wave source...', end=' ')
        X = spec_utils.wave_to_spectrogram(X, 1024, 2048)
        print('done')

        vr = VocalRemover(model, device,512)

        # improves quality
        # if args.tta:
        #     pred, X_mag, X_phase = vr.inference_tta(X)
        # else:
        pred, X_mag, X_phase = vr.inference(X)

        
        print('post processing...', end=' ')
        pred_inv = np.clip(X_mag - pred, 0, np.inf)
        pred = spec_utils.mask_silence(pred, pred_inv)
        print('done')

        print('inverse stft of instruments...', end=' ')
        y_spec = pred * X_phase
        wave = spec_utils.spectrogram_to_wave(y_spec, hop_length=1024)
        print('done')
        
        sf.write(os.getcwd() + "/fangyan_tones/processed_wavs/" + "{}_Instruments.wav".format(basename), wave.T, sr)

        print("inverse stft of vocals...", end=" ")
        v_spec = np.clip(X_mag - pred, 0, np.inf) * X_phase
        wave = spec_utils.spectrogram_to_wave(v_spec, hop_length=1024)
        print("done")

        sf.write(os.getcwd() + "/fangyan_tones/processed_wavs/" + "{}_Vocals.wav".format(basename), wave.T, sr)
