import os
import shutil

# Path to the main directory containing all folders
base_dir = r"D:\Hijackers_UE\VillanDies1\Content\1_Scene\S_4"

# Define the source folder and list all folders in base directory
source_folder_name = "04_0010"
source_folder_path = os.path.join(base_dir, source_folder_name)
destination_folders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder)) and folder != source_folder_name]

# Iterate over each destination folder
for dest_folder_name in destination_folders:
    dest_folder_path = os.path.join(base_dir, dest_folder_name)
    
    # Copy each file from the source folder to the destination folder with the updated name
    for file_name in os.listdir(source_folder_path):
        source_file_path = os.path.join(source_folder_path, file_name)
        
        # Replace "04_0010" in the filename with the destination folder name
        new_file_name = file_name.replace(source_folder_name, dest_folder_name)
        dest_file_path = os.path.join(dest_folder_path, new_file_name)
        
        # Copy file with the new name to the destination folder
        shutil.copy2(source_file_path, dest_file_path)
        print(f"Copied {new_file_name} to {dest_folder_path}")
