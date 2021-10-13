import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
from ttkthemes import themed_tk as tk
import time
import threading
from mutagen.mp3 import MP3

from pygame import mixer

mixer.init()

root= tk.ThemedTk()
root.get_themes()
root.set_theme("clearlooks")

statusbar=ttk.Label(root,text="Welcome", relief=SUNKEN, anchor=W, font="Time 10 italic")
statusbar.pack(side=BOTTOM, fill=X)

menubar=Menu(root)
root.config(menu=menubar)


subMenu=Menu(menubar, tearoff=0)

playlist=[] # contains path name

def browse_file():
    global filename_path
    filename_path=filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename=os.path.basename(filename)
    index=0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    playlistbox.pack()
    index=index+1
    

menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open", command= browse_file)
subMenu.add_command(label="Exit", command= root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About SkyBeat','tkinter based project')

subMenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us", command= about_us)

root.geometry('300x300')
root.title("SkyBeat")
root.iconbitmap(r'C:/Users/antar/Downloads/hnet.com-image.ico')

leftframe= Frame(root)
leftframe.pack(side=LEFT,padx=30, pady=30)

playlistbox=Listbox(leftframe)
playlistbox.pack()

addBtn=ttk.Button(leftframe,text="ADD", command=browse_file)
addBtn.pack(side=LEFT)

def del_song():
    selected_song=playlistbox.curselection()
    selected_song=int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn= ttk.Button(leftframe,text="DELETE", command=del_song)
delBtn.pack()



rightframe=Frame(root)
rightframe.pack()

topframe=Frame(rightframe)
topframe.pack()

lengthLabel=ttk.Label(topframe,text='Total Length:  --:--')
lengthLabel.pack(pady=5)

currenttimeLabel=ttk.Label(topframe,text='Current time:  --:--', relief= GROOVE)
currenttimeLabel.pack()





def show_details(play_song):
    

    file_data=os.path.splitext(play_song)
    #print(file_data)

    if file_data[1]=='.mp3':
        #mp3
        audio= MP3(play_song)
        
        total_length=audio.info.length
    else:
        a= mixer.Sound(play_song)
        
        total_length=a.get_length()




    
    mins,secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    lengthLabel['text']="Total Length " + " - "+ timeformat

    t1=threading.Thread(target= start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs=divmod(current_time,60)
            mins=round(mins)
            secs=round(secs)
            timeformat='{:02d}:{:02d}'.format(mins,secs)
            currenttimeLabel['text']='Current time'+ '-'+ timeformat
            time.sleep(1)
            
            current_time= current_time+1
           
            
    

def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text']="Resumed"
        paused=FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song=playlistbox.curselection()
            selected_song=int(selected_song[0])
            play_it=playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text']="Playing Music " + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Please select file')
            #print("Error")

    
        
        
        
    
    
def stop_music():
    mixer.music.stop()
    statusbar['text']="Stopping Music"
    
paused=FALSE
def pause_music():
    global paused
    paused=True
    mixer.music.pause()
    statusbar['text']="Paused"

def rewind_music():
    play_music()
    statusbar['text']="Rewind"


muted=FALSE
def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumebtn.configure(image=volume)
        scale.set(70)
        muted=FALSE
    else:
        mixer.music.set_volume(0)
        volumebtn.configure(image=mute)
        scale.set(0)
        muted=TRUE
        
    
    
def set_vol(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)
    
    
middleframe=Frame(rightframe)
middleframe.pack(padx=30,pady=30)

photo=PhotoImage(file='C:/Users/antar/Downloads/play-button.png')
btn=ttk.Button(middleframe,image=photo, command=play_music)
btn.grid(row=0,column=0, padx=10)

stop=PhotoImage(file='C:/Users/antar/Downloads/stop-button.png')
stopbtn=ttk.Button(middleframe,image=stop, command=stop_music)
stopbtn.grid(row=0,column=1,padx=10)

pause=PhotoImage(file='C:/Users/antar/Downloads/pause.png')  
pausebtn=ttk.Button(middleframe,image=pause, command=pause_music)
pausebtn.grid(row=0,column=2,padx=10)

bottomframe=Frame(rightframe)
bottomframe.pack()

rewind=PhotoImage(file='C:/Users/antar/Downloads/rewind.png')  
rewindbtn=ttk.Button(bottomframe,image=rewind, command=rewind_music)
rewindbtn.grid(row=0,column=0)


mute=PhotoImage(file='C:/Users/antar/Downloads/mute.png')
volume=PhotoImage(file='C:/Users/antar/Downloads/speaker.png') 
volumebtn=ttk.Button(bottomframe,image=volume, command=mute_music)
volumebtn.grid(row=0,column=1)


scale=ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0,column=2,pady=15,padx=30)




def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_WINDOW_DELETE",on_closing)
root.mainloop()