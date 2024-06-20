from pytube import YouTube
from pythumb import Thumbnail
import os
import subprocess

#function to remove invalid characters from a video title so that it can be properly downloaded
def clean_filename(filename):
    #make a set of invalid characters
    invalid_chars = r'\/:*?<>|"'
    invalid_characters = set(invalid_chars)

    #make a new string with invalid characters removed
    #if the character is in the set of invalid_characters, then it will be replaced with '_'
    cleaned_text = ''.join(['_' if char in invalid_characters else char for char in filename])

    #return the file name with invalid characters removed
    return cleaned_text


#function to download the YouTube video as mp4 given the url and download path
def download_youtube_mp4(url, save_path):
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
        print(f"Video downloaded successfully! Saved as '{video_title}.mp4'")

    except Exception as e:
        print("An error occurred:", str(e))

def convertMP4ToMP3(input_file, output_file):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        output_file
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("Error", "ffmpeg command failed", e)

#function to download the YouTube video as mp3 given the url and download path
def download_youtube_mp3(url, save_path):
    try:
        #create a YouTube object
        yt = YouTube(url)
        video_title = clean_filename(yt.title)

        #choose the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        #download stream to the specified path
        stream.download(output_path=save_path, filename=f"{video_title}.mp4")

        convertMP4ToMP3(f"{save_path}/{video_title}.mp4",f"{save_path}/{video_title}.mp3")

        print(f"Video downloaded successfully! Save as '{video_title}.mp3'")

    except Exception as e:
        print("An error occurred: ", str(e))


#function to download the YouTube video thumbnail given the url and download path
def download_youtube_thumbnail(url, save_path):
    try:
        #create YouTube object
        yt = YouTube(url)

        # get the video title
        thumbnail_filename = clean_filename(yt.title)

        #get the highest resolution of thumbnail, maxresdefault
        thumbnail = Thumbnail(url)
        thumbnail.fetch(size="maxresdefault")

        #save thumbnail to the specified save path
        thumbnail.save(dir=save_path, filename=thumbnail_filename)

        print(f"Thumbnail downloaded successfully! Saved as '{thumbnail_filename}.jpg'")

    except Exception as e:
        print("An error occurred:", str(e))


if __name__=="__main__":

    #while loop to continue downloading videos until told otherwise
    while True:
        #input url, save path, and give option to download thumbnail
        video_url= input("Enter the YouTube video URL: ")
        save_path = input("Enter the path to save the video: ")
        save_thumbnail = input("Do you want to save the thumbnail? (Y/N): ").strip().upper()
        format = input("Enter the video format(mp4/mp3): ")

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        #check if format is mp3 or mp4
        if format == "mp4":
            # call function to download video
            download_youtube_mp4(video_url, save_path)
        elif format == "mp3":
            # call function to download video
            download_youtube_mp3(video_url, save_path)

        #if told yes to download thumbnail, call function to download thumbnail
        if save_thumbnail == "Y":
            download_youtube_thumbnail(video_url, save_path)

        #option to download another video
        #if yes, then continue while loop
        #if no, end loop and break
        download_again = input("\nDo you want to download another video? (Y/N): ").strip().upper()

        if download_again != "Y":
            break
