import maya.cmds as cmds
import pyperclip

# Define the function to create a new scene
def new_scene():
    cmds.file(new=True, force=True)

# Define the function to rename the selected group
def rename_group():
    # Get the asset name from the text field
    asset_name = cmds.textField('assetNameField', query=True, text=True)
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
    # Get the asset name from the text field
    asset_name = cmds.textField('assetNameField', query=True, text=True)
    selected_objects = cmds.ls(selection=True)
    if selected_objects:
        if asset_name:
            group_name = f"AST_{asset_name}_00"
        else:
            group_name = "AST_default_00"
        cmds.group(selected_objects, name=group_name)
    else:
        cmds.warning("No objects selected to group.")

# Define the function to prefix selected objects with asset name
def prefix_selected():
    # Get the asset name from the text field
    asset_name = cmds.textField('assetNameField', query=True, text=True)
    if asset_name:
        selected_objects = cmds.ls(selection=True)
        if selected_objects:
            for obj in selected_objects:
                new_name = f"{asset_name}_{obj}"
                cmds.rename(obj, new_name)
        else:
            cmds.warning("No objects selected to rename.")
    else:
        cmds.warning("Please enter an asset name.")

# Define the function to create and assign AI Standard Surface material
def assign_material():
    # Get the asset name from the text field
    asset_name = cmds.textField('assetNameField', query=True, text=True)
    if asset_name:
        selected_objects = cmds.ls(selection=True)
        if selected_objects:
            # Create AI Standard Surface material
            shader_name = f"TEX_{asset_name}"
            shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=shader_name)
            
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

# Define the function to copy text to clipboard
def copy_to_clipboard():
    text_to_copy = "Modeling"
    pyperclip.copy(text_to_copy)

# Function to create the UI with buttons and a text field
def create_new_scene_button():
    # Delete the window if it already exists
    if cmds.window("newSceneWindow", exists=True):
        cmds.deleteUI("newSceneWindow")
    
    # Create a new window
    window = cmds.window("newSceneWindow", title="New Scene Creator", widthHeight=(200, 270))
    cmds.columnLayout(adjustableColumn=True)
    
    # Create the button to create a new scene
    cmds.button(label="New Scene", command=lambda x: new_scene())
    
    # Create the text field for asset name
    cmds.textField('assetNameField', placeholderText='Enter asset name...')
    
    # Create the button to group selected objects
    cmds.button(label="Group Selected", command=lambda x: group_selected())
    
    # Create the button to rename the selected object
    cmds.button(label="Rename Group", command=lambda x: rename_group())

    # Create the button to prefix selected objects with asset name
    cmds.button(label="Prefix Selected", command=lambda x: prefix_selected())
    
    # Create the button to create and assign AI Standard Surface material
    cmds.button(label="Assign Material", command=lambda x: assign_material())
    
    # Create the button to copy "Modeling" to clipboard
    cmds.button(label="Copy to Clipboard", command=lambda x: copy_to_clipboard())
    
    # Show the window
    cmds.showWindow(window)

# Call the function to create the UI
create_new_scene_button()
