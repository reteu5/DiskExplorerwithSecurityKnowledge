from tkinter import *
import os
import ctypes
import pathlib
from SMART import *



# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
# set a title
root.title('Simple Explorer')

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

# set a window
root.geometry("640x400+100+100")
root.resizable(True, True)


#smart
device_name_list = get_device_name()
device = []

for dev in device_name_list:
    device.append(Device(dev))


def dirChange(index):
    dir_att, dir_val = device[index].get_device_info()

    attributes.delete(0, END)
    values.delete(0, END)

    cur = 0
    for item in dir_att:
        attributes.insert(cur, item)
        cur += 1
    
    cur = 0
    for item in dir_val:
        values.insert(cur,item)
        cur += 1

def changeDirToC(event=None):
    # Get clicked item.
    dirChange(0)

def changeDirToD(event=None):
    # Get clicked item.
    dirChange(1)


    
Button(root, text=device_name_list[0], command=changeDirToC).grid(
    sticky='NSEW', column=0, row=0
)

Button(root, text=device_name_list[1], command=changeDirToD).grid(
    sticky='NSEW', column=1, row=0
)

# match (attribute - value)
attributes=Listbox(root)
attributes.grid(sticky='NSEW', column=0, row=1, ipady=10, ipadx=10)

values=Listbox(root)
values.grid(sticky='NSEW', column=1, row=1, ipady=10, ipadx=10)




# Call the function so the list displays
dirChange(0)

# run the main program
root.mainloop()