# from pySMART 
# REQUIREMENT : https://www.smartmontools.org/wiki/Download#InstalltheWindowspackage 에서 S.M.A.R.T. mon Tool 설치 필요


import os

class Device():
    
    def __init__(self, device_name):
        self.device_name = device_name
        self.info = {}
        self.results = []
    
    def get_device_info(self):
        
        cmd = 'smartctl -a ' + self.device_name
        
        data = os.popen(cmd).read()
        
        res = data.split('\n')[:-1]
        
        record = 0
        for l in res:
            if l == '' and record == 2:
                record = 1
                continue
            
            if l == '':
                record = 0
                       
            if record == 1 or record == 2:
                temp = l.split(':')
                self.info[temp[0]] = temp[-1].lstrip()
                print(temp[0]+': '+self.info[temp[0]])
                
            elif l == '=== START OF INFORMATION SECTION ===':
                record = 1
            
            elif l == '=== START OF SMART DATA SECTION ===':
                record = 2
               
def get_device_name():
    cmd = 'smartctl --scan'
    
    data = os.popen(cmd).read()
    data_ = data.split('\n')[:-1]
    name = []
    for d in data_:
        name.append(d.split(' ')[0])
    return name
    
if __name__ == '__main__':
    device_name_list = get_device_name()
    device = []
    
    for dev in device_name_list:
        device.append(Device(dev))
    
    for dev in device:
        dev.get_device_info()
        
