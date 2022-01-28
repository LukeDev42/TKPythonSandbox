#Import tkinter library
from tkinter import *
from tkcalendar import Calendar, DateEntry
#Create an instance of tkinter frame
win= Tk()
#Set the Geometry
win.geometry("750x250")
win.title("Date Picker")
#Create a Label
Label(win, text= "Choose a Date", background= 'gray61', foreground="white").pack(padx=20,pady=20)
#Create a Calendar using DateEntry
cal = DateEntry(win, width= 16, background= "magenta3", foreground= "white",bd=2)
cal.pack(pady=20)
win.mainloop()