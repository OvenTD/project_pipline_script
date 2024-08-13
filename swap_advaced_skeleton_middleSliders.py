import maya.cmds as cmds

def swap_and_rename_sliders(suffix1, suffix2):
    # Get selected objects
    selected_objects = cmds.ls(selection=True)
    
    if not selected_objects:
        cmds.warning("No objects selected.")
        return

    # List to store found objects
    obj1 = None
    obj2 = None

    # Iterate through each selected object and their children
    for obj in selected_objects:
        children = cmds.listRelatives(obj, allDescendents=True)
        
        if not children:
            continue
        
        for child in children:
            if child.endswith(suffix1):
                obj1 = child
            elif child.endswith(suffix2):
                obj2 = child

    if not obj1 or not obj2:
        cmds.warning("Couldn't find the required objects.")
        return

    # Extract parent paths
    parent1 = obj1.rsplit('|', 1)[0]
    parent2 = obj2.rsplit('|', 1)[0]

    # Rename obj1 to a temporary name
    temp_name = f"{parent1}|temp_{suffix1}"
    obj1 = cmds.rename(obj1, temp_name)

    # Swap names
    new_name1 = f"{parent2}"
    new_name2 = f"{parent1}"

    obj2 = cmds.rename(obj2, new_name2)
    obj1 = cmds.rename(obj1, new_name1)

# Create buttons to execute the functions
if cmds.window('swapSliderNamesWindow', exists=True):
    cmds.deleteUI('swapSliderNamesWindow')

cmds.window('swapSliderNamesWindow', title='Swap Slider Names', widthHeight=(200, 100))
cmds.columnLayout(adjustableColumn=True)
cmds.button(label='Swap middleSlider0 and middleSlider2', command=lambda x: swap_and_rename_sliders('middleSlider0', 'middleSlider2'))
cmds.button(label='Swap middleSlider1 and middleSlider3', command=lambda x: swap_and_rename_sliders('middleSlider1', 'middleSlider3'))
cmds.showWindow('swapSliderNamesWindow')
