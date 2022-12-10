#Release 파일 초기화
import subprocess

result1 = subprocess.run(["build.bat", "erase"], shell=True)

result2 = subprocess.run(["build.bat", "build"], shell=True)