import shutil
import string
import psutil

from ctypes import windll

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

if __name__ == '__main__':
   
   GetInfromationDrives = psutil.disk_partitions() #psutil 모듈로 다 구해지네... 열심히 경로 직접 구했는데...............................
   GetDrive = get_drives() # 여러 드라이브 리스트로 저장   
   #print(GetDrive)
   
   for Drive in GetInfromationDrives:
    print(Drive) #디스크들 정보 출력.......
    Percentage = psutil.disk_usage(Drive.mountpoint)
   
   for drive in GetDrive:
    path = drive + ':\\' # 여러 드라이브 중 한 드라이브만 추출해서 경로 입력
    total, used, free = shutil.disk_usage(path) # 디스크 용량 확인
    total_label, used_label, free_label = shutil.disk_usage(path)._fields #디스크 용량에 대한 이름 확인
    print(f'{total_label} = {total:,} byte  /  {used_label} = {used:,} byte  /  {free_label} = {free:,} byte')
    print(f'{total_label} = {(total / 2 ** 20):,.2f} MB  /  {used_label} = {(used / 2 ** 20):,.2f} MB  /  {free_label} = {(free / 2 ** 20):,.2f} MB /', f'Rate of usage = {Percentage.percent}%')
    #print(psutil.disk_usage(path))
