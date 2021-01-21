# -------------------------------------------------------------IMPORTING_MODULES---------------------------------------------------------
import os                                           # to interact with operating system
import threading                                    # to syncronise threads
import time                                         # to use time
import tkinter.messagebox                           # for messagebox
from tkinter import *                               # to create graphical user interface (GUI)
from tkinter import ttk                             # theam tkinter
from ttkthemes import themed_tk as tk               # for themes
from tkinter import filedialog                      # To browse the file
from mutagen.mp3 import MP3                         # to handel mp3 formte
from pygame import mixer                            # to handel music

#-----------------------------------------------------------------ROOT_WINDOW-------------------------------------------------------------

#root = Tk() # creating window (simple window without any theme)
root = tk.ThemedTk() # creating themed window
root.get_themes() # getting themes
root.set_theme('radiance') # applying theme
root.title("MyTunes")
root.iconbitmap(r'images/icon.ico')

#------------------------------------------------------------------VARIABLE----------------------------------------------------------------

v =DoubleVar()# for getting current volume
playlist=[] # playlist contanins filename with path

#----------------------------------------------------------------STSTUS_BAR------------------------------------------------------------------

statusbar = ttk.Label(root, text="Welcome to Melody",background='cyan4',foreground='white',relief=SUNKEN, anchor=W,font='courier 15 italic')
statusbar.pack(side=BOTTOM, fill=X)

#-----------------------------------------------------------------MENU_BAR-----------------------------------------------------------------
menubar = Menu(root)
root.config(menu=menubar)

subMenu = Menu(menubar, tearoff=0) # Create the submenu

#---------------------------------------------------------------BROWSE_FILE--------------------------------------------------------------
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
#-------------------------------------------------------------ADD_TO_PLAYLIST--------------------------------------------------------------
def add_to_playlist(filename):
    filename=os.path.basename(filename)
    index=0
    playlistbox.insert(index, filename)
    playlistbox.pack()
    playlist.insert(index,filename_path)
    index +=1

