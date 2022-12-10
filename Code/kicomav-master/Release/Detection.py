#백신 엔진으로 폴더 및 파일 검사
import subprocess

#result = exec(open("k2.py").read)
result = subprocess.call(["python", "k2.py", "Detection_List", "-r"], shell=True)
print(result)
