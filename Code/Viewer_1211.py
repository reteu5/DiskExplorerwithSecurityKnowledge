from tkinter import *
import os
import ctypes
from ctypes import windll
import pathlib
import stat
import subprocess
from SMART import *
from tkinter.font import *



# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
root.wm_attributes('-transparentcolor', 'grey')

# no title
root.overrideredirect(True)

# set a window
full_size = "1280x720+100+100"
root.geometry(full_size)                    # default : 1280x800+100+100
root.resizable(False, False)                # fixed


# SMART.py
device_name_list = get_device_name()
device = []

for dev in device_name_list:
    device.append(Device(dev))

def changeDirToC(event=None):
    disk.set("C")
    model_num.set(device[0].get_device_info("Model Number"))
    serial_num.set(device[0].get_device_info("Serial Number"))
    firm_ver.set(device[0].get_device_info("Firmware Version"))
    nvme_ver.set(device[0].get_device_info("NVMe Version"))
    total_cap.set(device[0].get_device_info("Total NVM Capacity"))
    util_cap.set(device[0].get_device_info("Namespace 1 Utilization"))
    data_read.set(device[0].get_device_info("Data Units Read"))
    data_write.set(device[0].get_device_info("Data Units Written"))
    power_hours.set(device[0].get_device_info("Power On Hours"))
    cycles.set(device[0].get_device_info("Power Cycles"))

    tmp = device[0].get_device_info("Temperature")
    tmp2 = tmp.split(' ')
    if (tmp2[1] == 'Celsius'):
        temper.set(tmp2[0])
        print(int(tmp2[0]))
        if int(tmp2[0]) > 35:
            temperCel.configure(image=redCel)
            var5.configure(bg='#FDBB7D')
        elif int(tmp2[0]) > 30:
            temperCel.configure(image=yellowCel)
            var5.configure(bg='#F1F451')
        elif int(tmp2[0]) < 30:
            temperCel.configure(image=blueCel)
            var5.configure(bg='#7DA9FD')
        else:
            temperCel.configure(image=grayCel)
            var5.configure(bg='#CACACA')
    else:
        temper.set('-')




def changeDirToD(event=None):
    disk.set("D")
    model_num.set(device[1].get_device_info("Device Model"))
    serial_num.set(device[1].get_device_info("Serial Number"))
    firm_ver.set(device[1].get_device_info("Firmware Version"))
    nvme_ver.set(device[1].get_device_info("NVMe Version"))
    total_cap.set(device[1].get_device_info("Total NVM Capacity"))
    util_cap.set(device[1].get_device_info("Namespace 1 Utilization"))
    data_read.set(device[1].get_device_info("Data Units Read"))
    data_write.set(device[1].get_device_info("Data Units Written"))
    power_hours.set(device[1].get_device_info("Power On Hours"))
    cycles.set(device[1].get_device_info("Power Cycles"))

    tmp = device[0].get_device_info("Temperature")
    tmp2 = tmp.split(' ')
    if (tmp2[1] == 'Celsius'):
        temper.set(tmp2[0])
        if int(tmp2[0]) > 35:
            temperCel.configure(image=redCel)
            var5.configure(bg='#FDBB7D')
        elif int(tmp2[0]) > 30:
            temperCel.configure(image=yellowCel)
            var5.configure(bg='#F1F451')
        elif int(tmp2[0]) < 30:
            temperCel.configure(image=blueCel)
            var5.configure(bg='#7DA9FD')
        else:
            temperCel.configure(image=grayCel)
            var5.configure(bg='#CACACA')
    else:
        temper.set('-')


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


initx = 0
inity = 0
def start_move(event):
    print(event)
    initx = event.x
    inity = event.y

def on_move(event):
    x = root.winfo_x() + event.x - initx
    y = root.winfo_y() + event.y - inity
    root.geometry("+%s+%s" % (x, y))

def stop_move(event):
    initx = None
    inity = None

