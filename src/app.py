from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from yt_to_mp4 import *
import os

file_location = None
url = None
save = None

def choose_location():
    global file_location
    file_location = filedialog.askdirectory()

def submit():
    url = url_entry.get()
    save = check_button_combobox.get()

    while True:
        video_url = url
        save_path = file_location
        save_thumbnail = save

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        download_youtube_video(video_url, save_path)

        if save_thumbnail == "Yes":
            download_youtube_thumbnail(video_url, save_path)

        answer = messagebox.askyesno(title = "Message",
                                     message="Done. Do you want to download another video?",
                                     icon='info')
        if not answer:
            window.quit()
            break
        if answer:
            break

