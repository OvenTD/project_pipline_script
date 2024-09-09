import openpyxl
import os
import re
import maya.cmds as cmds
import moviepy.editor as moviepy
import maya.mel as mel

# Global UI elements
global progress_control
global text_scroll_list

# Function to load Excel data
def load_excel_data(excel_file_path):
    workbook = openpyxl.load_workbook(excel_file_path, data_only=True, read_only=True)
    sheet = workbook.active

    cut_numbers = []
    first_frames = []
    last_frames = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            break
        cut_numbers.append(row[0])
        first_frames.append(row[1])
        last_frames.append(row[2])

    workbook.close()

    return cut_numbers, first_frames, last_frames

# Function to generate folder paths based on cut numbers
def generate_folder_paths(cut_numbers, root_dir):
    base_folder_path = f"{root_dir}/LO_"
    folder_paths = []

    for cut_number in cut_numbers:
        first_part = cut_number.split('_')[0]
        full_folder_path = f"{base_folder_path}{first_part}/{cut_number}/Scenefiles"
        folder_paths.append(full_folder_path)

    return folder_paths

# Function to find the latest .ma file in a directory
def find_latest_ma_file(folder_path):
    ma_files = [f for f in os.listdir(folder_path) if f.endswith('.ma')]
    highest_version = 0
    highest_version_file = None

    version_pattern = re.compile(r'_v(\d+)\.ma$')

    for ma_file in ma_files:
        match = version_pattern.search(ma_file)
        if match:
            version_number = int(match.group(1))
            if version_number > highest_version:
                highest_version = version_number
                highest_version_file = ma_file

    return highest_version_file

# Function to resolve animation or layout folder
def resolve_scene_folder(folder_path):
    anm_folder_path = f'{folder_path}/anm/Animation'
    lay_folder_path = f"{folder_path}/lay/Layout"

    if os.path.isdir(anm_folder_path):
        return anm_folder_path
    elif os.path.isdir(lay_folder_path):
        return lay_folder_path
    else:
        print(f"No 'anm' or 'lay' folder found in {folder_path}")
        return None

# Function to playblast and convert the video
def playblast_and_convert(scene_num, cleaned_scene_name, first_frame, last_frame, folder_path):
    # Set playback range
    cmds.playbackOptions(min=first_frame, max=last_frame)

    try:
        mel.eval('setNamedPanelLayout "Single Perspective View"')
        cmds.lookThru("AnimCam", "modelPanel4") 
    except:
        print('AnimCam not found')
        return

    cmds.modelEditor('modelPanel4', edit=True, displayAppearance='smoothShaded', displayTextures=True)

    # Define the playblast filename
    video_name = f'D:/Hijackers/Animatic_auto/S{scene_num}/{cleaned_scene_name}.avi'

    # Define parameters for the playblast
    playblast_options = {
        'format': 'avi',
        'filename': video_name,
        'forceOverwrite': True,
        'sequenceTime': 0,
        'clearCache': True,
        'viewer': False,
        'showOrnaments': False,
        'offScreen': True,
        'fp': 4,  # Frame padding
        'percent': 100,
        'compression': 'none',
        'quality': 100,
        'widthHeight': (1920, 1080),
    }

    # Execute the playblast command
    cmds.playblast(**playblast_options)

    # Convert the video to mp4 format
    clip = moviepy.VideoFileClip(video_name)
    mp4_video_name = f'D:/Hijackers/Animatic_auto/S{scene_num}/{cleaned_scene_name}.mp4'
    clip.write_videofile(mp4_video_name)

    # Remove the original AVI file
    os.remove(video_name)

# Function to process scenes and update UI
def process_scenes(cut_numbers, first_frames, last_frames, folder_paths):
    total_scenes = len(cut_numbers)
    
    for num, folder_path in enumerate(folder_paths):
        resolved_folder = resolve_scene_folder(folder_path)
        if not resolved_folder:
            continue

        # Find the highest version .ma file
        latest_ma_file = find_latest_ma_file(resolved_folder)
        if not latest_ma_file:
            print(f"No .ma files found in {resolved_folder}")
            continue

        # Extract base name and clean the name
        base_name, _ = os.path.splitext(latest_ma_file)
        parts = base_name.split('_')
        cleaned_scene_name = '_'.join(parts[1:3])

        # Extract scene number from folder path
        match = re.search(r'LO_(\d+)/', folder_path)
        scene_num = match.group(1) if match else 'Unknown'

        # Update textScrollList and progress bar
        cmds.textScrollList(text_scroll_list, edit=True, removeIndexedItem=1)
        cmds.progressBar(progress_control, edit=True, progress=int(((num+1)/total_scenes)*100))

        # Open the scene in Maya
        scene_file_path = f"{resolved_folder}/{latest_ma_file}"
        print(f'Opening file: {scene_file_path}')
        cmds.file(scene_file_path, force=True, open=True)

        # Playblast and convert the video
        playblast_and_convert(scene_num, cleaned_scene_name, first_frames[num], last_frames[num], folder_path)

# Main function to start processing with UI
def run_process():
    excel_file_path = 'D:/Hijackers/Animatic_auto/Frame_range_data.xlsx'
    root_dir = 'D:/Hijackers/Prism/VillanDies/03_Production/Shots'

    # Load data from the Excel file
    cut_numbers, first_frames, last_frames = load_excel_data(excel_file_path)

    # Generate folder paths based on cut numbers
    folder_paths = generate_folder_paths(cut_numbers, root_dir)

    # Populate the textScrollList with scene names
    cmds.textScrollList(text_scroll_list, edit=True, removeAll=True)
    cmds.textScrollList(text_scroll_list, edit=True, append=cut_numbers)

    # Process scenes
    process_scenes(cut_numbers, first_frames, last_frames, folder_paths)

# Function to create UI
def create_ui():
    global progress_control
    global text_scroll_list

    if cmds.window('sceneProcessorWindow', exists=True):
        cmds.deleteUI('sceneProcessorWindow')

    window = cmds.window('sceneProcessorWindow', title='Auto Plablast Generator', widthHeight=(400, 300))
    layout = cmds.columnLayout(adjustableColumn=True)

    # Button to start processing
    cmds.button(label='Start Process', command=lambda x: run_process())

    # Add a separator to create space between the button and the text scroll list
    cmds.separator(height=20, style='none')  # Adjust the height as needed

    # TextScrollList to display remaining scenes
    cmds.text(label="Remaining")
    text_scroll_list = cmds.textScrollList(numberOfRows=8, height=150)

    # Add another separator to create space between the list and the progress bar
    cmds.separator(height=10, style='none')

    # ProgressBar to show progress
    progress_control = cmds.progressBar(maxValue=100, width=400)

    cmds.showWindow(window)
# Call the UI creation function
create_ui()
