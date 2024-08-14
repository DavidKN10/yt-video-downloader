from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from pythumb import Thumbnail
import os


def clean_filename(filename):
    """
    Removes invalid characters in the video title and replaces it with "_".
    Used to set the file name as the video title.
    """
    invalid_chars = r'\/:*?<>|"'
    invalid_characters = set(invalid_chars)

    cleaned_text = ''.join(['_' if char in invalid_characters else char for char in filename])

    return cleaned_text


def download_mp4(url, path):
    """
    Downloads video as MP4.
    Make YouTube object, then get video title and use clean_filename() on the title.
    Make a stream with the highest resolution and then display the video title.
    Download video and print out results.
    If an error occurrs, print exception.
    """
    try:
        yt = YouTube(url)
        video_title = clean_filename(yt.title)
        stream = yt.streams.get_highest_resolution()

        print("Video Title: ", video_title)

        stream.download(output_path=path, filename=f"{video_title}.mp4")
        print("Video downloaded successfully!")
        print("Saved as: {video_title}.mp4")
    except Exception as e:
        print("An error occurred: ", str(e))


def download_mp3(url, path):
    """
    Same as download_mp4(), but download as MP3.
    """
    try:
        yt = YouTube(url)
        video_title = clean_filename(yt.title)
        stream = yt.streams.get_audio_only()

        print("Video Title: ", video_title)

        stream.download(output_path=path, filename=f"{video_title}.mp3", mp3=True)
        print("Video downloaded successfully!")
        print("Saved as: {video_title}.mp3")
    except Exception as e:
        print("An error occurred: ", str(e))


def download_thumbnail(url, save_path):
    """
    Function to download the video thumbnail.
    Make a YouTube object to get the title.
    Make a Thumbnail object and get the highest resolution.
    Download image and print result.
    If an error occurs, print exception.
    """
    try:
        yt = YouTube(url)

        thumbnail_filename = clean_filename(yt.title)

        thumbnail = Thumbnail(url)
        thumbnail.fetch(size="maxresdefault")

        thumbnail.save(dir=save_path, filename=thumbnail_filename)

        print(f"Thumbnail downloaded successfully! Saved as '{thumbnail_filename}.jpg'")

    except Exception as e:
        print("An error occurred:", str(e))


def download_playlist(url, path):
    """
    Function to download a full playlist.
    Make a Playlist object. Then video is downloaded using the same logic as download_mp4(), but in a for loop.
    If an error occurs, print exception.
    """
    try:
        playlist = Playlist(url)

        print("Playlist: {playlist.title}\n")

        for video in playlist.videos:
            video_title = clean_filename(video.title)
            print(f"Downloading: {video_title}")
            stream = video.streams.get_highest_resolution()
            stream.download(output_path=path, filename=f"{video_title}.mp4")

        print("Done. Playlist downloaded successfully!")

    except Exception as e:
        print("An error has occurred: ", str(e))


"""
First ask you are downloading a video or an entire playlist.

If playlist:
    - Enter URL
    - Enter path to save video
    - When done, ask you would like to download something else.
        * If yes, then go back to choosing between video or playlist
        * If no, then exit

If video:
    - Enter URL
    - Enter path to save video
    - Ask if you want to save thumbnail
    - Ask if you want to save as MP3 or MP4
    - When done, ask if you want to download something else

"""
if __name__ == "__main__":
    while True:

        video_or_playlist = input("Video or playlist? (V/P) > ").strip().upper()

        if video_or_playlist == "P":
            url = input("Enter playlist URL > ")
            path = input("Enter path to save playlist > ")

            if not os.path.exists(path):
                os.makedirs(path)

            download_playlist(url, path)

            download_again = input("\nDo you want to download something else? (Y/N) > ").strip().upper()

        else:
            url = input("Enter video URL > ")
            path = input("Enter path to save video > ")
            save_thumbnail = input("Do you want to save the thumbnail? (Y/N) > ").strip().upper()
            format = input("Enter format to save video as (mp3/mp4) > ")

            if not os.path.exists(path):
                os.makedirs(path)

            if format == "mp4":
                download_mp4(url, path)
            elif format == "mp3":
                download_mp3(url, path)

            if save_thumbnail == "Y":
                download_thumbnail(url, path)

            download_again = input("\nDo you want to download something else? (Y/N) > ").strip().upper()

        if download_again != "Y":
            break
