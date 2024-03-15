from pytube import YouTube
from pythumb import Thumbnail


#function to remove invalid characters from a video title so that it can be properly downloaded
def clean_filename(filename):
    #remove invalid characters 
    invalid_chars = r'\/:*?<>|"'
    invalid_characters = set(invalid_chars)

    # make a new string with invalid characters removed
    # if the character is in the set of invalid_characters, then it will be replaced with '_'
    cleaned_text = ''.join(['_' if char in invalid_characters else char for char in filename])

    #return the file name with invalid characters removed
    return cleaned_text


#function to download the YouTube video as mp4given the url and download path
def download_youtube_mp4(url, save_path):
    try:
        #create a YouTube object
        yt = YouTube(url)

        #get the video title
        video_title = clean_filename(yt.title)

        #choose the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        #download stream to the specified path
        stream.download(output_path=save_path, filename=f"{video_title}.mp4")

    except Exception as e:
        print("An error occurred:", str(e))


#function to download the YouTube video as mp3 given the url and download path
def download_youtube_mp3(url, save_path):
    try:
        #create a YouTube object
        yt = YouTube(url)

        #get the video title
        video_title = clean_filename(yt.title)

        #choose the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        #download stream to the specified path
        stream.download(output_path=save_path, filename=f"{video_title}.mp3")
    except Exception as e:
        print("An error occurred:", str(e))


#function to download the YouTube video thumbnail given the url and download path
def download_youtube_thumbnail(url, save_path):
    try:
        #create YouTube object
        yt = YouTube(url)

        # get the video title
        thumbnail_filename = clean_filename(yt.title)

        #get highest resolution of thumbnail, maxresdefault
        thumbnail = Thumbnail(url)
        thumbnail.fetch(size="maxresdefault")
        
        #save thumbnail to the specified save path
        thumbnail.save(dir=save_path, filename=thumbnail_filename)

    except Exception as e:
        print("An error occurred:", str(e))
      
