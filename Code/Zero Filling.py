import os
import shutil
import time

import argparse

parser = argparse.ArgumentParser(description='Zero fills the file system')
parser.add_argument('basepath', help='basepath is required.')
args = parser.parse_args()

# 드라이브 공간 확보
total, used, free = shutil.disk_usage(args.basepath)    

# 바이트 배열 생성
buff = bytearray(4000000000000*100)

tempdir = os.path.join(args.basepath, f"files_tmp")
if not os.path.exists(tempdir): os.makedirs(tempdir)
print(f"tempdir : {tempdir} 0으로 채워진 파일을 보관하기 위해 생성")

for i in range(int(free/len(buff))):
  ff = open(os.path.join(tempdir, f"file_{i}.tmp"), "wb")
  start = time.time()              #시작
  byteswritten = ff.write(buff)    #바이트쓰기
  end = time.time()                #끝
  speed = byteswritten/1048576 / (end-start)    #속도
  total, used, free = shutil.disk_usage(tempdir)    

  print(f'free: {int(free/(1024*1024))} Mb, speed = {speed:.2f} Mb/sec')
  ff.close()

# 임시 파일 생성
ff = open(os.path.join(tempdir, f"file_final.tmp"), "wb")
byteswritten = ff.write(bytearray(free))
ff.close()

# 임시 파일 삭제
print("드라이브 공간이 가득 참")
ans = input(f"삭제할건가요?: {tempdir} (Y/N)? ")
if "Y" == ans.upper():
  if os.path.exists(tempdir): shutil.rmtree(tempdir)
