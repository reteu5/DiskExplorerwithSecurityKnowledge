import shutil
import string
import psutil

from ctypes import windll


if __name__ == '__main__':
   
   GetInfromationDrives = psutil.disk_partitions() 
   
   for index in range(len(GetInfromationDrives)):
        Drive = GetInfromationDrives[index]
        print(Drive) #디스크들 정보 출력.......
        path = Drive.mountpoint
        Percentage = psutil.disk_usage(path)
        total, used, free = shutil.disk_usage(path) # 디스크 용량 확인
        total_label, used_label, free_label = shutil.disk_usage(path)._fields #디스크 용량에 대한 이름 확인
        print(f'{total_label} = {total:,} byte  /  {used_label} = {used:,} byte  /  {free_label} = {free:,} byte')
        print(f'{total_label} = {(total / 2 ** 20):,.2f} MB  /  {used_label} = {(used / 2 ** 20):,.2f} MB  /  {free_label} = {(free / 2 ** 20):,.2f} MB /', f'Rate of usage = {Percentage.percent}%')

        DiskIOInformation = []
        diskIO = psutil.disk_io_counters(perdisk=True)
        for i in diskIO['PhysicalDrive'+str(index)]:    # dictionary형 데이터에 드라이브 명으로 접근
            DiskIOInformation.append(i)
        print(f'read_count = {DiskIOInformation[0]}, write_count = {DiskIOInformation[1]}, read_bytes = {DiskIOInformation[2]}, write_bytes = {DiskIOInformation[3]}, read_time = {DiskIOInformation[4]}, write_time = {DiskIOInformation[5]}')
