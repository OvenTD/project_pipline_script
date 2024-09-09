import openpyxl
import os
import re
import maya.cmds as cmds
import moviepy.editor as moviepy
import maya.mel as mel

# Specify the path to the Excel file
file_path = r'D:\GIT\project_pipline_script\xlsx\file_pathes_and_names.xlsx'

# Load the workbook
workbook = openpyxl.load_workbook(file_path, data_only=True)

# Select the active sheet (or specify a sheet name)
sheet = workbook.active

# Initialize empty lists to store the data
first_frames = []
last_frames = []
scene_folder_paths = []
scene_folder_names = []

# Start reading from row 2 to skip headers (assuming there are headers)
for row in sheet.iter_rows(min_row=2, max_col=4, values_only=True):
    first_frames.append(row[0])  # Data from Column A
    last_frames.append(row[1])  # Data from Column B
    scene_folder_paths.append(row[2])  # Data from Column C
    scene_folder_names.append(row[3])  # Data from Column D

# Close the workbook
workbook.close()

for num in range(len(scene_folder_paths)):
    video_list = []

    print(scene_folder_paths[num])
    print(scene_folder_names[num])

    # Regular expression pattern to match the '01' part
    pattern = re.compile(r'LO_(\d+)/')

    # Search for the pattern in the file path
    match = pattern.search(scene_folder_paths[num])

    if match:
        # Extract and print the matched group
        scene_num = match.group(1)

    # Open the .ma file in Maya
    print('file -f -options "v=0;"  -ignoreVersion  -typ "mayaAscii" -o "'+ scene_folder_paths[num] + '";')
    mel.eval('file -f -options "v=0;"  -ignoreVersion  -typ "mayaAscii" -o "'+ scene_folder_paths[num] + '";')

    # # Set playback range
    # cmds.playbackOptions(min=first_frames[num], max=last_frames[num])

    # # Define the playblast filename
    # video_name = f'D:/Hijackers/Animatic_auto/S{scene_num}/{scene_folder_names[num]}.avi'

    # # Define parameters for the playblast
    # playblast_options = {
    #     'format': 'avi',
    #     'filename': video_name,
    #     'forceOverwrite': True,
    #     'sequenceTime': 0,
    #     'clearCache': True,
    #     'viewer': False,
    #     'showOrnaments': False,
    #     'offScreen': True,
    #     'fp': 4,  # Frame padding
    #     'percent': 100,
    #     'compression': 'none',
    #     'quality': 100,
    #     'widthHeight': (1920, 1080),
    # }

    # # Switch camera
    # cmds.lookThru("AnimCam", "modelPanel4")
    # cmds.playblast(**playblast_options)

    # # Convert the video to mp4 format
    # clip = moviepy.VideoFileClip(video_name)
    # avi_file = video_name
    # mp4_video_name = f'D:/Hijackers/Animatic_auto/S{scene_num}/{scene_folder_names[num]}.mp4'
    # clip.write_videofile(mp4_video_name)

    # os.remove(avi_file)

    # video_list.append(video_name)
