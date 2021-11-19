import youtube_dl
from pydub import AudioSegment
import subprocess

from pytube import YouTube
import yt-dlp

# TODO argparse or something rather than hard coding dir lol
output_dir = "./fangyan_tones/raw_wavs/"
ydl_opts = {
    'format' : 'bestvideo[ext=mp4]+bestaudio', 
    "audioformat": "wav",
    'merge-output-format' : 'mp4',
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }
        ]

}

# TODO Seconds please, didn't write capability to parse time yet. # num seconds to start, num second to end 
example_songs = [
    ["https://www.youtube.com/watch?v=JfHPOPwWabc", [("3", "7")]],
    ["https://www.youtube.com/watch?v=aknkofx2bHg", [("33", "64"), ("88", "100"), ("100, 132"), ("132", "153")],]
]

# TODO Get 4 segments from ^^^^, based on 0:33-1:04 female rapping, 1:28-1:40 opera, 1:40-2:12 male rapping, and the hook
if __name__ == "__main__":

    # TODO Currently youtube dl just pulls the best audio type, you can't force it to do wav because youtube doesn't use wav. 
    # Instead it uses mp4 maybe? So figure out how to do mp4 and convert to wav on download
    wav_path = ""
    for example_song, timestamps in example_songs:
        # example_song += "&title=something"
        # Get video title by downloading metadata
        # video_title = ""
        import os
        cmd = "yt-dlp -f 'ba' " + example_song
        os.system(cmd)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(example_song, download=False)
            video_title = info_dict.get('title', None)
            # download title to something usable for file name
            video_title = video_title.replace(" ", "_").replace(".", "")
            ydl_opts['outtmpl'] = output_dir + video_title + ".mp4"


        #HACK Re run youtubedl after editing title metadata in config  
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading ", video_title, "...")
            ydl.download([example_song])
            sound = AudioSegment.from_mp3(ydl_opts['outtmpl'])
            wav_path = ydl_opts['outtmpl'][:-4] + ".wav"
            sound.export(wav_path, format="wav")
        
        # Unpack timestamps and loop over them, cut up song into that chunk
        # Spawn subprocesses to do this concurrently, then we can continue downloading as well
        for time_start, time_end in timestamps:
            num_seconds = time_end - time_start
            subprocess.run(f"ffmpeg -i {wav_path} -vcodec copy -acodec copy -ss {time_start} -t {num_seconds} {wav_path}_time_start_{time_start}_end_{time_end}.mp4", shell=True)


        