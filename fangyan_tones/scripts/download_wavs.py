import youtube_dl
from pydub import AudioSegment

# TODO argparse or something rather than hard coding lol
output_dir = "./fangyan_tones/raw_wavs/"
ydl_opts = {
    'format': 'm4a',
    'postprocessors': 
    [
        {
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }
    ],
}

example_songs = [
    "https://www.youtube.com/watch?v=aknkofx2bHg"
]


if __name__ == "__main__":

    # TODO Currently youtube dl just pulls the best audio type, you can't force it to do wav because youtube doesn't use wav. 
    # Instead it uses mp4 maybe? So figure out how to do mp4 and convert to wav on download
    for example_song in example_songs:
        # Get video title by downloading metadata
        video_title = ""
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(example_song, download=False)
            video_title = info_dict.get('title', None)
            # process title to something usable for file
            video_title = video_title.replace(" ", "_").replace(".", "")
            ydl_opts['outtmpl'] = output_dir + video_title + ".mp3"


        #HACK Re run youtubedl after editing title metadata in config  
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading ", video_title, "...")
            ydl.download([example_song])
            sound = AudioSegment.from_mp3(ydl_opts['outtmpl'])
            wav_path = ydl_opts['outtmpl'][:-4] + ".wav"
            sound.export(wav_path, format="wav")
            