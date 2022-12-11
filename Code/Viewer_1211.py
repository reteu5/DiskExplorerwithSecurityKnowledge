from tkinter import *
import os
import ctypes
import pathlib
import stat
import subprocess
from SMART import *
from tkinter.font import *



# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
# set a title
#root.title('Simple Explorer')

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

# set a window
root.geometry("1280x720+100+100")           # 1280x800+100+100
#root.resizable(True, True)


#smart
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
    else:
        temper.set('-')

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




frame_photo = PhotoImage(file='img/frame.png')
frame_label = Label(root, border=0, bg='white', image=frame_photo)
frame_label.pack(fill=BOTH, expand=True)


# Frame1 : Drive Type + Disk Name
#frame1 = Frame(root, relief="solid")
#frame1.place(x=36, y=114, width=583, height=70)
font1 = Font(family="Inter", weight='bold', size = 24)
label1=Label(root, textvariable=disk, font=font1, bg='#5E80F8', fg='white')
label1.place(x=36+18,y=114+21)

font3 = Font(family="Inter", weight='bold', size = 20)
var1=Label(root, textvariable=model_num, font=font3, bg='#BBFFE7')
var1.place(x=36+84, y=114+21)


# Frame2 : Disk Details
font2 = Font(family="Inter", weight='bold', size = 10)
#label2=Label(root, text="일련번호 (S/N)")
#label2.place(x=30, y=5)
var2=Label(root, textvariable=serial_num, font=font2, border=0, bg='white')
var2.place(x=50+152, y=337+5)

#label3=Label(root, text="펌웨어 버전 정보")
#label3.place(x=30, y=42)
var3=Label(root, textvariable=firm_ver, font=font2, border=0, bg='white')
var3.place(x=50+152, y=337+42)

#label4=Label(root, text="NVMe 버젼")
#label4.place(x=30, y=79)
var4=Label(root, textvariable=nvme_ver, font=font2, border=0, bg='white')
var4.place(x=50+152, y=337+79)


# 온도 : 위험 빨강='#FDBB7D', 평범 파랑='#7DA9FD', 경고 노랑='#F1F451', 알수없음='#CACACA'
font5 = Font(family="Inter", weight='bold', size = 24)
var5=Label(root, textvariable=temper, font=font5, bg='#FDBB7D', fg='white')
var5.place(x=53+10, y=223+27)


#label6=Label(root, text="총 저장공간")
#label6.place(x=30, y=116)
var6=Label(root, textvariable=total_cap, font=font2, border=0, bg='white')
var6.place(x=50+152, y=337+116)

#label7=Label(root, text="점유중인 저장공간")
#label7.place(x=30, y=153)
var7=Label(root, textvariable=util_cap, font=font2, border=0, bg='white')
var7.place(x=50+152, y=337+153)

#label8=Label(root, text="총 읽기량")
#label8.place(x=30, y=190)
var8=Label(root, textvariable=data_read, font=font2, border=0, bg='white')
var8.place(x=50+152, y=337+190)

#label9=Label(root, text="총 쓰기량")
#label9.place(x=30, y=227)
var9=Label(root, textvariable=data_write, font=font2, border=0, bg='white')
var9.place(x=50+152, y=337+227)

#label10=Label(root, text="가동 시간")
#label10.place(x=30, y=264)
var10=Label(root, textvariable=power_hours, font=font2, border=0, bg='white')
var10.place(x=50+152, y=337+264)

#label11=Label(root, text="사용 횟수")
#label11.place(x=30, y=301)
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
    # 프로그램 처음 실행시에는 정상적으로 작동하는데, 경로를 이동하면 함수 자체는 거치는데 하이라이트가 안되는 현상 발생. 버그 수정 필요합니다.
    # 프로그램 처음 실행시에는 정상적으로 작동하는데, 경로를 이동하면 함수 자체는 거치는데 하이라이트가 안되는 현상 발생. 버그 수정 필요합니다.
    # 프로그램 처음 실행시에는 정상적으로 작동하는데, 경로를 이동하면 함수 자체는 거치는데 하이라이트가 안되는 현상 발생. 버그 수정 필요합니다.
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
    Label(top, text='Enter File or Folder name').place(x=0, y=0, relx=0.5)
    Entry(top, textvariable=newFileName).place(x=0, y=50, relx=0.5, relwidth=0.8)
    Button(top, text="Create", command=newFileOrFolder).place(x=0, y=100, relx=0.5)

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
Button(root, text='Folder Up', command=goBack, relief='flat', image=button_img1, bg='#BBFFE7', activebackground='#BBFFE7').place(x=654, y=135)

# Keyboard shortcut for going up
root.bind("<Alt-Up>", goBack)
font4 = Font(family="Inter", weight='bold', size = 12)
Entry(root, font=font4, textvariable=currentPath, width=40, border=0, bg='black', fg='white').place(x=770, y=147)

# List of files and folder
list = Listbox(root, width=60, height=21, relief='flat')
list.place(x=765, y=212)

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
menubar.add_command(label="(un)Hide File", command=file_magician)
# Adding a quit button to the Menubar
menubar.add_command(label="Quit", command=root.quit)
# Make the menubar the Main Menu
root.config(menu=menubar)


changeDirToC()
pathChange('')

# run the main program
root.mainloop()

