import os

def find_fbx_files(root_dir):
    fbx_file_paths = []
    fbx_file_names = []
    
    # os.walk를 사용하여 디렉토리를 순회합니다.
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # 파일의 확장자가 .fbx인지 확인합니다.
            if filename.lower().endswith('.fbx'):
                # .fbx 파일의 전체 경로를 리스트에 추가합니다.
                full_path = os.path.join(dirpath, filename)
                # 경로에서 역슬래시를 슬래시로 변경합니다.
                full_path = full_path.replace('\\', '/')
                fbx_file_paths.append(full_path)
                # 파일 이름을 리스트에 추가합니다.
                fbx_file_names.append(filename)
    
    return fbx_file_paths, fbx_file_names
root_directory = 'D:/Hijackers/MotionCaptureData/OKcut'

# 함수 호출 및 결과 출력
fbx_file_paths, fbx_file_names = find_fbx_files(root_directory)
print("FBX 파일 경로 리스트:")
print(fbx_file_paths)
print("\nFBX 파일 이름 리스트:")
print(fbx_file_names)