menu_photo = PhotoImage(file='img/menu.png')
menu_label = Label(root, border=0, bg='grey', image=menu_photo)
menu_label.pack(fill=BOTH, expand=True)

menu_label.bind("<ButtonPress-1>", start_move)
menu_label.bind("<ButtonRelease-1>", stop_move)
menu_label.bind("<B1-Motion>", on_move)

frame_photo = PhotoImage(file='img/frame.png')
frame_label = Label(root, border=0, bg='grey', image=frame_photo)
frame_label.pack(fill=BOTH, expand=True)


# : Drive Type + Disk Name
font1 = Font(family="Inter", weight='bold', size = 24)
label1=Label(root, textvariable=disk, font=font1, bg='#5E80F8', fg='white')
label1.place(x=36+18,y=114+21)

font3 = Font(family="Inter", weight='bold', size = 20)
var1=Label(root, textvariable=model_num, font=font3, bg='#BBFFE7')
var1.place(x=36+84, y=114+21)


# : Disk Details
font2 = Font(family="Inter", weight='bold', size = 10)

# 일련번호 (S/N)
var2=Label(root, textvariable=serial_num, font=font2, border=0, bg='white')
var2.place(x=50+152, y=337+5)

# 펌웨어 버전 정보
var3=Label(root, textvariable=firm_ver, font=font2, border=0, bg='white')
var3.place(x=50+152, y=337+42)

# NVMe 버젼
var4=Label(root, textvariable=nvme_ver, font=font2, border=0, bg='white')
var4.place(x=50+152, y=337+79)


# 온도 : 위험 빨강='#FDBB7D', 평범 파랑='#7DA9FD', 경고 노랑='#F1F451', 알수없음='#CACACA'
blueCel = PhotoImage(file='img/blueCel.png')
redCel = PhotoImage(file='img/redCel.png')
yellowCel = PhotoImage(file='img/yellowCel.png')
grayCel = PhotoImage(file='img/grayCel.png')
temperCel = Label(root, border=0, bg='#BBFFE7', image=blueCel)
temperCel.place(x=53, y=233)

font5 = Font(family="Inter", weight='bold', size = 22)
var5=Label(root, textvariable=temper, font=font5, bg='#FDBB7D', fg='white')
var5.place(x=53+7, y=223+27+10)


# 총 저장공간
var6=Label(root, textvariable=total_cap, font=font2, border=0, bg='white')
var6.place(x=50+152, y=337+116)

# 점유중인 저장공간
var7=Label(root, textvariable=util_cap, font=font2, border=0, bg='white')
var7.place(x=50+152, y=337+153)

# 총 읽기량
var8=Label(root, textvariable=data_read, font=font2, border=0, bg='white')
var8.place(x=50+152, y=337+190)

# 총 쓰기량
var9=Label(root, textvariable=data_write, font=font2, border=0, bg='white')
var9.place(x=50+152, y=337+227)

# 가동 시간
var10=Label(root, textvariable=power_hours, font=font2, border=0, bg='white')
var10.place(x=50+152, y=337+264)

# 사용 횟수
var11=Label(root, textvariable=cycles, font=font2, border=0, bg='white')
var11.place(x=50+152, y=337+301)



# file explorer

def pathChange(*event):
    print("path changed to "+str(currentPath.get()))
    # Get all Files and Folders from the given Directory
    directory = os.listdir(currentPath.get())
    # Clearing the list
    list.delete(0, END)
    # Inserting the files and directories into the list
    count = 0
    for file in directory:
        list.insert("end", file) # end : 목록의 마지막에 이어 붙이기. // 원본 : list.insert(0, file)
                    
    # 만약 파일의 숨김 속성('h')이 1이라면 listbox 상에서 하이라이트 처리.
    for file in directory:
        if(has_hidden_attribute(file) == 1) :
            print("Found a hidden one     @ " + str(count))
            # print("FOUND_A_HIDDEN_FILE!!!! HOORAY!!!!!!__________123412341234123412341234==========1234123412341234")
            list.itemconfig(count, {'bg' : 'khaki1'})
        print(count)
        count += 1
        
