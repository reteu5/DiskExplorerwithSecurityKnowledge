# DiskExplorerwithSecurityKnowledge
프로젝트 수행 계획은 [[여기](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/slides/%EB%B0%B1%EC%8A%B9%EC%9A%B0_%ED%8C%80%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8.pdf)]에서 확인하실 수 있습니다.  
분담 전까지는 같은 기능 구현에 여러 사람이 들어가는 일이 없도록 코드에 변경 사항이 있을 경우 바로바로 커밋해주시면 감사드리겠습니다요.

파이팅!

## 1. 1차적으로 구현 완료된 기능
 -- * [[File_Searcher.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/File_Searcher.py)] --

 * 드라이브 볼륨 [[mountpoint @ Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py#:~:text=for%20drive%20in%20GetDrive,i%20in%20diskIO%3A)]
 * 드라이브 포맷 [[fstype @ Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py#:~:text=for%20drive%20in%20GetDrive,i%20in%20diskIO%3A)]
 * rw 권한 및 이동식 디스크 여부 확인 [[opts @ Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
 * maxfile [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * 어떻게 읽어야되는지 모르겠음
 * maxpath [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * 어떻게 읽어야 되는지 모르겠음
 * 총 저장공간 [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
 * 사용한 저장공간 [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
 * 가용 저장공간 [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
 
 ## 2. 확인이 필요한 기능
 * Rate of Usage [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * 저장공간 사용률을 나타낸 거라면 버그가 있는 것 같고, 디스크 로드율을 말하는거라면 확인 필요
 * read_count [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * C 드라이브 기준으로만 계산이 되는 것 같은데 확인 필요
 * write_count [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * C 드라이브 기준으로만 계산이 되는 것 같은데 확인 필요
 * read_bytes [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * C 드라이브 기준으로만 계산이 되는 것 같은데 확인 필요
 * write_bytes [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * C 드라이브 기준으로만 계산이 되는 것 같은데 확인 필요
 * read_time [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * C 드라이브 기준으로만 계산이 되는 것 같은데 확인 필요
 * write_time [[Get_Disk_Information.py](https://github.com/reteu5/DiskExplorerwithSecurityKnowledge/blob/main/Code/Get_Disk_Information.py)]
   * C 드라이브 기준으로만 계산이 되는 것 같은데 확인 필요
