from tkinter import *
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Combobox
from pytubefix import YouTube, Playlist
from pythumb import Thumbnail
from PIL import ImageTk, Image
import os


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


def download_playlist(url, path):
    try:
        playlist = Playlist(url)

        global download_progress

        for video in playlist.videos:
            download_progress.config(text=f"Downloading: {video.title}")
            video_title = clean_filename(video.title)
            stream = video.streams.get_highest_resolution()
            stream.download(output_path=path, filename=f"{video_title}.mp4")

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


def submit_video():
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


def submit_playlist():
    global url
    url = p_url_entry.get()

    while True:
        playlist_url = url
        save_path = file_location

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        download_playlist(playlist_url, save_path)

        answer = messagebox.askyesno(title="Message",
                                     message="Done. Do you want to download something else?",
                                     icon='info')

        if answer:
            download_progress.config(text="")
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

notebook = ttk.Notebook(window)
video_tab = Frame(notebook)
playlist_tab = Frame(notebook)
notebook.add(video_tab, text="Videos")
notebook.add(playlist_tab, text="Playlists")
notebook.pack(fill=BOTH, expand=YES)



# ==================== Video tab ====================
message = Label(video_tab, text="Welcome!", font=("", 20))
message.place(x=350, y=0)
message = Label(video_tab, text="Enter a YouTube video URL and the video will be saved to your local storage",
                font=("", 15))
message.place(x=60, y=30)

frame = Frame(video_tab)
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

submit_button = Button(message_frame, text='submit', command=submit_video, font=("", 15))
submit_button.grid(row=3, column=2)

for widget in message_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

frame2 = Frame(video_tab)
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



# ==================== Playlist tab ====================
p_message = Label(playlist_tab, text="Enter playlist URL and the videos will be saved",
                  font=("",15))
p_message.place(x=60, y=30)

p_frame = Frame(playlist_tab)
p_frame.place(x=90, y=70)
p_message_frame = LabelFrame(p_frame, text="Playlist Info", font=("", 15))
p_message_frame.grid(row=0, column=0)

p_url_label = Label(p_message_frame, text="Enter Playlist URL", font=("",15))
p_url_label.grid(row=0, column=0)
p_url_entry = Entry(p_message_frame, font=("", 15), width=18)
p_url_entry.grid(row=0, column=1)

p_location_label = Label(p_message_frame, text="Choose location to save playlist", font=("",15))
p_location_label.grid(row=1, column=0)
p_location_button = Button(p_message_frame, text="choose location", command=choose_location, font=("",15))
p_location_button.grid(row=1, column=1)

p_submit_button = Button(p_message_frame, text='submit', command=submit_playlist, font=("", 15))
p_submit_button.grid(row=1, column=2)

for widget in p_message_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

p_frame2 = Frame(playlist_tab)
p_frame2.place(x=100, y=275)

download_progress = Label(p_frame2, text="", font=("", 15), justify="center")
download_progress.grid(row=1, column=0)

window.mainloop()
