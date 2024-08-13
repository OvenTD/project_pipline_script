import maya.cmds as cmds

def get_objects_in_group(group_name, prefix):
    """
    Returns the names of objects in the specified group that start with the given prefix.
    
    Parameters:
    group_name (str): The name of the group to search within.
    prefix (str): The prefix to filter object names.
    
    Returns:
    list: A list of matching object names.
    """
    # Get immediate children in the group
    children = cmds.listRelatives(group_name, children=True, fullPath=True)
    
    # Filter objects by prefix
    if children:
        matching_objects = [child for child in children if child.split('|')[-1].startswith(prefix)]
    else:
        matching_objects = []
    
    return matching_objects

def print_objects_in_group(group_name, prefix):
    """
    Prints the names of objects in the specified group that start with the given prefix.
    
    Parameters:
    group_name (str): The name of the group to search within.
    prefix (str): The prefix to filter object names.
    """
    matching_objects = get_objects_in_group(group_name, prefix)
    
    # Print the matching objects
    print(f"Objects in '{group_name}' starting with '{prefix}':")
    for obj in matching_objects:
        print(obj)

def compare_high_low_objects():
    """
    Compares the objects in 'GEO_High' and 'GEO_Low' groups and prints objects that do not match.
    """
    high_objects = get_objects_in_group("GEO_High", "GEO_High")
    low_objects = get_objects_in_group("GEO_Low", "GEO_Low")
    
    # Extract names without the prefix
    high_names = {obj.split('|')[-1].replace("GEO_High", "") for obj in high_objects}
    low_names = {obj.split('|')[-1].replace("GEO_Low", "") for obj in low_objects}
    
    # Find non-matching objects
    high_only = high_names - low_names
    low_only = low_names - high_names
    
    # Print non-matching objects
    if high_only:
        print("Objects in 'GEO_High' but not in 'GEO_Low':")
        for name in high_only:
            print(f"GEO_High{name}")
    else:
        print("All objects in 'GEO_High' are matched in 'GEO_Low'")
    
    if low_only:
        print("Objects in 'GEO_Low' but not in 'GEO_High':")
        for name in low_only:
            print(f"GEO_Low{name}")
    else:
        print("All objects in 'GEO_Low' are matched in 'GEO_High'")

def selected_obj():
    """
    Returns the currently selected object.
    """
    selected = cmds.ls(selection=True)
    if selected:
        return selected[0]
    else:
        cmds.warning("No object selected.")
        return None

def get_skin_cluster_node(obj):
    """
    Returns the skin cluster node of the given object.
    
    Parameters:
    obj (str): The name of the object.
    
    Returns:
    str: The name of the skin cluster node.
    """
    skin_cluster_nodes = cmds.ls(cmds.listHistory(obj), type="skinCluster")
    if skin_cluster_nodes:
        return skin_cluster_nodes[0]
    else:
        return None

def SelectSkinbindedJoints():
    skinned_object = selected_obj()
    
    if not skinned_object:
        return
    
    skin_cluster_node = get_skin_cluster_node(skinned_object)

    if skin_cluster_node:
        joint_list = cmds.skinCluster(skin_cluster_node, query=True, inf=True)

        print("Joints connected to the skinned object:")
        for joint in joint_list:
            print(joint)
        cmds.select(joint_list)
    else:
        print("No skin cluster node found for the skinned object.")

def skin_bind_and_copy_weights():
    """
    Selects objects in high_objects, gets their skinbinded joints, binds them to the corresponding low_objects,
    and copies skin weights from high_objects to low_objects.
    """
    high_objects = get_objects_in_group("GEO_High", "GEO_High")
    low_objects = get_objects_in_group("GEO_Low", "GEO_Low")

    # Extract names without the prefix
    high_names = [obj.split('|')[-1].replace("GEO_High", "") for obj in high_objects]
    low_dict = {obj.split('|')[-1].replace("GEO_Low", ""): obj for obj in low_objects}

    for high_obj in high_objects:
        # Select high object
        cmds.select(high_obj)
        # Get and select the skin-binded joints of the high object
        SelectSkinbindedJoints()
        
        # Find the corresponding low object
        high_name = high_obj.split('|')[-1].replace("GEO_High", "")
        low_obj = low_dict.get(high_name)
        
        if low_obj:
            # Select the corresponding low object
            cmds.select(low_obj, add=True)
            # Perform skin binding
            cmds.skinCluster(toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1)
            
            # Copy skin weights
            high_skin_cluster = get_skin_cluster_node(high_obj)
            low_skin_cluster = get_skin_cluster_node(low_obj)
            
            if high_skin_cluster and low_skin_cluster:
                cmds.copySkinWeights(ss=high_skin_cluster, ds=low_skin_cluster, noMirror=True, 
                                     surfaceAssociation='closestPoint', influenceAssociation='oneToOne')
            else:
                print(f"Failed to find skin cluster for: {high_obj} or {low_obj}")
        else:
            print(f"No corresponding low object found for: {high_obj}")

def copy_skin_weights_only():
    """
    Copies skin weights from high_objects to corresponding low_objects without binding them.
    """
    high_objects = get_objects_in_group("GEO_High", "GEO_High")
    low_objects = get_objects_in_group("GEO_Low", "GEO_Low")

    # Extract names without the prefix
    high_names = [obj.split('|')[-1].replace("GEO_High", "") for obj in high_objects]
    low_dict = {obj.split('|')[-1].replace("GEO_Low", ""): obj for obj in low_objects}

    for high_obj in high_objects:
        # Find the corresponding low object
        high_name = high_obj.split('|')[-1].replace("GEO_High", "")
        low_obj = low_dict.get(high_name)
        
        if low_obj:
            # Copy skin weights
            high_skin_cluster = get_skin_cluster_node(high_obj)
            low_skin_cluster = get_skin_cluster_node(low_obj)
            
            if high_skin_cluster and low_skin_cluster:
                cmds.copySkinWeights(ss=high_skin_cluster, ds=low_skin_cluster, noMirror=True, 
                                     surfaceAssociation='closestPoint', influenceAssociation='oneToOne')
            else:
                print(f"Failed to find skin cluster for: {high_obj} or {low_obj}")
        else:
            print(f"No corresponding low object found for: {high_obj}")

def create_buttons():
    """
    Creates a UI window with five buttons for printing objects in 'GEO_High' and 'GEO_Low' groups,
    comparing objects between the two groups, selecting skin-binded joints, and copying skin weights.
    """
    if cmds.window("printObjectsWindow", exists=True):
        cmds.deleteUI("printObjectsWindow")

    window = cmds.window("printObjectsWindow", title="Print and Compare Objects", widthHeight=(300, 250))
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.button(label="Print GEO_High Objects", 
                command=lambda x: print_objects_in_group("GEO_High", "GEO_High"))
    
    cmds.button(label="Print GEO_Low Objects", 
                command=lambda x: print_objects_in_group("GEO_Low", "GEO_Low"))
    
    cmds.button(label="Compare GEO_High and GEO_Low Objects", 
                command=lambda x: compare_high_low_objects())
    
    cmds.button(label="Skin Bind and Copy Weights", 
                command=lambda x: skin_bind_and_copy_weights())
    
    cmds.button(label="Copy Skin Weights Only", 
                command=lambda x: copy_skin_weights_only())
    
    cmds.showWindow(window)

# Execute the function to create buttons
create_buttons()