#--------------------------------------------------------------ADDING_CASCADE---------------------------------------------------------------
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
# root.destory is used to destorry
subMenu.add_command(label="Exit", command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About MyTune', 'This is a music player build using Python Tkinter by gauravk2050')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

#----------------------------------------------------------------LEFT_FRAME---------------------------------------------------------------------

leftframe= Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

toplf=Frame(leftframe)
toplf.pack()

#----------------------------------------------------------------PLAYLIST------------------------------------------------------------------------

playlistbox = Listbox(toplf,selectbackground='deepskyblue2',selectmode=EXTENDED,font=("times new roman",12,"bold"),bg="gray80",fg="black",bd=5,relief=GROOVE)
playlistbox.pack(fill = BOTH)
songtracks = os.listdir("C:/Users/GAURAV/Downloads/Music")
i=0
for track in songtracks:
        fp="C:/Users/GAURAV/Downloads/Music/"+track
        playlistbox.insert(END,track)
        playlist.insert(i, fp)
        i += 1

bottomlf=Frame(leftframe)
bottomlf.pack()

addbtn=ttk.Button(toplf,text='  Add  ',command=browse_file)
addbtn.pack(side=LEFT)

#----------------------------------------------------------------DELETE_SONG------------------------------------------------------------------------

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

deletebtn = ttk.Button(toplf,text=' Remove ',command=del_song)
deletebtn.pack(side=LEFT)

#--------------------------------------------------------------PLAY_PREVIOUS_SONG--------------------------------------------------------------------
def previous():
    global z
    z = z - 1
    try:
        stop_music()
        time.sleep(1)
        play_it = playlist[z]
        mixer.music.load(play_it)
        mixer.music.play()
        statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
        show_details(play_it)
    except:
        tkinter.messagebox.showerror('File not found', 'MyTunes could not find the file. Please check again.')

prevphoto=PhotoImage(file='images/previous.png')
previous=ttk.Button(bottomlf,image=prevphoto,command=previous)
previous.pack(side=LEFT,pady=10)

all=PhotoImage()

#----------------------------------------------------------------PLAY_NEXT_SONG--------------------------------------------------------------------
def next():
    global z
    z = z + 1
    try:
        stop_music()
        time.sleep(1)
        play_it = playlist[z]
        mixer.music.load(play_it)
        mixer.music.play()
        statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
        show_details(play_it)
    except:
        tkinter.messagebox.showerror('File not found', 'MyTunes could not find the file. Please check again.')

nextphoto=PhotoImage(file='images/next.png')
next=ttk.Button(bottomlf,image=nextphoto,command=next)
next.pack(side=LEFT,pady=10)
#------------------------------------------------------------------RIGHT_FRAME--------------------------------------------------------------------
rightframe= Frame(root)
rightframe.pack(padx=20,pady=30)

topframe=Frame(rightframe)
topframe.pack()
# length of file
lengthlabel = ttk.Label(topframe, text='Total Length : --:--',font='verdana 10 bold')
lengthlabel.pack(pady=5)

# current time
currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()

#--------------------------------------------------------------PREVIEW_SONG_DETAILS--------------------------------------------------------------------
def show_details(play_song):
    # check file formate i.e mp3 or wav or any other
    file_data = os.path.splitext(play_song)
    # it gives list in which 1st elemet is path and second element is format

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length  # getting length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()  # getting length

    # divemod divide total length by 60 and calculate remainder into in secs and quotient into min
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    # creating thread so that program will not be busy only in loop
    # program can perform multiple task at a same time
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

#--------------------------------------------------------------COUNT_SONG_DURATION--------------------------------------------------------------------
def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    # current_time = 0 # increasing type formate
    # while current_time <= t and mixer.music.get_busy():
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            # mins, secs = divmod(current_time, 60)
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            # current_time += 1
            t -= 1
#-------------------------------------------------------------------PLAY_SONG--------------------------------------------------------------------
def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            global z
            stop_music()
            time.sleep(1) # given buffer time to 1 sec because our thread need 1sec buffer time
            selected_song = playlistbox.curselection()#give the selected file
            # selectd_song gives the list value so conver into integer
            # the latest file is added is always go to 0th index
            selected_song=int(selected_song[0]) # now we use this index to det the actually full file path from playlist
            z=selected_song
            play_it=playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Mytune could not find the file. Please check again.')

#----------------------------------------------------------------------STOP_SONG--------------------------------------------------------------------
def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

#----------------------------------------------------------------------PAUSE_SONG--------------------------------------------------------------------
paused = FALSE
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

#----------------------------------------------------------------------REWIND_SONG--------------------------------------------------------------------
def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

#-----------------------------------------------------------------------SONG_VOLUME--------------------------------------------------------------------
def set_vol(val):
    # val have string value so we need to convert it
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # it is devided by 100 because set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1

#----------------------------------------------------------------------MUTE_SONG--------------------------------------------------------------------
muted = FALSE
def mute_music():
    global muted
    global x
    if muted:  # Unmute the music
        y = x / 100
        mixer.music.set_volume(y)
        volumeBtn.configure(image=volumePhoto)
        scale.set(x)
        muted = FALSE
    else:  # mute the music
        x = v.get()
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


# pady = y-axis , padx = x-axis
middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

#---------------------------------------------------------BUTTONS_IN_RIGHT_FRAME-------------------------------------------------------------
# play button
playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

# stop button
stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

# pause button
pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.
bottomframe = Frame(rightframe)
bottomframe.pack()

# rewind button
rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0,padx=3)

# mute, volume button
mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/audio.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1,padx=3)

# volume scale
scale = ttk.Scale(bottomframe, from_=0, to=100,variable=v,orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=10)

#-------------------------------------------------------------CLOSING_APP----------------------------------------------------------------
def on_closing():
    stop_music() # closing music
    # closng window
    root.destroy()

# protocol - a way of communication
#WM_DELETE_WINDOW refers to red cross button on top right of window
root.protocol('WM_DELETE_WINDOW',on_closing)# calling on_closing

root.mainloop()
