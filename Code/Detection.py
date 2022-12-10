#kicomav-master/Init_Release.py 후 실행
#백신 엔진으로 폴더 및 파일 검사
import subprocess

result = subprocess.call(["python", "kicomav-master/Release/k2.py", "Detection_List", "-r"], shell=True)
print(result)
