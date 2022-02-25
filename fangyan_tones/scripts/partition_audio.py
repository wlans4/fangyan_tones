
from fangyan_tones.utils.wav_utils import split_segment, separate_audio
import pathlib

directory = "/Users/wyatt/Projects/fangyan_tones/fangyan_tones/raw_wavs"
segments = [

    ["0:45-1:27", "1:28-2:08"],
    ["0:30-1:20", "1:46-2:10"],
    ["0:33-1:25", "1:46-2:10"]
]

if __name__ == "__main__":
    
    song_paths = [str(song_path.absolute()) for song_path in pathlib.Path(directory).glob("*.wav")]
    song_output_paths = []
    for song_path, song_segments in zip(song_paths, segments):
        song_output_paths += split_segment(song_path, song_segments)
    
    separate_audio(song_output_paths)
