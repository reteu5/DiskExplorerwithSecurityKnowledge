from tkinter import *
import os
import ctypes
import pathlib
import stat
from SMART import *
from tkinter.font import *



# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
# set a title
root.title('Simple Explorer')

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

# set a window
root.geometry("2760x720+100+100")           # 1280x800+100+100
root.resizable(True, True)


#smart
device_name_list = get_device_name()
device = []

for dev in device_name_list:
    device.append(Device(dev))

def changeDirToC(event=None):
    disk.set("C:")
    model_num.set(device[0].get_device_info("Model Number"))
    serial_num.set(device[0].get_device_info("Serial Number"))
    firm_ver.set(device[0].get_device_info("Firmware Version"))
    nvme_ver.set(device[0].get_device_info("NVMe Version"))
    temper.set(device[0].get_device_info("Temperature"))
    total_cap.set(device[0].get_device_info("Total NVM Capacity"))
    util_cap.set(device[0].get_device_info("Namespace 1 Utilization"))
    data_read.set(device[0].get_device_info("Data Units Read"))
    data_write.set(device[0].get_device_info("Data Units Written"))
    power_hours.set(device[0].get_device_info("Power On Hours"))
    cycles.set(device[0].get_device_info("Power Cycles"))



def changeDirToD(event=None):
    disk.set("D:")
    model_num.set(device[1].get_device_info("Device Model"))
    serial_num.set(device[1].get_device_info("Serial Number"))
    firm_ver.set(device[1].get_device_info("Firmware Version"))
    nvme_ver.set(device[1].get_device_info("NVMe Version"))
    temper.set(device[1].get_device_info("Temperature"))
    total_cap.set(device[1].get_device_info("Total NVM Capacity"))
    util_cap.set(device[1].get_device_info("Namespace 1 Utilization"))
    data_read.set(device[1].get_device_info("Data Units Read"))
    data_write.set(device[1].get_device_info("Data Units Written"))
    power_hours.set(device[1].get_device_info("Power On Hours"))
    cycles.set(device[1].get_device_info("Power Cycles"))

def close():
    root.quit()
    root.destroy()

menubar=Menu(root)


# match (attribute - value)
disk = StringVar(
    root,
    name='disk',
    value="C:"
)
model_num = StringVar(
    root,
    name='model_num',
    value="None"
)
serial_num = StringVar(
    root,
    name='serial_num',
    value="None"
)
firm_ver = StringVar(
    root,
    name='firm_version',
    value="None"
)
nvme_ver = StringVar(
    root,
    name='nvme_ver',
    value="None"
)
temper = StringVar(
    root,
    name='temper',
    value="None"
)
total_cap = StringVar(
    root,
    name='total_cap',
    value="None"
)
util_cap = StringVar(
    root,
    name='util_cap',
    value="None"
)
data_read = StringVar(
    root,
    name='data_read',
    value="None"
)
data_write = StringVar(
    root,
    name='data_write',
    value="None"
)
power_hours = StringVar(
    root,
    name='power_hours',
    value="None"
)
cycles = StringVar(
    root,
    name='cycles',
    value="None"
)

font_title = Font(family="나눔 고딕",size = 20,weight='bold')
title_frame = Frame(root, relief='solid', width = 400, height = 20)
title_frame.grid(column=0, row=0)
main_frame = Frame(root, relief='solid', width = 400, height = 300)
main_frame.grid(column=0, row=1)
explorer_frame = Frame(root, relief='solid', width = 100, height = 300, bg="Yellow")
explorer_frame.grid(column=1, row=0, rowspan=2)


label1=Label(title_frame, textvariable=disk, font=font_title, anchor="e")
label1.grid(column=0, row=0)
var1=Label(title_frame, textvariable=model_num, font=font_title, anchor="w")
var1.grid(column=1, row=0)

label2=Label(main_frame, text="일련번호 (S/N)", anchor="e")
label2.grid(column=0, row=2, sticky="e")
var2=Label(main_frame, textvariable=serial_num, width = 20, anchor="w", bg="white")
var2.grid(column=1, row=2)

label3=Label(main_frame, text="펌웨어 버전 정보", anchor="e")
label3.grid(column=0, row=3, sticky="e")
var3=Label(main_frame, textvariable=firm_ver, width = 20, anchor="w", bg="white")
var3.grid(column=1, row=3)

label4=Label(main_frame, text="NVMe 버젼", anchor="e")
label4.grid(column=0, row=4, sticky="e")
var4=Label(main_frame, textvariable=nvme_ver, width = 20, anchor="w", bg="white")
var4.grid(column=1, row=4)

label5=Label(main_frame, text="온도", anchor="e")
label5.grid(column=0, row=5, sticky="e")
var5=Label(main_frame, textvariable=temper, width = 20, anchor="w", bg="white")
var5.grid(column=1, row=5)

label6=Label(main_frame, text="총 저장공간", anchor="e")
label6.grid(column=0, row=6, sticky="e")
var6=Label(main_frame, textvariable=total_cap, width = 20, anchor="w", bg="white")
var6.grid(column=1, row=6)

