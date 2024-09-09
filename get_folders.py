import os

def print_folder_names(path):
    try:
        # 선택한 경로에서 모든 항목을 검사
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            # 해당 항목이 폴더인지 확인[]
            if os.path.isdir(item_path):
                print(item)
    except Exception as e:
        print(f"Error: {e}")

# 사용할 경로를 지정
selected_path = r'D:\Hijackers\MotionCaptureData\Baked'
print_folder_names(selected_path)
