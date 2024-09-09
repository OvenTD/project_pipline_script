import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

# 지정한 폴더 경로
folder_path = r'D:\Hijackers\Animatic_auto'

# 모든 MP4 파일을 저장할 리스트
mp4_files = []

# 하위 폴더를 포함하여 모든 MP4 파일 찾기
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.mp4'):
            # 전체 파일 경로 추가
            mp4_files.append(os.path.join(root, file))

# 파일 리스트 정렬 (선택 사항: 필요에 따라 정렬 기준을 변경할 수 있음)
#mp4_files.sort()

# MP4 파일들을 VideoFileClip 객체로 변환
clips = [VideoFileClip(file) for file in mp4_files]

# 비디오 클립들을 이어붙임
final_clip = concatenate_videoclips(clips)

# 이어진 비디오를 파일로 저장
output_path = r'D:\Hijackers\combined_video.mp4'
final_clip.write_videofile(output_path, codec='libx264')
