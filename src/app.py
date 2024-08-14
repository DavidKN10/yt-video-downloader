from tkinter import *
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Combobox
from pytubefix import YouTube
from pythumb import Thumbnail
from PIL import ImageTk, Image
import os
import subprocess

file_location = None
url = None
save = None
format = None


def clean_filename(filename):
    invalid_chars = r'\/:*?<>|"'
    invalid_characters = set(invalid_chars)

    cleaned_text = ''.join(['_' if char in invalid_characters else char for char in filename])

    return cleaned_text


def download_mp4(url, path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)

        video_title = clean_filename(yt.title)

        global title_video
        title_video.config(text=f"{video_title}")

        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=path, filename=f"{video_title}.mp4")

    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error: {e}")


def download_mp3(url, path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)

        video_title = clean_filename(yt.title)

        global title_video
        title_video.config(text=f"{video_title}")

        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=path, filename=f"{video_title}.mp3", mp3=True)

    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error: {e}")


def download_thumbnail(url, path):
    try:
        yt = YouTube(url)

        thumbnail_filename = clean_filename(yt.title)

        thumbnail = Thumbnail(url)
        thumbnail.fetch(size="maxresdefault")

        thumbnail.save(dir=path, filename=thumbnail_filename)

    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error: {e}")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_complete = (bytes_downloaded / total_size) * 100
    percent = str(int(percent_complete))
    percent_label.configure(text=percent + '%')
    percent_label.update()
    progress_bar['value'] = float(percent_complete)


def choose_location():
    global file_location
    file_location = filedialog.askdirectory()


def submit():
    global url
    url = url_entry.get()

    global save
    save = check_button_combobox.get()

    global format
    format = format_button_combobox.get()

    while True:
        video_url = url
        save_path = file_location
        save_thumbnail = save
        video_format = format

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        download_thumbnail(url, save_path)
        yt = YouTube(url, on_progress_callback=on_progress)
        video_title = clean_filename(yt.title)

        canvas = Canvas(frame2, height=300, width=500)
        canvas.grid(row=1, column=0)
        img = Image.open(f"{save_path}/{video_title}.jpg").resize((500, 300))
        imgTK = ImageTk.PhotoImage(img)
        canvas.create_image(20, 20, anchor=NW, image=imgTK)

        if video_format == "MP4":
            download_mp4(video_url, save_path)
        elif video_format == "MP3":
            download_mp3(video_url, save_path)

        answer = messagebox.askyesno(title="Message",
                                     message="Done. Do you want to download another video?",
                                     icon='info')

        if save_thumbnail == "No":
            os.remove(f"{save_path}/{video_title}.jpg")

        if answer:
            progress_bar['value'] = 0
            percent_label.configure(text="0%")

            global title_video
            title_video.config(text="")
            break
        else:
            window.quit()
            break


window = Tk()
window.iconbitmap("V33983897_on_X.ico")
window.geometry('800x800')
window.minsize(800, 800)
window.maxsize(800, 800)
window.title("YouTube Downloader by Noaxadd")

message = Label(window, text="Welcome!", font=("", 20))
message.place(x=350, y=0)
message = Label(window, text="Enter a YouTube video URL and the video will be saved to your local storage",
                font=("", 15))
message.place(x=60, y=30)

frame = Frame(window)
frame.place(x=100, y=70)
message_frame = LabelFrame(frame, text="Video Info", font=("", 15))
message_frame.grid(row=0, column=0)

location_label = Label(message_frame, text="Choose location to save video", font=("", 15))
location_label.grid(row=1, column=0)

location_button = Button(message_frame, text="choose location", command=choose_location, font=("", 15))
location_button.grid(row=1, column=1)

url_label = Label(message_frame, text="Enter YouTube video URL", font=("", 15))
url_label.grid(row=0, column=0)

url_entry = Entry(message_frame, font=("", 15), width=18)
url_entry.grid(row=0, column=1)

x = IntVar()

check_button = Label(message_frame, text="Save Thumbnail?", font=("", 15))

check_button_combobox = Combobox(message_frame, values=["Yes", "No"])
check_button.grid(row=2, column=0)
check_button_combobox.grid(row=2, column=1)

format_button = Label(message_frame, text="Choose a Format", font=("", 15))

format_button_combobox = Combobox(message_frame, values=["MP3", "MP4"])
format_button.grid(row=3, column=0)
format_button_combobox.grid(row=3, column=1)

submit_button = Button(message_frame, text='submit', command=submit, font=("", 15))
submit_button.grid(row=3, column=2)

for widget in message_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

frame2 = Frame(window)
frame2.place(x=150, y=275)

canvas = Canvas(frame2, height=300, width=500)
canvas.grid(row=1, column=0)
img = Image.open(f"V33983897_on_X.jpg").resize((460, 300))
imgTK = ImageTk.PhotoImage(img)
canvas.create_image(20, 20, anchor=NW, image=imgTK)

title_video = Label(frame2, text="", font=("", 10), justify="center")
title_video.grid(row=2, column=0)

percent_label = Label(frame2, text="0%", font=("", 15), justify="center")
percent_label.grid(row=3, column=0)

# progress bar
progress_bar = ttk.Progressbar(frame2, orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.grid(row=4, column=0, padx=10, pady=10)

window.mainloop()
