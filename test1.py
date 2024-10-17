from moviepy.editor import VideoFileClip
import os

# AVI 파일들이 저장된 경로
input_folder = r"D:\Hijackers\Prism\VillanDies\05_ProjectWindow\movies"
output_folder = r"D:\Hijackers\Prism\VillanDies\05_ProjectWindow\movies"

# 파일명을 1.avi ~ 7.avi로 정의하고 변환
for i in range(6, 7):
    input_file = os.path.join(input_folder, f"{i}.avi")
    output_file = os.path.join(output_folder, f"{i}.mp4")

    # VideoFileClip을 사용해 AVI 파일을 로드하고 MP4로 변환
    try:
        clip = VideoFileClip(input_file)
        clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
        print(f"{input_file} -> {output_file} 변환 완료")
    except Exception as e:
        print(f"{input_file} 변환 중 오류 발생: {e}")
