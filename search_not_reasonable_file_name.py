import os

def find_files_and_dirs_with_pattern(start_dir, pattern):
    """
    지정된 디렉토리와 하위 디렉토리를 탐색하여 디렉토리명이나 파일명에 특정 패턴이 포함된 파일을 출력합니다.

    :param start_dir: 시작 디렉토리 경로
    :param pattern: 파일명이나 디렉토리명에 포함되어야 하는 패턴

    구글 드라이브 사용시 충돌시 생기는 (1) 폴더를 찾아서 보여주는 코드입니다.
    """
    for root, dirs, files in os.walk(start_dir):
        # 디렉토리명에 패턴이 포함된 경우 출력
        for dir_name in dirs:
            if pattern in dir_name:
                print(os.path.join(root, dir_name))
        
        # 파일명에 패턴이 포함된 경우 출력
        for file in files:
            if pattern in file:
                print(os.path.join(root, file))

# 시작 디렉토리 경로와 파일명에 포함되어야 하는 패턴을 설정합니다.
start_directory = 'D:/Hijackers/Prism/VillanDies'  # 시작 디렉토리 경로를 입력하세요.
file_name_pattern = '(1)'

# 함수를 호출하여 파일명을 탐색합니다.
find_files_and_dirs_with_pattern(start_directory, file_name_pattern)
