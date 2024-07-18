import maya.cmds as cmds
import maya.mel as mel
import os

def createInputWindow():
    # Create a window
    if cmds.window("InputSceneAndCut", exists=True):
        cmds.deleteUI("InputSceneAndCut")
    window = cmds.window("InputSceneAndCut", title="Input Scene and Cut", widthHeight=(300, 200))
    
    # Add a layout
    cmds.columnLayout(adjustableColumn=True)
    
    # Add text field for Scene and Cut
    scene_field = cmds.textField(placeholderText="Scene")
    cut_field = cmds.textField(placeholderText="Cut")
    
    # Add some space
    cmds.separator(height=10, style='none')
    
    # Add string field for namespace
    namespace_field = cmds.textField(placeholderText="Namespace")
    
    # Add buttons
    cmds.button(label="Get Namespace", command=lambda *args: getNamespace(namespace_field))
    cmds.button(label="Connect Attributes", command=lambda *args: connectAttributes(namespace_field))
    cmds.button(label="Create HumanIK Character", command=lambda *args: createHumanIKCharacter(namespace_field))
    cmds.button(label="Process Scene and Cut", command=lambda *args: processSceneAndCut(namespace_field, scene_field, cut_field))
    
    # Show the window
    cmds.showWindow(window)

def find_fbx_files(root_dir):
    fbx_file_paths = []
    fbx_file_names = []
    
    # Traverse the directory using os.walk.
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file extension is .fbx.
            if filename.lower().endswith('.fbx'):
                # Add the full path of the .fbx file to the list.
                full_path = os.path.join(dirpath, filename)
                # Replace backslashes with slashes in the path.
                full_path = full_path.replace('\\', '/')
                fbx_file_paths.append(full_path)
                # Add the file name to the list.
                fbx_file_names.append(filename)
    
    return fbx_file_paths, fbx_file_names

def getNamespace(namespace_field):
    selected = cmds.ls(selection=True)
    if selected:
        namespace = selected[0].split(':')[0] if ':' in selected[0] else ''
        cmds.textField(namespace_field, edit=True, text=namespace)
    else:
        cmds.warning("Please select an object to get its namespace.")

def connectAttributes(namespace_field):
    namespace = cmds.textField(namespace_field, query=True, text=True)
    
    for ctrl in joint_pairs_dict:
        destination_object = ctrl
        source_object = joint_pairs_dict[ctrl]

        if namespace:
            destination_object = f"{namespace}:{ctrl}"

        anim_curves = cmds.listConnections(source_object, type='animCurve')
        if anim_curves:
            for anim_curve in anim_curves:
                attribute = anim_curve.split('_')[-1]
                print(source_object, attribute, "->", destination_object, attribute)
                cmds.connectAttr(f'{anim_curve}.output', f"{destination_object}.{attribute}")

def createHumanIKCharacter(namespace_field):
    namespace = cmds.textField(namespace_field, query=True, text=True)
    
    two_arms = [f'{namespace}:FKShoulder_L', f'{namespace}:FKShoulder_R']
    
    for obj in two_arms:
        cmds.setAttr(f"{obj}.rotateX", 0.413)
        cmds.setAttr(f"{obj}.rotateY", -37.1)
        cmds.setAttr(f"{obj}.rotateZ", -1.46)

    # Ensure the HumanIK module is loaded
    if not cmds.pluginInfo('mayaHIK', query=True, loaded=True):
        cmds.loadPlugin('mayaHIK')

    # Open the HumanIK Character Controls window
    mel.eval('HIKCharacterControlsTool')

    # Create a HumanIK character (e.g., named 'Character1')
    character_name = f'{namespace}HumanIK'
    mel.eval(f'hikCreateCharacter("{character_name}")')
    
    # Assign joints to HumanIK character
    for joint in joint_pairs_dict:
        full_joint_name = f'{namespace}:{joint}' if namespace else joint
        try:
            cmds.connectAttr(f'{full_joint_name}.Character', f'{character_name}.{joint_pairs_dict[joint]}', force=True)
        except Exception as e:
            cmds.warning(f"Failed to connect {full_joint_name} to {character_name}.{joint_pairs_dict[joint]}: {e}")

def processSceneAndCut(namespace_field, scene_field, cut_field):
    namespace = cmds.textField(namespace_field, query=True, text=True)
    scene_value = cmds.textField(scene_field, query=True, text=True)
    cut_value = cmds.textField(cut_field, query=True, text=True)

    try:
        scene_int = int(scene_value)
        cut_int = int(cut_value)
    except ValueError:
        cmds.warning("Scene and Cut fields must be integers.")
        return

    if 'Bille' in namespace:
        character_name = 'Bille'
    elif 'Hero' in namespace:
        character_name = 'Hero'
    elif 'Devi' in namespace:
        character_name = 'Devi'
    else:
        character_name = 'Extra'

    root_directory = 'D:/Hijackers/MotionCaptureData/Baked'
    scene_directory = f'{root_directory}/Scene{scene_int:02d}'
    char_directory = f'{scene_directory}/{character_name}'

    fbx_file_paths, fbx_file_names = find_fbx_files(char_directory)

    # Format to look for
    search_prefix = f'{scene_int}-{cut_int}'

    # Find matching files and their indices
    matching_indices = [i for i, file_name in enumerate(fbx_file_names) if file_name.startswith(search_prefix)]

    if not matching_indices:
        cmds.warning("No matching files found.")
        return

    global searched_fbxes
    searched_fbxes = [fbx_file_names[i] for i in matching_indices]
    
    # Show a window with the list of matching files
    createFBXSelectionWindow()

def createFBXSelectionWindow():
    if cmds.window("FBXSelectionWindow", exists=True):
        cmds.deleteUI("FBXSelectionWindow")
    
    window = cmds.window("FBXSelectionWindow", title="Select FBX File", widthHeight=(300, 200))
    cmds.columnLayout(adjustableColumn=True)

    global fbx_radio_collection
    fbx_radio_collection = cmds.radioCollection()

    for fbx in searched_fbxes:
        cmds.radioButton(label=fbx)

    cmds.button(label="Process Selected FBX", command=processSelectedFBX)
    
    cmds.showWindow(window)

def processSelectedFBX(*args):
    selected_fbx = cmds.radioCollection(fbx_radio_collection, query=True, select=True)
    print(f"Processing selected FBX: {selected_fbx}")
    # Further processing of the selected FBX file can be done here

# Create the input window
createInputWindow()

joint_pairs_dict = {
    'HipSwinger_M': 'Hips',
    'FKHip_R': 'RightUpLeg',
    'FKKnee_R': 'RightLeg',
    'FKAnkle_R': 'RightFoot',
    'FKToes_R': 'RightToeBase',
    'FKHip_L': 'LeftUpLeg',
    'FKKnee_L': 'LeftLeg',
    'FKAnkle_L': 'LeftFoot',
    'FKToes_L': 'LeftToeBase',
    'FKScapula_L': 'LeftShoulder',
    'FKScapula_R': 'RightShoulder',
    'FKShoulder_L': 'LeftArm',
    'FKElbow_L': 'LeftForeArm',
    'FKWrist_L': 'LeftHand',
    'FKShoulder_R': 'RightArm',
    'FKElbow_R': 'RightForeArm',
    'FKWrist_R': 'RightHand',
    'FKHead_M': 'Head',
    'FKNeck_M': 'Neck',
    'FKChest_M': 'Spine1',
    'FKSpine1_M': 'Spine'
}
