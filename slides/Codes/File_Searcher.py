from tkinter import *
from Get_Disk_Information import get_drives
import os 
import os.path

def clickListBox(evt):
    global currentDir, searchDirList
    if (dirListBox.curselection() == ()):  # 다른 리스트 박스를 클릭할 때는 무시함.
        return
    dirName = str(dirListBox.get(dirListBox.curselection()))  # 클릭한 폴더 이름 (문자열)
    if dirName == '상위폴더':
        if len(searchDirList) == 1:  # 상위 폴더를 클릭했는데, 현재 C:\\면 무시함.
            return
        searchDirList.pop()  # 상위 폴더 이동이므로, 마지막 검색 폴더(=현재 폴더) 제거
    else:
        searchDirList.append(currentDir+dirName+'\\')  # 검색 리스트에 클릭한 폴더 추가

    return fillListBox()

def fillListBox():  # 항상 제일 검색한 폴더 리스트의 마지막 폴더(=현재 폴더)를 표시
    global currentDir, searchDirList, dirLabel, dirListBox, fileListBox
    dirListBox.delete(0, END)  # 폴더 리스트 박스를 비움
    fileListBox.delete(0, END)  # 파일 리스트 박스를 비움

    dirListBox.insert(END, "상위폴더")
    currentDir = searchDirList[len(searchDirList) - 1]  # 디렉터리 리스트의 마지막이 현재 폴더.
    dirLabel.configure(text=currentDir) # ﻿위쪽 글자를 현재 폴더로 변경한다. 현재 폴더 안의 파일 · 폴더 목록을 뽑은 후
    folderList = os.listdir(currentDir)

    for item in folderList: # ﻿파일은 파일 리스트 박스에 삽입하고 ,폴더는 폴더 리스트 박스에 삽입한다
        if os.path.isdir(currentDir + item):
            dirListBox.insert(END, item)
        elif os.path.isfile(currentDir + item):
            fileListBox.insert(END, item)
 

window = None
GETDRIRVES = get_drives()
dirLabel, dirListBox, fileListBox = None, None, None # 윈도창에 나올 위젯 변수들

if __name__ == "__main__":
    
    for GETDRIVE in GETDRIRVES:
        print(GETDRIVE)

    CurrentDriver = input("위 드라이버 중에 선택하세요 (드라이브 이름과 반드시 동일하게 이름 작성) : ")
    searchDirList = [CurrentDriver + ':\\']  
    currentDir = CurrentDriver + ':\\'

    window = Tk()
    window.title("폴더 및 파일 목록 보기")
    window.geometry('300x500')

    dirLabel = Label(window, text=currentDir) # 위쪽 현재 폴더의 전체 경로 출력
    dirLabel.pack()

    dirListBox = Listbox(window) # 왼족 현재 폴더의 하위 폴더 목록을 보여 주는 리스트 박스
    dirListBox.pack(side=LEFT, fill=BOTH, expand=1)
    dirListBox.bind('<<ListboxSelect>>', clickListBox)

    fileListBox = Listbox(window) # 왼족 현재 폴더의 파일 목록을 보여주는 리스트 박스
    fileListBox.pack(side=RIGHT, fill=BOTH, expand=1)

    fillListBox()   # 초기엔 드라이브의 모든 폴더 목록을 만들기

    window.mainloop()