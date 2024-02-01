from pytube import YouTube
from pythumb import Thumbnail
import os


def clean_filename(filename):
    #remove invalid characters from a video title so that it can be properly downloaded
    invalid_chars = r'\/:*?<>|"'
    invalid_characters = set(invalid_chars)

    cleaned_text = ''.join(['_' if char in invalid_characters else char for char in filename])

    return cleaned_text


def download_youtube_video(url, save_path):
    try:
        #create a YouTube object
        yt = YouTube(url)

        #get the video title
        video_title = clean_filename(yt.title)
        print("Video Title: ", video_title)

        #choose the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        #download stream to the specified path
        stream.download(output_path=save_path, filename=f"{video_title}.mp4")
        print(f"Video downloaded successfully! Saved as '{video_title}.jpg'")

    except Exception as e:
        print("An error occurred:", str(e))


def download_youtube_thumbnail(url, save_path):
    try:
        #create YouTube object
        yt = YouTube(url)

        # get the video title
        thumbnail_filename = clean_filename(yt.title)

        thumbnail = Thumbnail(url)
        thumbnail.fetch(size="maxresdefault")
        thumbnail.save(dir=save_path, filename=thumbnail_filename)

        print(f"Thumbnail downloaded successfully! Saved as '{thumbnail_filename}.jpg'")

    except Exception as e:
        print("An error occurred:", str(e))


if __name__=="__main__":

    while True:
        video_url= input("Enter the YouTube video URL: ")
        save_path = input("Enter the path to save the video: ")
        save_thumbnail = input("Do you want to save the thumbnail? (Y/N): ").strip().upper()

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        download_youtube_video(video_url, save_path)

        if save_thumbnail == "Y":
            download_youtube_thumbnail(video_url, save_path)

        download_again = input("\nDo you want to download another video? (Y/N): ").strip().upper()

        if download_again != "Y":
            break
