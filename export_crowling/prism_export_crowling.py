import maya.cmds as cmds
import os
import cv2
import numpy as np
import pyautogui
import time

# Global delay time (in seconds) between actions
DELAY_TIME = 0.5
DELAY_BETWEEN_CLICKS = 1.0  # Delay time between ABC and MB type button clicks

# Image search and click function with return to original mouse position
def find_and_click_image(image_path):
    # Get the current mouse position
    original_position = pyautogui.position()
    
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    # Load the image to search for
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    # Find the best match location
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Set a threshold to determine if the match is good enough
    threshold = 0.8
    if max_val >= threshold:
        # Calculate the center of the matched image
        img_w, img_h = template.shape[1], template.shape[0]
        center_x = max_loc[0] + img_w // 2
        center_y = max_loc[1] + img_h // 2
        
        # Click on the found location
        pyautogui.click(center_x, center_y)
        
    else:
        print(f"Image not found: {image_path}")
    
    # Return to the original mouse position
    pyautogui.moveTo(original_position)

# Functions to click specific buttons
def click_export_button():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\export_button.png')

def click_prism_export_button():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\prism_export_button.PNG')

def click_abc_type_button():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\abc_type_button.png')

def click_mb_type_button():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\mb_type_button.png')

def click_comment_textfield():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\comment_textfield.png')

def type_selected_folder_name():
    # Type the selected folder name
    selected_folder = cmds.textScrollList("folderList", query=True, selectItem=True)
    if selected_folder:
        pyautogui.typewrite(selected_folder[0])
    else:
        print("No folder selected to type.")

# Function to create a new scene
def create_new_scene():
    cmds.file(new=True, force=True)

# Function to rename selected objects based on asset name
def rename_selected_objects(asset_name):
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("No objects selected.")
        return
    
    for index, obj in enumerate(selected_objects):
        new_name = f"AST_{asset_name}_{index:02d}"
        cmds.rename(obj, new_name)

# Function to rename selected objects based on folder name
def rename_group():
    selected_folder = cmds.textScrollList("folderList", query=True, selectItem=True)
    if not selected_folder:
        cmds.warning("No folder selected.")
        return
    
    folder_name = selected_folder[0]
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("No objects selected.")
        return
    
    for index, obj in enumerate(selected_objects):
        new_name = f"AST_{folder_name}_{index:02d}"
        cmds.rename(obj, new_name)

# Function to add a prefix to selected objects based on folder name
def add_prefix_to_selected_objects():
    selected_folder = cmds.textScrollList("folderList", query=True, selectItem=True)
    if not selected_folder:
        cmds.warning("No folder selected.")
        return
    
    folder_name = selected_folder[0]
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("No objects selected.")
        return
    
    for obj in selected_objects:
        new_name = f"{folder_name}_{obj}"
        cmds.rename(obj, new_name)

# Function to load folder names into a text scroll list
def load_folders_to_list():
    #directory_path = r"D:\Hijackers\Prism\VillanDies\03_Production\Assets\environment\asset\lab"
    directory_path = r"D:\Hijackers\Prism\VillanDies\03_Production\Assets\environment\asset\Square"
    
    cmds.textScrollList("folderList", edit=True, removeAll=True)
    
    if os.path.exists(directory_path):
        folders = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]
        for folder in folders:
            cmds.textScrollList("folderList", edit=True, append=folder)
    else:
        cmds.warning("Directory does not exist.")
def rename_group():
    selected_folder = cmds.textScrollList("folderList", query=True, selectItem=True)
    if not selected_folder:
        cmds.warning("No folder selected.")
        return
    
    # Get the asset name from the text field
    asset_name = selected_folder[0]
    if asset_name:
        selected_objects = cmds.ls(selection=True)
        if selected_objects:
            new_name = f"AST_{asset_name}_00"
            cmds.rename(selected_objects[0], new_name)
        else:
            cmds.warning("No object selected to rename.")
    else:
        cmds.warning("Please enter an asset name.")

# Define the function to group selected objects
def group_selected():
    selected_folder = cmds.textScrollList("folderList", query=True, selectItem=True)
    if not selected_folder:
        cmds.warning("No folder selected.")
        return
    
    # Get the asset name from the text field
    asset_name = selected_folder[0]
    selected_objects = cmds.ls(selection=True)
    if selected_objects:
        if asset_name:
            group_name = f"AST_{asset_name}_00"
        else:
            group_name = "AST_default_00"
        cmds.group(selected_objects, name=group_name)
    else:
        cmds.warning("No objects selected to group.")



# Define the function to create and assign AI Standard Surface material
def assign_material():
    selected_folder = cmds.textScrollList("folderList", query=True, selectItem=True)
    if not selected_folder:
        cmds.warning("No folder selected.")
        return
    
    # Get the asset name from the text field
    asset_name = selected_folder[0]
    if asset_name:
        selected_objects = cmds.ls(selection=True)
        if selected_objects:
            # Create AI Standard Surface material
            shader_name = f"TEX_{asset_name}"
            shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)
            
            # Assign material to selected objects
            for obj in selected_objects:
                shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{shader_name}SG")
                cmds.connectAttr(f"{shader}.outColor", f"{shading_group}.surfaceShader", force=True)
                cmds.select(obj, replace=True)
                cmds.hyperShade(assign=shader_name)
        else:
            cmds.warning("No objects selected to apply material.")
    else:
        cmds.warning("Please enter an asset name.")

# Function to display the UI
def show_ui():
    if cmds.window("newSceneWindow", exists=True):
        cmds.deleteUI("newSceneWindow", window=True)
    
    window = cmds.window("newSceneWindow", title="New Scene Creator", widthHeight=(300, 400))
    
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Create New Scene", command=lambda *args: create_new_scene())
    cmds.button(label="Load Folder Names", command=lambda *args: load_folders_to_list())
    cmds.textScrollList("folderList", numberOfRows=8, allowMultiSelection=False)
    
    cmds.separator(height=10)
    cmds.button(label="Group Selected", command=lambda x: group_selected())
    cmds.button(label="Rename Group", command=lambda *args: rename_group())
    cmds.button(label="Rename Selected Objects", command=lambda *args: rename_selected_objects(cmds.textScrollList("folderList", query=True, selectItem=True)[0]))
    cmds.button(label="Add Prefix", command=lambda *args: add_prefix_to_selected_objects())

    
    
    # Create the button to create and assign AI Standard Surface material
    cmds.button(label="Assign Material", command=lambda x: assign_material())
    
    
    
    cmds.showWindow(window)

# Display the UI
show_ui()
