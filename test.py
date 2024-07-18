import maya.cmds as cmds
import maya.mel as mel

# Ensure the HumanIK module is loaded
if not cmds.pluginInfo('mayaHIK', query=True, loaded=True):
    cmds.loadPlugin('mayaHIK')

# Open the HumanIK Character Controls window
mel.eval('HIKCharacterControlsTool')

# Create a HumanIK character (e.g., named 'Character1')
character_name = 'Character1'
mel.eval(f'hikCreateCharacter("{character_name}")')

# # Define the specific joint (e.g., 'LeftUpLeg' joint)
# left_up_leg_joint = 'Bille_Rigging:FKHip_L'

# # Check if the joint exists, and create it if it does not
# if not cmds.objExists(left_up_leg_joint):
#     cmds.joint(name=left_up_leg_joint, position=(0, 10, 0))

# # Enable HumanIK definition edit mode
# mel.eval('hikUpdateDefinitionUI()')

# # Function to set the HumanIK joint definition
# def set_humanik_joint(character, hik_joint, joint_name):
#     mel.eval(f'setCharacterObject("{character}", {hik_joint}, "{joint_name}")')

# # HumanIK definition joint index constants (e.g., HIKLeftUpLeg is 9)
# HIKLeftUpLeg = 9

# # Assign the actual joint to the defined HumanIK joint
# set_humanik_joint(character_name, HIKLeftUpLeg, left_up_leg_joint)

# # Apply the HumanIK definition updates
# mel.eval('hikUpdateDefinitionUI()')

# cmds.connectAttribute(f"Bille_Rigging:FKSpine1_M.Character", f"Character1.Spine")
joint = 'Bille_Rigging:FKShoulder_L'
cmds.connectAttr(f'{joint}.Character', f'{character_name}.RightUpLeg', force=True)

import maya.cmds as cmds
import maya.mel as mel
def createInputWindow():
    # Create a window
    if cmds.window("InputSceneAndCut", exists=True):
        cmds.deleteUI("InputSceneAndCut")
    window = cmds.window("InputSceneAndCut", title="Input Scene and Cut", widthHeight=(300, 150))
    
    # Add a layout
    cmds.columnLayout(adjustableColumn=True)
    
    # Add text field for Scene and Cut
    scene_field = cmds.textField(text="", placeholderText="Scene")
    cut_field = cmds.textField(text="", placeholderText="Cut")
    
    # Add string field for namespace
    namespace_field = cmds.textField(text="", placeholderText="Namespace")
    
    # Add buttons
    cmds.button(label="Get Namespace", command=lambda *args: getNamespace(namespace_field))
    cmds.button(label="Connect Attributes", command=lambda *args: connectAttributes(scene_field, cut_field, namespace_field))
    cmds.button(label="Cancel", command=lambda *args: onCancel(window,namespace_field))
    
    # Show the window
    cmds.showWindow(window)

def getNamespace(namespace_field):
    selected = cmds.ls(selection=True)
    if selected:
        namespace = selected[0].split(':')[0] if ':' in selected[0] else ''
        cmds.textField(namespace_field, edit=True, text=namespace)
    else:
        cmds.warning("Please select an object to get its namespace.")

def connectAttributes(scene_field, cut_field, namespace_field):
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
                print(source_object,attribute,"->",destination_object,attribute)
                cmds.connectAttr(f'{anim_curve}.output', f"{destination_object}.{attribute}")

def onCancel(window, namespace_field):
    namespace = cmds.textField(namespace_field, query=True, text=True)
    # Ensure the HumanIK module is loaded
    if not cmds.pluginInfo('mayaHIK', query=True, loaded=True):
        cmds.loadPlugin('mayaHIK')

    # Open the HumanIK Character Controls window
    mel.eval('HIKCharacterControlsTool')

    # Create a HumanIK character (e.g., named 'Character1')
    character_name = 'Character1'
    mel.eval(f'hikCreateCharacter("{character_name}")')
    for joint in joint_pairs_dict:
        cmds.connectAttr(f'{namespace}:{joint}.Character', f'{character_name}.{joint_pairs_dict[joint]}', force=True)


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
    'FKShoulder_R': 'RightArm',
    'FKElbow_R': 'RightForeArm',
    'FKWrist_R': 'RightHand',
    'FKHead_M': 'Head',
    'FKNeck_M': 'Neck',
    'FKChest_M': 'Spine3',
    'FKSpine1_M': 'Spine1'
}
#0.413, -37.1, -1.46
keys_list = list(joint_pairs_dict.keys())
