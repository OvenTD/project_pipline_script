import os
import hou

def files():
    global folder_path
    folder_path = "D:/Houdini/Chance_Hair/Anim_Imort_01/ready" 
    return os.listdir(folder_path)

def get_abc_file_list(directory_path):
    """
    Returns a list of .abc files in the specified directory.

    Args:
        directory_path (str): Path to the directory to search for .abc files.

    Returns:
        list: A list of .abc files in the directory.
    """
    try:
        # Check if the directory exists
        if not os.path.isdir(directory_path):
            raise ValueError(f"The directory does not exist: {directory_path}")
        
        # Generate the list of .abc files
        abc_files = [
            file for file in os.listdir(directory_path) 
            if file.endswith('.abc') and os.path.isfile(os.path.join(directory_path, file))
        ]
        return abc_files
    
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    char_name = "Hero"
    input_path = f"D:/Houdini/Hijackers/{char_name}/Input"
    Gdrive_path = "D:/GDrive/Houdini_render_state"
    output_path = f"D:/Houdini/Hijackers/{char_name}/Output"
    hair_or_eyebrow = ["Hair","Eyebrow"]
    version = 0

    input_file_list = get_abc_file_list(input_path)
    print(input_file_list)

    for file in input_file_list:
        info_list = file[:-4].split("_")
        type_info, scene_info, cut_info, char_name, start_frame, end_frame = info_list

        input_node = hou.node("/obj/Input/input")
        input_node.parm("InputCache").set(input_path+"/"+file)

        setting_node = hou.node("/obj/output/setting")
        print(start_frame, end_frame)
        setting_node.parm("StartFrame").set(start_frame)
        setting_node.parm("EndFrame").set(end_frame)
        
        hair_node = hou.node("/obj/output/Hair_ABC")
        cloak_node = hou.node("/obj/output/Cloak_ABC")
        
        setting_node.parm("Export_Hair").set(f"{output_path}/hair/Hero_{scene_info}_{cut_info}_hair_{version}.abc")
        setting_node.parm("Export_Cloak").set(f"{output_path}/cloak/Hero_{scene_info}_{cut_info}_cloak_{version}.abc")
        
        hair_node.parm(f"execute").pressButton()
        
        cloak_node.parm(f"execute").pressButton()

main()