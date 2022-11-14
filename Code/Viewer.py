from tkinter import *
import os
import ctypes
import pathlib
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
root.geometry("1280x800+100+100")
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

menu_1=Menu(menubar, tearoff=0)
menu_1.add_command(label="C드라이브", command=changeDirToC)
menu_1.add_command(label="D드라이브", command=changeDirToD)
menu_1.add_separator()
menu_1.add_command(label="하위 메뉴 1-3", command=close)
menubar.add_cascade(label="파일", menu=menu_1)

menu_2=Menu(menubar, tearoff=0, selectcolor="red")
menu_2.add_radiobutton(label="하위 메뉴 2-1", state="disable")
menu_2.add_radiobutton(label="하위 메뉴 2-2")
menu_2.add_radiobutton(label="하위 메뉴 2-3")
menubar.add_cascade(label="보기", menu=menu_2)

menu_3=Menu(menubar, tearoff=0)
menu_3.add_checkbutton(label="하위 메뉴 3-1")
menu_3.add_checkbutton(label="하위 메뉴 3-2")
menubar.add_cascade(label="도구", menu=menu_3)

menu_4=Menu(menubar, tearoff=0)
menubar.add_cascade(label="도움말", menu=menu_4)

root.config(menu=menubar)



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
title_frame = Frame(root, relief='solid', width = 700, height = 20)
title_frame.grid(column=0, row=0)
main_frame = Frame(root, relief='solid', width = 700, height = 300)
main_frame.grid(column=0, row=1)

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



changeDirToC()

# run the main program
root.mainloop()

