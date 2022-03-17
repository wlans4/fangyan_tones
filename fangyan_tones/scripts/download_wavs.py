import subprocess
import glob
import time

example_songs = ["https://www.youtube.com/watch?v=aknkofx2bHg"]
directory = "/Users/wyatt/Projects/fangyan_tones/fangyan_tones/raw_wavs"
segments = [["0:45-1:27", "1:28-2:08"], ["0:30-1:20", "1:46-2:10"],
            ["0:33-1:25", "1:46-2:10"]]

from fangyan_tones.utils.wav_utils import split_segment, separate_audio
import pathlib

if __name__ == "__main__":

    # Download audio first
    wav_path = ""
    import os, subprocess

    for example_song in example_songs:
        # example_song += "&title=something"
        # Get video title by downloading metadata
        # video_title = ""
        import os
        import subprocess
        subprocess.run([
            'youtube-dl', '-f', 'bestaudio[ext=m4a]', example_song, '--output',
            'fangyan_tones/raw_wavs/%(title)s.%(ext)s"', '--extract-audio'
        ])

    while True:
        audio_files = [
            file for file in glob.glob("fangyan_tones/raw_wavs/*")
            if file[-3:] != "wav"
        ]
        parts = [file for file in audio_files if ".part" in file]
        if parts:
            time.sleep(3)
            print(".part file still exists, sleeping..")
            continue
        for file_path in audio_files:
            file_out = file_path[:-4] + ".wav"

            os.system('ffmpeg -i ' + "'" + file_path + "'" + " '" + file_out +
                      "'")
            os.remove(file_path)
            break

    # Partition audio
    song_paths = [
        str(song_path.absolute())
        for song_path in pathlib.Path(directory).glob("*.wav")
    ]
    song_output_paths = []
    for song_path, song_segments in zip(song_paths, segments):
        song_output_paths += split_segment(song_path, song_segments)

    separate_audio(song_output_paths)
