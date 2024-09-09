#
# This code is for asset folders.
# Make folders from the name list.
#


import os

def create_folders(names_list, base_directory):
    for name in names_list:
        folder_path = os.path.join(base_directory, name)
        try:
            os.makedirs(folder_path)
            print(f"폴더 생성 완료: {folder_path}")
        except FileExistsError:
            print(f"폴더 이미 존재함: {folder_path}")
        except Exception as e:
            print(f"폴더 생성 실패: {folder_path}. 오류: {str(e)}")

# 예제 리스트와 기본 디렉토리 설정
name_list = [
    "Badge_01",
    "Badge_02",
    "Badge_03",
    "Badge_04",
    "Badge_05",
    "Badge_06",
    "Badge_07",
    
 

]
  # 여기에 원하는 이름 리스트 추가
base_directory = r"D:\Hijackers_Gdrive\Asset_reference\Badge"  # 여기에 기본 디렉토리 경로 입력

create_folders(name_list, base_directory)