label7=Label(main_frame, text="점유중인 저장공간", anchor="e")
label7.grid(column=0, row=7, sticky="e")
var7=Label(main_frame, textvariable=util_cap, width = 20, anchor="w", bg="white")
var7.grid(column=1, row=7)

label8=Label(main_frame, text="총 읽기량", anchor="e")
label8.grid(column=0, row=8, sticky="e")
var8=Label(main_frame, textvariable=data_read, width = 20, anchor="w", bg="white")
var8.grid(column=1, row=8)

label9=Label(main_frame, text="총 쓰기량", anchor="e")
label9.grid(column=0, row=9, sticky="e")
var9=Label(main_frame, textvariable=data_write, width = 20, anchor="w", bg="white")
var9.grid(column=1, row=9)

label10=Label(main_frame, text="가동 시간", anchor="e")
label10.grid(column=0, row=10, sticky="e")
var10=Label(main_frame, textvariable=power_hours, width = 20, anchor="w", bg="white")
var10.grid(column=1, row=10)

label11=Label(main_frame, text="사용 횟수", anchor="e")
label11.grid(column=0, row=11, sticky="e")
var11=Label(main_frame, textvariable=cycles, width = 20, anchor="w", bg="white")
var11.grid(column=1, row=11)



# file explorer

def pathChange(*event):
    # Get all Files and Folders from the given Directory
    directory = os.listdir(currentPath.get())
    # Clearing the list
    list.delete(0, END)
    # Inserting the files and directories into the list         읽어온 파일들에 대해 적용하는 for문 
    count = 0
    for file in directory:
        list.insert("end", file) # 목록의 마지막에 이어 붙이기. // 원본 : list.insert(0, file)
    
    for file in directory:
                # 만약 파일의 숨김 속성('h')이 1이라면 하이라이트 처리.
        if(has_hidden_attribute(file) == 1) :
            print("FOUND_A_HIDDEN_FILE!!!! HOORAY!!!!!!__________123412341234123412341234==========1234123412341234")
            list.itemconfig(count, {'bg' : 'khaki1'})
        count += 1
        
def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def changePathByClick(event=None):
    # Get clicked item.
    picked = list.get(list.curselection()[0])
    # get the complete path by joining the current path with the picked item
    path = os.path.join(currentPath.get(), picked)
    # Check if item is file, then open it
    if os.path.isfile(path):
        print('Opening: '+path)
        os.startfile(path)
    # Set new path, will trigger pathChange function.
    else:
        currentPath.set(path)

def goBack(event=None):
    # get the new path
    newPath = pathlib.Path(currentPath.get()).parent
    # set it to currentPath
    currentPath.set(newPath)
    # simple message
    print('Going Back')

def open_popup():
    global top
    top = Toplevel(explorer_frame)
    top.geometry("250x150")
    top.resizable(False, False)
    top.title("Child Window")
    top.columnconfigure(0, weight=1)
    Label(top, text='Enter File or Folder name').grid()
    Entry(top, textvariable=newFileName).grid(column=0, pady=10, sticky='NSEW')
    Button(top, text="Create", command=newFileOrFolder).grid(pady=10, sticky='NSEW')

def newFileOrFolder():
    # check if it is a file name or a folder
    if len(newFileName.get().split('.')) != 1:
        open(os.path.join(currentPath.get(), newFileName.get()), 'w').close()
    else:
        os.mkdir(os.path.join(currentPath.get(), newFileName.get()))
    # destroy the top
    top.destroy()
    pathChange()

top = ''

# String variables
newFileName = StringVar(explorer_frame, "File.dot", 'new_name')
currentPath = StringVar(
    explorer_frame,
    name='currentPath',
    value=pathlib.Path.cwd()
)
# Bind changes in this variable to the pathChange function
currentPath.trace('w', pathChange)

Button(explorer_frame, text='Folder Up', command=goBack).grid(
    sticky='NSEW', column=0, row=0
)
# Keyboard shortcut for going up
root.bind("<Alt-Up>", goBack)
Entry(explorer_frame, textvariable=currentPath).grid(
    sticky='NSEW', column=1, row=0, ipady=10, ipadx=10
)

# List of files and folder
list = Listbox(explorer_frame, width = 70)
list.grid(sticky='NSEW', column=1, row=1, ipady=10, ipadx=10)

# List Accelerators
list.bind('<Double-1>', changePathByClick)
list.bind('<Return>', changePathByClick)

# Menu
menubar = Menu(root)
# change directory
menubar.add_command(label="C: drive", command=changeDirToC)
menubar.add_command(label="D: drive", command=changeDirToD)
# Adding a new File button
menubar.add_command(label="Add File or Folder", command=open_popup)
# Adding a quit button to the Menubar
menubar.add_command(label="Quit", command=root.quit)
# Make the menubar the Main Menu
root.config(menu=menubar)


changeDirToC()
pathChange('')

# run the main program
root.mainloop()

