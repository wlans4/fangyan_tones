import subprocess
import glob
import time

from fangyan_tones.utils.wav_utils import split_segment, separate_audio
import pathlib

example_songs = [
    # "https://youtu.be/OR-0wptI_u0", "https://youtu.be/8CD06hC1KGU",
    # "https://youtu.be/wr-6wwt8RXk", "https://youtu.be/nhyT8HDT4lg",
    # "https://youtu.be/55yJh4SHUBY", "https://youtu.be/DuErkkiCaZU",
    "https://youtu.be/LdPjnubLRN0"  #, "https://youtu.be/EZxhW-uSN_I",
    # "https://youtu.be/-WkecBaA4z8", "https://youtu.be/LL50Fu4UvG0",
    # "https://youtu.be/_byK6M95hTc", "https://youtu.be/npiAxeLtHDM",
    # "https://youtu.be/9q7JOQfcJQM", "https://youtu.be/TMB6-YflpA4"
]
directory = "/Users/wyatt/Projects/fangyan_tones/fangyan_tones/raw_wavs"
segments = [
    # ["0:30-1:50"], ["0:43-1:02", "1:42-2:11"], ["0:55-1:14"],
    #         ["0:38-1:15", "2:07-2:35"], ["0:36-0:44"],
    #         ["0:40-1:00", "1:30-1:42"],
    ["0:33-1:43"]  #, ["0:18-0:42"],
    # ["0:47-0:57"], ["0:29-2:00"], ["0:48-1:10", "1:20-1:52"],
    # ["1:33-1:47"], ["1:40-2:48"], ["2:14-2:56"]
]

if __name__ == "__main__":

    # Download audio first
    wav_path = ""
    import os, subprocess
    processes = []
    segment_to_title = []
    for i, example_song in enumerate(example_songs):
        # example_song += "&title=something"
        # Get video title by downloading metadata
        # video_title = ""
        import os
        import subprocess
        # Not sure if running these as subprocesses actually leads to any speedup here, can probably just do all of these sequentially..
        processes.append(
            subprocess.Popen([
                'youtube-dl', '-f', 'bestaudio[ext=m4a]', example_song,
                '--output', 'fangyan_tones/raw_wavs/%(title)s.%(ext)s"',
                '--extract-audio', '--download-archive',
                'wav_downloader_archive.txt', '--restrict-filenames'
            ]))
        # TODO still need to fix issue with title here, if the title has a ' in it then we need to restrict filename but then it throws off chinese chars..
        title = subprocess.check_output([
            "youtube-dl", "--skip-download", "--get-title", f"{example_song}",
            "--restrict-filenames"
        ])
        segment_to_title.append(
            title.decode("utf-8")[:-2].replace("'", "").replace('"', ''))
    # Wait until all downloads are done before continuing..
    for process in processes:
        process.wait()
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
            file_out = file_out.replace("'", "").replace('"', '')

            # see more info here for filtering high freq:
            # https://superuser.com/questions/733061/reduce-background-noise-and-optimize-the-speech-from-an-audio-clip-using-ffmpeg
            # Convert to wav with lowpass filter for maximizing upper range to 4khz
            output_command = 'ffmpeg -i ' + "'" + file_path + "'" + " -af 'lowpass=f=4000' '" + file_out + "'"
            print("\n", output_command)
            print("\n")
            os.system(output_command)
            os.remove(file_path)
        break

    # Partition audio
    song_paths = [
        str(song_path.absolute())
        for song_path in pathlib.Path(directory).glob("*.wav")
    ]
    song_output_paths = []
    for song_path in song_paths:

        song_segments = []
        for i, title in enumerate(segment_to_title):
            if title in song_path:
                song_segments = segments[i]
        if song_segments:
            song_output_paths += split_segment(song_path, song_segments)
        else:
            song_segments += [song_path]

    separate_audio(song_output_paths)
