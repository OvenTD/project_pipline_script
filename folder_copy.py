import os
import shutil

# Define source and destination directories
source_dir = r'D:\Hijackers\Animatic_auto\S01'
destination_dir = r'E:\Hijackers_UE\VillanDies1\Content\1_Scene\S_1'

# Iterate over all files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith(".mp4"):
        # Split the filename by the hyphen to remove the unnecessary part
        parts = filename.split('-')
        if len(parts) == 2:
            # Keep only the second part, which is already in "04_0010" format
            new_name = parts[1]  # "04_0010.mp4"
            new_name = new_name.replace(".mp4", "")  # Remove extension for folder creation

            # Define the new folder path in the destination directory
            new_folder_path = os.path.join(destination_dir, new_name)

            # Create the directory structure if it doesn't already exist
            os.makedirs(new_folder_path, exist_ok=True)

            # Copy the MP4 file to the new folder
            source_file_path = os.path.join(source_dir, filename)
            destination_file_path = os.path.join(new_folder_path, filename)
            print(f"Copied {filename} as {new_name} to {new_folder_path}")

print("File renaming and copying completed.")
