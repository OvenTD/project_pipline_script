import maya.cmds as cmds
import maya.mel as mel
import os

class SceneProcessor:
    def __init__(self):
        self.scene = None
        self.cut = None
        self.namespace = ""
        self.directory = None
        self.searched_fbxes = None
        self.selected_fbx = None
        self.character_name = None
        self.root_directory = 'D:/Hijackers/MotionCaptureData/Baked'
        self.scene_directory = None
        self.fbx_file_paths = None
        self.fbx_file_names = None
        self.mocap_namespace = None
        self.character_rotation_offset = None
        self.joint_pairs_dict = {
            'RootX_M': 'Hips',
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
        self.humanik_code={
            'Reference':0,
            'Hips' : 1,
            'LeftUpLeg':2,
            'LeftLeg':3,
            'LeftFoot':4,
            'RightUpLeg':5,
            'RightLeg':6,
            'RightFoot':7,
            'Spine':8,
            'LeftArm':9,
            'LeftForeArm':10,
            'LeftHand':11,
            'RightArm':12,
            'RightForeArm':13,
            'RightHand':14,
            'Head':15,
            'LeftToeBase':16,
            'RightToeBase':17,
            'LeftShoulder':18,
            'RightShoulder':19,
            'Neck':20,
            #21 and 22 are extra wrists
            'Spine1':23,
            'Spine2':24,
            'Spine3':25,
            #26-32 are additional spines

        }

    def createInputWindow(self):
        # Create a window
        if cmds.window("InputSceneAndCut", exists=True):
            cmds.deleteUI("InputSceneAndCut")
        window = cmds.window("InputSceneAndCut", title="Input Scene and Cut", widthHeight=(300, 400))
        
        # Add a layout
        cmds.columnLayout(adjustableColumn=True)
        
        # Add text field for Scene and Cut
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(80, 200))
        cmds.text(label="Scene:")
        self.scene_field = cmds.intField(annotation="Scene", value=1)
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(80, 200))
        cmds.text(label="Cut:")
        self.cut_field = cmds.intField(annotation="Cut", value=35)
        cmds.setParent("..")
        
        # Add text field for namespace (read-only)
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(80, 200))
        cmds.text(label="Namespace:")
        self.namespace_field = cmds.textField(text=self.namespace, editable=False)
        cmds.setParent("..")
        
        # Add buttons
        cmds.button(label="Get Namespace", command=self.getNamespace)
        cmds.button(label="Connect Attributes", command=self.connectAttributes)
        cmds.button(label="Create HumanIK Character", command=self.createHumanIKCharacter)
        cmds.button(label="Process Scene and Cut", command=self.processSceneAndCut)
        
        # Add textScrollList for showing FBX files
        self.fbx_scroll_list = cmds.textScrollList(height=100, allowMultiSelection=False)
        
        # Add a button to process the selected FBX
        cmds.button(label="Process Selected FBX", command=self.processSelectedFBX)
        
        # Show the window
        cmds.showWindow(window)

    def getNamespace(self, *args):
        selected = cmds.ls(selection=True)
        if selected:
            self.namespace = selected[0].split(':')[0] if ':' in selected[0] else ''
            cmds.textField(self.namespace_field, edit=True, text=self.namespace)
        else:
            cmds.warning("Please select an object to get its namespace.")

    def connectAttributes(self, *args):
        namespace = cmds.textField(self.namespace_field, query=True, text=True)
        
        for ctrl in self.joint_pairs_dict:
            destination_object = ctrl
            source_object = self.joint_pairs_dict[ctrl]
    
            if namespace:
                destination_object = f"{namespace}:{ctrl}"
    
            anim_curves = cmds.listConnections(source_object, type='animCurve')
            if anim_curves:
                for anim_curve in anim_curves:
                    attribute = anim_curve.split('_')[-1]
                    print(source_object, attribute, "->", destination_object, attribute)
                    cmds.connectAttr(f'{anim_curve}.output', f"{destination_object}.{attribute}")

    def createHumanIKCharacter(self, *args):
        namespace = cmds.textField(self.namespace_field, query=True, text=True)
        
        two_arms = [f'{namespace}:FKShoulder_L', f'{namespace}:FKShoulder_R']
        
        FKIK_list = ['FKIKLeg_R','FKIKLeg_L','FKIKArm_L','FKIKArm_R']
        for i in FKIK_list:
            cmds.setAttribute(f'{i}.FKIKBlend',0)


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
        Char_HumanIK = f'{namespace}HumanIK'
        mel.eval(f'hikCreateCharacter("{Char_HumanIK}")')
        
        # Assign joints to HumanIK character
        self.assignJointsToHumanIKCharacter(Char_HumanIK,namespace,False)

    def processSceneAndCut(self, *args):
        cmds.namespace( set=':' )
        self.scene = cmds.intField(self.scene_field, query=True, value=True)
        self.cut = cmds.intField(self.cut_field, query=True, value=True)
        self.namespace = cmds.textField(self.namespace_field, query=True, text=True)
        
        if not self.namespace:
            cmds.warning("Please select an object to get its namespace.")
            return
        
        if 'Bille' in self.namespace:
            self.character_name = 'Bille'
            self.character_rotation_offset = [0.413, -37.1,-1.46]
        elif 'Hero' in self.namespace:
            self.character_name = 'Hero'
            self.character_rotation_offset = [0.053, -46.807,2.471]
        elif 'Devi' in self.namespace:
            self.character_name = 'Devi'
            self.character_rotation_offset = [0.413, -37.1,-1.46]
        else:
            self.character_name = 'Extra'
            self.character_rotation_offset = [0.413, -37.1,-1.46]
    
        self.scene_directory = f'{self.root_directory}/Scene{self.scene:02d}/{self.character_name}'
    
        self.fbx_file_paths, self.fbx_file_names = self.find_fbx_files(self.scene_directory)
    
        # Format to look for
        search_prefix = f'{self.scene}-{self.cut}'
    
        # Find matching files and their indices
        matching_indices = [i for i, file_name in enumerate(self.fbx_file_names) if file_name.startswith(search_prefix)]
    
        if not matching_indices:
            cmds.warning("No matching files found.")
            return
    
        self.searched_fbxes = [self.fbx_file_names[i] for i in matching_indices]
        
        # Update the textScrollList with the matching files
        cmds.textScrollList(self.fbx_scroll_list, edit=True, removeAll=True)
        for fbx in self.searched_fbxes:
            cmds.textScrollList(self.fbx_scroll_list, edit=True, append=fbx)

    def find_fbx_files(self,root_dir):
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

    def processSelectedFBX(self, *args):
        selected_fbx = cmds.textScrollList(self.fbx_scroll_list, query=True, selectItem=True)
        if not selected_fbx:
            cmds.warning("No FBX file selected.")
            return
        self.selected_fbx = selected_fbx[0]
        fbx_file_path = f"{self.scene_directory}/{self.selected_fbx}"

        self.mocap_namespace = "motionCaptureData"
        
        if cmds.namespace( exists=self.mocap_namespace )==False:
            if cmds.namespaceInfo( currentNamespace=True )!=self.mocap_namespace:
                cmds.namespace( add=self.mocap_namespace )  
        try:cmds.namespace( set=self.mocap_namespace )
        except:print("No namespace")
        cmds.file(fbx_file_path, i=True, type="FBX", ignoreVersion=True, ra=True, namespace=self.mocap_namespace)
        cmds.namespace( set=':' )
                # Ensure the HumanIK module is loaded
        if not cmds.pluginInfo('mayaHIK', query=True, loaded=True):
            cmds.loadPlugin('mayaHIK')
    
        # Open the HumanIK Character Controls window
        mel.eval('HIKCharacterControlsTool')
    
        # Create a HumanIK character (e.g., named 'Character1')
        MotionCaptueHumanIK = f'MotionCaptureHumanIK'
        mel.eval(f'hikCreateCharacter("{MotionCaptueHumanIK}")')
        
        # Assign joints to HumanIK character
        for joint in self.joint_pairs_dict:
            full_joint_name = f'{self.mocap_namespace}:{self.joint_pairs_dict[joint]}'
            
            self.assignJointsToHumanIKCharacter(MotionCaptueHumanIK,self.mocap_namespace,True)
            # try:
            #     cmds.connectAttr(f'{full_joint_name}.Character', f'{MotionCaptueHumanIK}.{self.joint_pairs_dict[joint]}', force=True)
            # except Exception as e:
            #     cmds.warning(f"Failed to connect {full_joint_name} to {MotionCaptueHumanIK}.{self.joint_pairs_dict[joint]}: {e}")

    def assignJointsToHumanIKCharacter(self, humanIK, namespace,IsMocap):
        
        for joint, hik_joint in self.joint_pairs_dict.items():
            if IsMocap:
                full_joint_name = f'{namespace}:{hik_joint}'
            else:
                full_joint_name = f'{namespace}:{joint}'
            mel_command = f'setCharacterObject("{full_joint_name}","{humanIK}",{self.humanik_code[hik_joint]},0);'
            try:
                mel.eval(mel_command)
            except Exception as e:
                cmds.warning(f"Failed to assign {full_joint_name} to {humanIK}.{hik_joint}: {e}")

# Instantiate the SceneProcessor class and create the input window
processor = SceneProcessor()
processor.createInputWindow()
