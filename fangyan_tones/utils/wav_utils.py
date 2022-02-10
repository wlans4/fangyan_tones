from typing import List
import pathlib
from pydub import AudioSegment
import os

import librosa
import numpy as np
import soundfile as sf
import torch
from fangyan_tones.lib import nets
from fangyan_tones.lib import spec_utils
from fangyan_tones.lib.vocal_remover import VocalRemover
import argparse

def split_segment(wav_path, time_chunks: List[str]):
    """Splits a song into multiple chunks, based on time chunks in the format
    of ["1:51-2:20", "2:30-2:55"] etc

    Args:
        wav_path ([type]): [description]
        output_path ([type]): [description]
        time_chunks (List[str]): [description]
    """
    audio_segment = AudioSegment.from_wav(wav_path)
    song_name = wav_path.split("/")[-1].split(".")[0]
    processed_path = str(pathlib.Path(wav_path).parent.parent) + "/processed_wavs/"
    output_paths = []
    for time in time_chunks:
        times = time.split("-")
        t1 = get_sec(times[0]) * 1000 #Works in milliseconds
        t2 = get_sec(times[1]) * 1000
        segment = audio_segment[t1:t2]
        output_path = f"{processed_path}{song_name}_{time}.wav"
        output_paths.append(output_path)
        segment.export(output_path, format="wav")
    return output_paths
    

def get_sec(time_str):
    """Get Seconds from time."""
    if ":" in time_str:
        min, sec = time_str.split(':')
        return int(min) * 60 + int(sec)
    else:
        return int(time_str)


def separate_audio(wav_paths):

    # TODO stop using argparse in a function.. too lazy to change 
    p = argparse.ArgumentParser()
    p.add_argument('--gpu', '-g', type=int, default=-1)
    p.add_argument('--sr', '-r', type=int, default=44100)
    p.add_argument('--n_fft', '-f', type=int, default=2048)
    p.add_argument('--hop_length', '-H', type=int, default=1024)
    p.add_argument('--batchsize', '-B', type=int, default=4)
    p.add_argument('--cropsize', '-c', type=int, default=256)
    p.add_argument('--output_image', '-I', action='store_true')
    p.add_argument('--postprocess', '-p', action='store_true')
    p.add_argument('--tta', '-t', action='store_true')
    args = p.parse_args()

    print('loading model...', end=' ')
    device = torch.device('cpu')
    model = nets.CascadedNet(args.n_fft)
    model.load_state_dict(torch.load("fangyan_tones/pretrained_models/vocal_separator_baseline.pth", map_location=device))
    if torch.cuda.is_available() and args.gpu >= 0:
        device = torch.device('cuda:{}'.format(args.gpu))
        model.to(device)
    print('done')

    for wav in wav_paths:

        print(f'Loading {wav}...', end=' ')
        X, sr = librosa.load(
            wav, sr=args.sr, mono=False, dtype=np.float32, res_type='kaiser_fast')
        basename = os.path.splitext(os.path.basename(wav))[0]
        print('done')

        if X.ndim == 1:
            # mono to stereo
            X = np.asarray([X, X])

        X_spec = spec_utils.wave_to_spectrogram(X, args.hop_length, args.n_fft)

        sp = VocalRemover(model, device, args.batchsize, args.cropsize, args.postprocess)

        if args.tta:
            y_spec, v_spec = sp.separate_tta(X_spec)
        else:
            y_spec, v_spec = sp.separate(X_spec)


        wave = spec_utils.spectrogram_to_wave(v_spec, hop_length=args.hop_length)
        sf.write(wav, wave.T, sr)