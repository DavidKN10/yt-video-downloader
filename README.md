# YouTube Video Downloader

---

<p>
    <img src="markdown files/window.jpg">
</p>

### Overview

---

This program allows you to download the video and thumbnail of a YouTube video or playlist. The videos are downloaded to the highest queallity up to 1080p. 
This program uses Python and the  [pytubefix](https://pytubefix.readthedocs.io/en/latest/) and [pythumb](https://pypi.org/project/pythumb/) libraries to save the video and thumbnail. 

There is also a CLI version of the app.


### Features 

---

* download a YouTube video to the highest resolution up to 1080p
* option to download the thumbnail of the video
* download as either MP3 or MP4
* choose location of where you want to save the files
* download all videos on a playlist

### Prerequisites
---
Before you can use the GUI or CLI apps, you need to install ffmpeg.
<br>

1.) First, go to [Chocolatey](https://chocolatey.org/install) and follow the instructions to install it.
<br>
2.) Once you have Chocolatey installed, you can go to the console and type the following:
```shell
choco install ffmpeg-full
```
<br>
3.) You will be prompted to choose which scripts to run. Type "A" to run all. Let the installation finish. 
<br>

### How to Set Up GUI App

---

Once you have downloaded the zip file, decompress it and store it where ever you want. 
However, make sure to keep the files in the locations that they are in. Otherwise, you will encounter errors. 
You could make a shortcut of the .exe file and move that shortcut outside the folder if you want.
<br>

If you followed the prerequisites, you should be able to use the applications now. 

### How to Set Up Command Line Program

---

Download "yt_downloader_cli.py"

Make sure you also have [python](https://www.python.org/downloads/), pytubefix, and pythumb installed.

Instructions to download pythumb and pytube:

```shell
pip install pytubefix
```

```shell
pip install pythumb
```

Once you have everything installed, open the command line. Once there, 
change to the directory of where the "yt_downloader_cli.py" is saved.

```shell
cd (location where yt_downloader_cli.py is saved)
```

Now open the python file in the command line using Python:
```shell
python yt_downloader_cli.py
```

### How to Use the GUI App

---

#### Videos

In the entry box next to "Enter YouTube video URL", place the URL to the video.
On the button that says "choose location", a window will open,
and you can go to the folder where you want to save the video. 
Next to "Save Thumbnail?" you will see a dropdown menu that will give you the options
"Yes" and "No". If "Yes" is chosen, the thumbnail will be saved on the same location 
where you are saving the video. If "No" is chosen, the thumbnail will not be saved. 
Now, in the "Choose a Format" dropdown menu, you can choose between MP3 or MP4 and the video will be saved in the chosen format. 

<p>
    <img src="markdown files/window.jpg">
</p>

When you click on "submit", the video and thumbnail will start downloading.

Once the video downloads, you will get the following window:

<p>
    <img src="markdown files/message box.jpg">
</p>


If you click "Yes", the message window will close and you can continue downloading more videos.
If you click "No", the message box will close and you will exit the program.

#### Playlists



### How to Use the Command Line Program

---

You will first be prompted to enter the URL of the video:
```shell
Enter the YouTube video URL: 
```
Copy and paste the URL and hit enter. 
Now you will be prompted to enter the directory to save the file.
```shell
Enter the YouTube video URL: 
Enter the path to save the video: 
```
After entering the location, you will be asked if you want to save the thumbnail.
If you type "Y" or "y", the thumbnail will be saved. You can type anything else to decline. 
```shell
Enter the YouTube video URL: 
Enter the path to save the video: 
Do you want to save the thumbnail? (Y/N):
```
After choosing to save the thumbnail or not, you will be prompted to enter the format you
want to download the video as. Type "mp3" for mp3 or "mp4" for mp4.
```shell
Enter the YouTube video URL: 
Enter the path to save the video: 
Do you want to save the thumbnail? (Y/N):
Enter the video format(mp4/mp3): 
```
After entering yor option, the console will print out the name of the video with invalid characters removed. 
Then the console will tell you if the video and thumbnail were downloaded successfully. 
If the video did not download successfully, it will tell you what error it encountered. 
```shell
Enter the YouTube video URL: 
Enter the video format(mp4/mp3): 
Enter the path to save the video: 
Do you want to save the thumbnail? (Y/N):
Video Title: (title will be printed here)
Video downloaded successfully! Saved as '(name of video)'
Thumbnail downloaded successfully! Saved as '(name of image)'
```

After the video downloads, you will prompted to choose whether you want to download another video or not.
If you type "y", you will prompted to enter the URL and follow the same steps again. If you type "n", the 
program will exit. 
```shell
Enter the YouTube video URL: (URL goes here)
Enter the video format(mp4/mp3): (format goes here)
Enter the path to save the video: (path goes here)
Do you want to save the thumbnail? (Y/N):
Video Title: (title will be printed here)
Video downloaded successfully! Saved as '(name of video)'
Thumbnail downloaded successfully! Saved as '(name of image)'

Do you want to download another video? (Y/N):
```