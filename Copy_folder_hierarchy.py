import os
import shutil

def copy_folder_structure(src, dest):
    """
    Copy the folder structure from src to dest without copying any files.

    :param src: Source directory path
    :param dest: Destination directory path
    """
    for root, dirs, files in os.walk(src):
        # Calculate the destination directory path
        dest_dir = root.replace(src, dest, 1)
        
        # Create the destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            print(f"Created directory: {dest_dir}")
        
        # Copy the folder structure (directories only)
        for dir_ in dirs:
            new_dest_dir = os.path.join(dest_dir, dir_)
            if not os.path.exists(new_dest_dir):
                os.makedirs(new_dest_dir)
                print(f"Created directory: {new_dest_dir}")

# Example usage
source_directory = 'D:/Hijackers/MotionCaptureData/OKcut'
destination_directory = 'D:/Hijackers/MotionCaptureData/Baked'
copy_folder_structure(source_directory, destination_directory)
