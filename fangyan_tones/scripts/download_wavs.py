import subprocess
import glob
import time

example_songs = ["https://www.youtube.com/watch?v=aknkofx2bHg"]

if __name__ == "__main__":

    # TODO Currently youtube dl just pulls the best audio type, you can't force it to do wav because youtube doesn't use wav.
    # Instead it uses mp4 maybe? So figure out how to do mp4 and convert to wav on download
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

            os.system('ffmpeg -i ' + "'" + file_path + "'" + " '" + file_out + "'")
            os.remove(file_path)
            break
