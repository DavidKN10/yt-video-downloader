from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from yt_to_mp4 import *
import os

file_location = None    #variable for save path
url = None              #variable for url
save = None             #variable for option to save thumbnail

#function that will work alongside the 'choose location' button
#will open a window, so you can choose where to save the video and thumbnail
def choose_location():
    global file_location
    file_location = filedialog.askdirectory()


#function that will work alongside the 'submit' button
def submit():
    #get url from the entry box and save it to url    
    url = url_entry.get()

    #url to save the option that was chosen in the dropdown box
    #will save the option into the variable save    
    save = check_button_combobox.get()

    #while loop to continue downloading if told to do so
    #follows similar logic as the while loop in yt2mp4_console.py
    while True:
        video_url = url
        save_path = file_location
        save_thumbnail = save

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        #call the function from yt_to_mpy.py to download video
        download_youtube_video(video_url, save_path)

        #if the option to save thumbnail was yes, save thumbnail
        if save_thumbnail == "Yes":
            download_youtube_thumbnail(video_url, save_path)

        #When the video and thumbnail finish downloading, a message box will appear.
        #if you click yes, message box closes, and you can download another video
        #if you click no, message box closes and window closes as well
        answer = messagebox.askyesno(title = "Message",
                                     message="Done. Do you want to download another video?",
                                     icon='info')

        #if you click no, then close everything and end while loop
        if not answer:
            window.quit()
            break

        #if you click yes, end while loop only
        if answer:
            break


window = Tk()
#making the icon, window, and title
window.iconbitmap("V33983897_on_X.ico")
window.geometry('530x500')
window.minsize(530, 300)
window.maxsize(530,300)
window.title("YouTube to mp4 by Noaxadd")

#labels at the top of window that give instructions
message = Label(window, text="Welcome!")
message.place(x=5, y=0)
message = Label(window, text="Enter a YouTube video URL and the video will be saved to your local storage")
message.place(x=5, y=30)

#Frame for video info
#this is the place where you will input all the information of the video
frame = Frame(window)
frame.place(x=55, y=70)
message_frame = LabelFrame(frame, text="Video Info")
message_frame.grid(row=0, column=0)

#label for choosing location
test = Label(message_frame, text="Choose location to save video")
test.grid(row=1, column=0)

#button that when clicked, it will open a window to choose a save location
test2=Button(message_frame, text="choose location", command=choose_location)
test2.grid(row=1, column=1)

#label for entry box where you will type the url
url_label = Label(message_frame, text="Enter YouTube video URL")
url_label.grid(row=0,column=0)

#entry box where you will type the url
url_entry = Entry(message_frame)
url_entry.grid(row=0, column=1)

x = IntVar()

#label for saving the thumbnail option
check_button = Label(message_frame, text="Save Thumbnail?")

#combobox that gives the option yes or no
check_button_combobox = Combobox(message_frame, values=["Yes", "No"])
check_button.grid(row=2, column=0)
check_button_combobox.grid(row=2, column=1)

#button that when clicked, it will execute the 'submit' function and download the video
submit_button = Button(message_frame, text='submit', command=submit)
submit_button.grid(row=3, column=2)

for widget in message_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

window.mainloop()
