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


window = Tk()
window.iconbitmap("V33983897_on_X.ico")
window.geometry('530x500')
window.minsize(530, 300)
window.maxsize(530,300)
window.title("YouTube to mp4 by Noaxadd")

message = Label(window, text="Welcome!")
message.place(x=5, y=0)

message = Label(window, text="Enter a YouTube video URL and the video will be saved to your local storage")
message.place(x=5, y=30)

frame = Frame(window)
frame.place(x=55, y=70)
message_frame = LabelFrame(frame, text="Video Info")
message_frame.grid(row=0, column=0)

test = Label(message_frame, text="Choose location to save video")
test.grid(row=1, column=0)

test2=Button(message_frame, text="choose location", command=choose_location)
test2.grid(row=1, column=1)

url_label = Label(message_frame, text="Enter YouTube video URL")
url_label.grid(row=0,column=0)

url_entry = Entry(message_frame)
url_entry.grid(row=0, column=1)

x = IntVar()
check_button = Label(message_frame, text="Save Thumbnail?")
check_button_combobox = Combobox(message_frame, values=["Yes", "No"])
check_button.grid(row=2, column=0)
check_button_combobox.grid(row=2, column=1)

submit_button = Button(message_frame, text='submit', command=submit)
submit_button.grid(row=3, column=2)

for widget in message_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

window.mainloop()
