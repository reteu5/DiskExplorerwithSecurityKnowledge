import os
import shutil
import time

import argparse

parser = argparse.ArgumentParser(description='Zero fills the file system')
parser.add_argument('basepath', help='basepath is required.')
args = parser.parse_args()

# 드라이브 공간 확보
total, used, free = shutil.disk_usage(args.basepath)  #path에 대한 디스크 사용량 통계를 total(총량), used(사용량), free(사용할 수 있는 양) 속성이 있는 튜플로 알려줌

# 바이트 배열 생성
buff = bytearray(1048576*100)  #정해진 길이 만큼 0으로 채워진 바이트 배열 생성

tempdir = os.path.join(args.basepath, f"files_tmp") #인수에 전달된 2개의 문자열을 결합해, 1개의 경로로 할 수 있음
if not os.path.exists(tempdir): os.makedirs(tempdir) #os.path.exists:tempdir존재 여부 확인, 존재하지 않으면 tempdir라는 dir 생성  
print(f"tempdir : {tempdir} 0으로 채워진 파일을 보관하기 위해 생성") #{tempdir}에 tempdir명이 들어감

for i in range(int(free/len(buff))):  #사용할 수 있는 양/buff길이 만큼 반복
  ff = open(os.path.join(tempdir, f"file_{i}.tmp"), "wb") #tempdir이랑 file_{i}.tmp경로를 합친 걸 이진수 쓰기 모드로 열기
  start = time.time()              #시작
  byteswritten = ff.write(buff)    #바이트쓰기 파일에 생성한 바이트 배열 쓰기
  end = time.time()                #끝
  speed = byteswritten/1048576 / (end-start)    #속도 
  total, used, free = shutil.disk_usage(tempdir)    #tempdir의 디스크 사용량

  print(f'free: {int(free/(1024*1024))} Mb, speed = {speed:.2f} Mb/sec') 
  ff.close()

# 임시 파일 생성
ff = open(os.path.join(tempdir, f"file_final.tmp"), "wb")  #os.path.join: tempdir와 file_final.tmp 경로를 합침  write binary 
byteswritten = ff.write(bytearray(free))  #
ff.close()

# 임시 파일 삭제
print("드라이브 공간이 가득 참")
ans = input(f"삭제할건가요?: {tempdir} (Y/N)? ")
if "Y" == ans.upper():
  if os.path.exists(tempdir): shutil.rmtree(tempdir)