def has_hidden_attribute(filepath):
    # 원본 코드(아래 코드가 작동 안 할 경우 이걸로 교체) : return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result

def file_magician():
    picked = list.get(list.curselection()[0])
    if(has_hidden_attribute(picked) == 1) :
        show_file(picked)
        print("Selected file is now being shown.")
    else :
        hide_file(picked)
        print("Selected file is now hidden.")
    pathChange()
        
def hide_file(filepath):
    subprocess.check_call(["attrib", "+H", filepath])
    
def show_file(filepath):
    subprocess.check_call(["attrib", "-H", filepath])
    
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
    # get the new path      // 부모 경로를 newPath에 할당
    newPath = pathlib.Path(currentPath.get()).parent
    # set it to currentPath // newPath를 리스트에 띄우기 위해 set 처리
    currentPath.set(newPath)
    # simple message
    print('Going Back')

def open_popup():
    global top
    top = Toplevel(root)
    top.geometry("250x150")
    top.resizable(False, False)
    top.title("Child Window")
    top.columnconfigure(0, weight=1)
    Label(top, text='Enter File or Folder name').place(x=0, y=0)
    Entry(top, textvariable=newFileName).place(x=0, y=50, relwidth=0.8)
    Button(top, text="Create", command=newFileOrFolder).place(x=0, y=100)

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
newFileName = StringVar(root, "File.dot", 'new_name')
currentPath = StringVar(
    root,
    name='currentPath',
    value=pathlib.Path.cwd()
)
# Bind changes in this variable to the pathChange function
currentPath.trace('w', pathChange)


# Frame3 : File Explorer (button, path, listBox)

button_img1 = PhotoImage(file='img/upButton.png')
Button(root, command=goBack, border=0, image=button_img1, bg='#BBFFE7', activebackground='#BBFFE7').place(x=654, y=145)

# Keyboard shortcut for going up
root.bind("<Alt-Up>", goBack)
font4 = Font(family="Inter", weight='bold', size = 12)
Entry(root, font=font4, textvariable=currentPath, width=40, border=0, bg='black', fg='white').place(x=770, y=157)

# List of files and folder
list = Listbox(root, width=60, height=21, relief='flat')
list.place(x=765, y=212)

# List Accelerators
list.bind('<Double-1>', changePathByClick)
list.bind('<Return>', changePathByClick)


cButton = PhotoImage(file='img/cButton.png')
Button(root, command=changeDirToC, border=0, 
        image=cButton, bg='#D9D9D9', activebackground='#D9D9D9').place(x=72, y=11)

dButton = PhotoImage(file='img/dButton.png')
Button(root, command=changeDirToD, border=0, 
        image=dButton, bg='#D9D9D9', activebackground='#D9D9D9').place(x=192, y=11)

addButton = PhotoImage(file='img/add.png')
Button(root, command=open_popup, border=0, 
        image=addButton, bg='#D9D9D9', activebackground='#D9D9D9').place(x=765, y=11)




hideButton = PhotoImage(file='img/hide.png')
Button(root, command=file_magician, border=0, 
        image=hideButton, bg='#D9D9D9', activebackground='#D9D9D9').place(x=880, y=11)

#def detect():
#    result = subprocess.call(["python", "kicomav-master/Release/k2.py", "img", "-r"], shell=True)
#detectButton = PhotoImage(file='img/detectButton.png')
#Button(root, command=detect, border=0, 
#        image=detectButton, bg='#BBFFE7', activebackground='#D9D9D9').place(x=654, y=83)

quitButton = PhotoImage(file='img/quit.png')
Button(root, command=root.quit, border=0, 
        image=quitButton, bg='#D9D9D9', activebackground='#D9D9D9').place(x=1212, y=15)





changeDirToC()
pathChange('')

# run the main program
root.mainloop()

