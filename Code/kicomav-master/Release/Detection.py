import subprocess

#result = exec(open("k2.py").read)
result = subprocess.call(["python", "k2.py", "Detection_List", "-r"], shell=True)
print(result)
