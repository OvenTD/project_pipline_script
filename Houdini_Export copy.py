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
    version = 1

    file_list = files()
    """['S01_0010', 'S01_0020', 'S01_0040', 
                      'S01_0050', 'S01_0100', 'S01_0110', 'S01_0140', 
                      'S01_0170', 'S01_0190', 'S01_0270', 'S01_0280', 
                      'S01_0290', 'S01_0300', 'S01_0323', 'S01_0323', 
                      'S01_0325', 'S01_0330', 'S01_0330', 'S01_0340']"""
    root_file_list = ["S02_0090",'S02_0115','S04_0010','S02_0050','S02_0170','S02_0180']
    
    
    scene_cut_list = ['S04_0110']

    input_file_list = get_abc_file_list(input_path)
    print(input_file_list)

    
    #
    for scene_cut in scene_cut_list:
        tmp_import_list =[]
        
        for file in file_list:
            if scene_cut in file:
                tmp_import_list.append(file)
                
        for input in tmp_import_list:
            if "eyebrow" in input:
                eyebrow_abc = input
                continue
            elif "scalp" in input:
                scalp_abc = input
                continue
            elif "collision" in input:
                collision_abc = input
                continue
                
        
        
        info_list = eyebrow_abc.split("_")

        scene_info, cut_info, start_frame, end_frame, state_info, char_name ,type_info = info_list
        

        input_node = hou.node("/obj/Input_Control")

        if state_info == "move":
            export_hair_node = hou.node("/obj/Sim_Export/Rop_Hair")
            export_eyebrow_node = hou.node("/obj/Sim_Export/Rop_Eyebrow")
            input_node.parm("OutputABC").set(f"{output_path}/move/") 
        elif state_info == "static":
            export_hair_node = hou.node("/obj/Sta_Export/Rop_Hair")
            export_eyebrow_node = hou.node("/obj/Sta_Export/Rop_Eyebrow")
            input_node.parm("OutputABC").set(f"{output_path}/static/")
        
        input_node.parm("Anim_Scalp").set(f"{folder_path}/{scalp_abc}") 
        input_node.parm("Anim_Eyebrow").set(f"{folder_path}/{eyebrow_abc}") 
        input_node.parm("collisionSkin").set(f"{folder_path}/{collision_abc}") 
        
        input_node.parmTuple("renderFrame").set((start_frame, end_frame))

        for i in hair_or_eyebrow:
            file_name = f"{scene_info}_{cut_info}_{char_name}Char{i}_v0{version}"
            print()
            print(file_name,"rendering")
            input_node.parm("FileName").set(file_name) 
            if i == "Hair":
                if state_info == "static":
                    continue
                print()
                export_hair_node.parm(f"execute").pressButton()
            elif i == "Eyebrow":
                print()
                export_eyebrow_node.parm(f"execute").pressButton()

            print(file_name,"finished")
            print()
            file_path = f"G:/내 드라이브/Houdini_render_state/finished_{file_name}.txt"
            try:
                with open(file_path, "w"):
                    pass
                print(f": {file_path}")
            except Exception as e:
                print(f"Error: {str(e)}")