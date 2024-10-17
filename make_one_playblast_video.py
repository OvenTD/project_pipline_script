import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import maya.cmds as cmds

# Specify the folder path
folder_path = r'D:\Hijackers\Animatic_auto'

# List to store all MP4 files
mp4_files = []

# Find all MP4 files, including those in subfolders
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.mp4'):
            # Add the full file path to the list
            mp4_files.append(os.path.join(root, file))


# Save the concatenated video to a file
output_path = r'D:\Hijackers\combined_video.mp4'


# Function to run the video combination logic
def combine_videos_in_maya(*args):
    folder_path = r'D:\Hijackers\Animatic_auto'
    mp4_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))

    clips = [VideoFileClip(file) for file in mp4_files]
    final_clip = concatenate_videoclips(clips)
    output_path = r'D:\Hijackers\combined_video.mp4'
    final_clip.write_videofile(output_path, codec='libx264')

# Create a Maya UI button to trigger the script
if cmds.window("combineVideoWin", exists=True):
    cmds.deleteUI("combineVideoWin")

window = cmds.window("combineVideoWin", title="Combine Videos", widthHeight=(200, 100))
cmds.columnLayout(adjustableColumn=True)
cmds.button(label="Combine MP4 Videos", command=combine_videos_in_maya)
cmds.showWindow(window)
