from pytube import YouTube

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_lowest_resolution()
    try:
        youtubeObject.download(filename="save.mp4")
    except:
        print("An error has occurred")
    print("Download is completed successfully")


link = "https://www.youtube.com/watch?v=KBsqQez-O4w"
Download(link)