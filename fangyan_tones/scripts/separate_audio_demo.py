import torchaudio

from fangyan_tones.utils import (
    load_separator_model,
    get_wavs,
    convert_wav,
    save_wav
)

#TODO figure out how to run on gpu so we can mass run these on my desktop
if __name__ == "__main__":
    sepformer = load_separator_model(gpu=False)
    example_wavs = get_wavs("fangyan_tones/raw_wavs/")
    for wav in example_wavs:
        waveform, sample_rate = torchaudio.load(wav, format="wav")
        processed_audio = convert_wav(wav, sepformer)
        save_wav("fangyan_tones/fangyan_tones/processed_wavs/" + wav.split("/")[-1], processed_audio)