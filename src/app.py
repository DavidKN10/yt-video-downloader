from tkinter import *
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Combobox
from pytube import YouTube
from pythumb import Thumbnail
from PIL import ImageTk,Image
import os
import subprocess


file_location = None    #variable for save path
url = None              #variable for url
save = None             #variable for option to save thumbnail
format = None           #variable for choosing a format


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
        messagebox.showinfo("Error", "ffmpeg command failed")


#function to download the YouTube video as mp4 given the url and download path
def download_youtube_mp4(url, save_path):
    try:
        #create a YouTube object
        yt = YouTube(url, on_progress_callback=on_progress)

        #get the video title
        video_title = clean_filename(yt.title)

        title_video_label = Label(frame2, text=f"Video Title: {video_title}", font=("", 10))
        title_video_label.grid(row=2, column=0)

        #choose the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        #download stream to the specified path
        stream.download(output_path=save_path, filename=f"{video_title}.mp4")

    except Exception as e:
        messagebox.showerror(title="Error",
                             message=f"Error: {e}")


# function to download the YouTube video as mp3 given the url and download path
def download_youtube_mp3(url, save_path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        video_title = clean_filename(yt.title)

        download_youtube_mp4(url, save_path)

        convertMP4ToMP3(f"{save_path}/{video_title}.mp4", f"{save_path}/{video_title}.mp3")

    except Exception as e:
        messagebox.showerror(title="Error",
                             message=f"Error: {e}")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_complete = (bytes_downloaded / total_size) * 100
    percent = str(int(percent_complete))
    percent_label.configure(text=percent+'%')
    percent_label.update()

    #update progress bar
    progress_bar['value'] = float(percent_complete)


# function to download the YouTube video thumbnail given the url and download path
def download_youtube_thumbnail(url, save_path):
    try:
        # create YouTube object
        yt = YouTube(url)

        # get the video title
        thumbnail_filename = clean_filename(yt.title)

        # get the highest resolution of thumbnail, maxresdefault
        thumbnail = Thumbnail(url)
        thumbnail.fetch(size="maxresdefault")

        # save thumbnail to the specified save path
        thumbnail.save(dir=save_path, filename=thumbnail_filename)

    except Exception as e:
        messagebox.showerror(title="Error",
                             message=f"Error: {e}")


#function that will work alongside the 'choose location' button
#will open a window, so you can choose where to save the video and thumbnail
def choose_location():
    global file_location
    file_location = filedialog.askdirectory()


#function that will work alongside the 'submit' button
def submit():
    #get url from the entry box and save it to url
    global url
    url = url_entry.get()

    #url to save the option that was chosen in the dropdown box
    #will save the option into the variable save
    global save
    save = check_button_combobox.get()

    global format
    format = format_button_combobox.get()

    #while loop to continue downloading if told to do so
    #follows similar logic as the while loop in yt2mp4_console.py
    while True:
        video_url = url
        save_path = file_location
        save_thumbnail = save
        video_format = format

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        download_youtube_thumbnail(url, save_path)
        yt = YouTube(url, on_progress_callback=on_progress)
        video_title = clean_filename(yt.title)

        canvas = Canvas(frame2, height=300, width=500)
        canvas.grid(row=1, column=0)
        img = Image.open(f"{save_path}/{video_title}.jpg").resize((500, 300))
        imgTK = ImageTk.PhotoImage(img)
        canvas.create_image(20, 20, anchor=NW, image=imgTK)

        # check if format is mp3 or mp4
        if video_format == "MP4":
            # call function to download video
            download_youtube_mp4(video_url, save_path)
        elif video_format == "MP3":
            # call function to download video
            download_youtube_mp3(video_url, save_path)
            os.remove(f"{save_path}/{video_title}.mp4")


        #When the video and thumbnail finish downloading, a message box will appear.
        #if you click yes, message box closes, and you can download another video
        #if you click no, message box closes and window closes as well
        answer = messagebox.askyesno(title = "Message",
                                     message="Done. Do you want to download another video?",
                                     icon='info')

        #if the option to save thumbnail was yes, save thumbnail
        if save_thumbnail == "No":
            os.remove(f"{save_path}/{video_title}.jpg")

        #if you click no, then close everything and end while loop
        #if you click yes, end while loop only
        if answer:
            progress_bar['value'] = 0
            percent_label.configure(text="0%")
            break
        else:
            window.quit()
            break


window = Tk()
#making the icon, window, and title
window.iconbitmap("V33983897_on_X.ico")
window.geometry('800x800')
window.minsize(800, 800)
window.maxsize(800,800)
window.title("YouTube Downloader by Noaxadd")

#labels at the top of window that give instructions
message = Label(window, text="Welcome!", font=("", 20))
message.place(x=350, y=0)
message = Label(window, text="Enter a YouTube video URL and the video will be saved to your local storage", font=("", 15))
message.place(x=60, y=30)

#Frame for video info
#this is the place where you will input all the information of the video
frame = Frame(window)
frame.place(x=100, y=70)
message_frame = LabelFrame(frame, text="Video Info", font=("", 15))
message_frame.grid(row=0, column=0)

#label for choosing location
test = Label(message_frame, text="Choose location to save video", font=("", 15))
test.grid(row=1, column=0)

#button that when clicked, it will open a window to choose a save location
test2=Button(message_frame, text="choose location", command=choose_location, font=("", 15))
test2.grid(row=1, column=1)

#label for entry box where you will type the url
url_label = Label(message_frame, text="Enter YouTube video URL", font=("", 15))
url_label.grid(row=0,column=0)

#entry box where you will type the url
url_entry = Entry(message_frame, font=("", 15), width=18)
url_entry.grid(row=0, column=1)

x = IntVar()

#label for saving the thumbnail option
check_button = Label(message_frame, text="Save Thumbnail?", font=("", 15))

#combobox that gives the option yes or no
check_button_combobox = Combobox(message_frame, values=["Yes", "No"])
check_button.grid(row=2, column=0)
check_button_combobox.grid(row=2, column=1)

#label for choosing format
format_button = Label(message_frame, text="Choose a Format", font=("", 15))

#combobox that lets you choose between mp3 or mp4
format_button_combobox = Combobox(message_frame, values=["MP3", "MP4"])
format_button.grid(row=3, column=0)
format_button_combobox.grid(row=3, column=1)

#button that when clicked, it will execute the 'submit' function and download the video
submit_button = Button(message_frame, text='submit', command=submit, font=("", 15))
submit_button.grid(row=3, column=2)

for widget in message_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

#new frame to add the progress bar and video title
frame2 = Frame(window)
frame2.place(x=150, y=275)
#message_frame2 = LabelFrame(frame2, text="Progress", font=("", 15))
#message_frame2.grid(row=0, column=0)

#to display the thumbnail on the window
#has a placeholder image before download
canvas = Canvas(frame2, height=300, width=500)
canvas.grid(row=1, column=0)
img = Image.open(f"V33983897_on_X.jpg").resize((460, 300))
imgTK = ImageTk.PhotoImage(img)
canvas.create_image(20, 20, anchor=NW, image=imgTK)

title_video = Label(frame2, text="", font=("", 10), justify="center")
title_video.grid(row=2, column=0)

percent_label = Label(frame2, text="0%", font=("", 15), justify="center")
percent_label.grid(row=3, column=0)

#progress bar
progress_bar = ttk.Progressbar(frame2, orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.grid(row=4, column=0, padx=10, pady=10)

window.mainloop()