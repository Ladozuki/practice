from pytube import YouTube

def download_audio(video_url):
    yt = YouTube(video_url)
    audio = yt.streams.filter(only_audio = True).first()
    audio.download(filename = 'drone_track.mp4')

    print("Download Complete")

video_url = 'https://www.youtube.com/watch?v=6lqS34C4DCg&list=LL&index=3'

download_audio(video_url)

