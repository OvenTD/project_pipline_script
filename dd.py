import maya.cmds as cmds
import maya.mel as mel
import os
import math

class SceneProcessor:
    def __init__(self):
        self.scene = None
        self.cut = None
        self.namespace = ""
        self.directory = None
        self.searched_fbxes = None
        self.character_name = None
        self.root_directory = 'D:/Hijackers/MotionCaptureData/Baked'
        self.scene_directory = None
        self.fbx_file_paths = None
        self.fbx_file_names = None
        self.mocap_namespace = "motionCaptureData"
        self.reference_joint = f'{self.mocap_namespace}:Reference'
        self.character_rotation_offset = None
        self.char_human_ik = None
        self.mocap_human_ik = 'MotionCaptureHumanIK'
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
            'Spine1':23,
            'Spine2':24,
            'Spine3':25,
        }
        self.arm_offset_data = {
            'Bille': [0.413, -37.1, -1.46],
            'Hero': [0.053, -46.807, 2.471],
            'Devi': [0.413, -37.1, -1.46]
        }

    def createInputWindow(self):
        if cmds.window("InputSceneAndCut", exists=True):
            cmds.deleteUI("InputSceneAndCut")
        window = cmds.window("InputSceneAndCut", title="Input Scene and Cut", widthHeight=(300, 400))
        
        cmds.columnLayout(adjustableColumn=True)
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(80, 200))
        cmds.text(label="Scene:")
        self.scene_field = cmds.intField(annotation="Scene", value=1)
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(80, 200))
        cmds.text(label="Cut:")
        self.cut_field = cmds.intField(annotation="Cut", value=15)
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(80, 200))
        cmds.text(label="Namespace:")
        self.namespace_field = cmds.textField(text=self.namespace, editable=False)
        cmds.setParent("..")
        
        cmds.button(label="Get Namespace", command=self.get_namespace)
        cmds.button(label="Process Scene and Cut", command=self.processSceneAndCut)
        
        self.fbx_scroll_list = cmds.textScrollList(height=100, allowMultiSelection=False)
        
        cmds.button(label="Process Selected FBX", command=self.processSelectedFBX)
        
        cmds.showWindow(window)

    def get_namespace(self, *args):
        selected = cmds.ls(selection=True)
        if selected:
            self.namespace = selected[0].split(':')[0] if ':' in selected[0] else ''
            cmds.textField(self.namespace_field, edit=True, text=self.namespace)
        else:
            cmds.warning("Please select an object to get its namespace.")

    def createHumanIKCharacter(self, *args):
        
        self.set_fkikblend_0()
        self.set_arm_rotation_offset()
    
        self.set_hik_plugin()
    
        self.char_human_ik = f'{self.character_name}HumanIK'
        self.initialize_humanik_character(self.char_human_ik)

        self.assignJointsToHumanIKCharacter(self.char_human_ik,self.namespace,False)
    def set_fkikblend_0(self):
        FKIK_list = [f'{self.namespace}:FKIKLeg_R',f'{self.namespace}:FKIKLeg_L',
                     f'{self.namespace}:FKIKArm_L',f'{self.namespace}:FKIKArm_R']
        for i in FKIK_list:
            cmds.setAttr(f'{i}.FKIKBlend',0)
        
    
    def set_arm_rotation_offset(self):
        two_arms = [f'{self.namespace}:FKShoulder_L', f'{self.namespace}:FKShoulder_R']
        for obj in two_arms:
            cmds.setAttr(f"{obj}.rotateX", self.character_rotation_offset[0])
            cmds.setAttr(f"{obj}.rotateY", self.character_rotation_offset[1])
            cmds.setAttr(f"{obj}.rotateZ", self.character_rotation_offset[2])

    def processSceneAndCut(self, *args):
        self.scene = cmds.intField(self.scene_field, query=True, value=True)
        self.cut = cmds.intField(self.cut_field, query=True, value=True)
        
        self.set_character_namespace()
    
        self.scene_directory = f'{self.root_directory}/Scene{self.scene:02d}/{self.character_name}'
    
        self.fbx_file_paths, self.fbx_file_names = self.find_fbx_files(self.scene_directory)
    
        scene_cut_matched_fbxes =self.find_scene_cut_matched_files()
        
        self.update_textscroll(scene_cut_matched_fbxes)

    def set_character_namespace(self):
        self.namespace = cmds.textField(self.namespace_field, query=True, text=True)
        
        character_name = self.namespace.split('_')[0]
        if character_name in self.arm_offset_data:
            self.character_name = character_name
            self.character_rotation_offset = self.arm_offset_data[character_name]
            
        else:
            self.character_name = 'Extra'
            self.character_rotation_offset = [0.413, -37.1, -1.46]

    def find_scene_cut_matched_files(self):
        search_prefix = f'{self.scene}-{self.cut}'
    
        matching_indices = [i for i, file_name in enumerate(self.fbx_file_names) if file_name.startswith(search_prefix)]

        if not matching_indices:
            cmds.warning("No matching files found.")
            return
    
        return [self.fbx_file_names[i] for i in matching_indices]

    def find_fbx_files(self, root_dir):
        fbx_file_paths = []
        fbx_file_names = []
        
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.lower().endswith('.fbx'):
                    full_path = os.path.join(dirpath, filename)
                    full_path = full_path.replace('\\', '/')
                    fbx_file_paths.append(full_path)
                    fbx_file_names.append(filename)
        
        return fbx_file_paths, fbx_file_names
    def update_textscroll(self,scene_cut_matched_fbxes):
        cmds.textScrollList(self.fbx_scroll_list, edit=True, removeAll=True)
        for fbx in scene_cut_matched_fbxes:
            cmds.textScrollList(self.fbx_scroll_list, edit=True, append=fbx)
        
    def processSelectedFBX(self, *args):
        self.createHumanIKCharacter()

        fbx_file_path = self.get_selected_fbx_returns_fbx_path()

        self.set_motion_capture_namespace()
        self.import_fbx(fbx_file_path)
        self.reset_namespace()

        self.set_hik_plugin()
    
        self.initialize_humanik_character(self.mocap_human_ik)

        self.assignJointsToHumanIKCharacter(self.mocap_human_ik, self.mocap_namespace, IsMocap=True)
 
        self.update_humanik_ui()

        self.select_hik_character(self.char_human_ik)
        self.select_hik_source(self.mocap_human_ik)

        self.bake_keys()
        
        self.delete_mocap_objects()

    def get_selected_fbx_returns_fbx_path(self):
        selected_fbx = cmds.textScrollList(self.fbx_scroll_list, query=True, selectItem=True)
        if not selected_fbx:
            cmds.warning("No FBX file selected.")
            return
        self.selected_fbx = selected_fbx[0]
        fbx_file_path = f"{self.scene_directory}/{self.selected_fbx}"
        return fbx_file_path
    def set_motion_capture_namespace(self):
        if not cmds.namespace(exists=self.mocap_namespace):
            if cmds.namespaceInfo(currentNamespace=True) != self.mocap_namespace:
                cmds.namespace(add=self.mocap_namespace)
        try:
            cmds.namespace(set=self.mocap_namespace)
        except:
            print("No namespace")
    def reset_namespace(self):
        cmds.namespace(set=':')
    def set_hik_plugin(self):
        if not cmds.pluginInfo('mayaHIK', query=True, loaded=True):
            cmds.loadPlugin('mayaHIK')
    
    def import_fbx(self, fbx_file_path):
        cmds.file(fbx_file_path, i=True, type="FBX", ignoreVersion=True, ra=True, namespace=self.mocap_namespace)

    def initialize_humanik_character(self,humanik):
        mel.eval('HIKCharacterControlsTool')
        mel.eval(f'hikCreateCharacter("{humanik}")')
        
    def delete_mocap_objects(self):
        cmds.delete(self.reference_joint)
        cmds.delete(self.char_human_ik)
        cmds.delete(self.mocap_human_ik)
        cmds.namespace(rm=self.mocap_namespace)

    def update_humanik_ui(self):
        """Update HumanIK UI."""
        mel.eval('hikUpdateCurrentSourceFromUI();')
        mel.eval('hikUpdateContextualUI();')
        mel.eval('hikControlRigSelectionChangedCallback')
        
    def bake_keys(self):
        bake_items = list(self.joint_pairs_dict.keys()) 
        bake_items_with_namespace = [f"{self.namespace}:{item}" for item in bake_items]
        first_frame, last_frame = self.get_first_and_last_frame()

        cmds.bakeResults(bake_items_with_namespace,
            simulation=True,
            t=(first_frame, last_frame),
            hierarchy='below',
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=True,
            preserveOutsideKeys=True,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            removeBakedAnimFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=True)
        
    def get_first_and_last_frame(self):
        keyframes = cmds.keyframe(self.reference_joint, query=True, timeChange=True)
        first_frame = math.floor(keyframes[0])
        last_frame = math.ceil(keyframes[-1])
        return first_frame, last_frame
    
    def assignJointsToHumanIKCharacter(self, humanIK, namespace, IsMocap):
        """Assign joints to the specified HumanIK character."""
        for joint, hik_joint in self.joint_pairs_dict.items():
            full_joint_name = f'{namespace}:{hik_joint}' if IsMocap else f'{namespace}:{joint}'
            mel_command = f'setCharacterObject("{full_joint_name}","{humanIK}",{self.humanik_code[hik_joint]},0);'
            try:
                mel.eval(mel_command)
            except Exception as e:
                cmds.warning(f"Failed to assign {full_joint_name} to {humanIK}.{hik_joint}: {e}")
    
    def select_hik_source(self, humanik):
        """Select the specified HumanIK source."""
        mel.eval('hikUpdateCurrentCharacterFromUI();')
        allSourceChar = cmds.optionMenuGrp("hikSourceList", query=True, itemListLong=True)

        for i,item in enumerate(allSourceChar,start=1):
            optMenu = "hikSourceList|OptionMenu"
            sourceChar = cmds.menuItem(item, query=True, label=True)
            print(sourceChar)
            if sourceChar == f" {humanik}":
                cmds.optionMenu(optMenu, edit=True, select=i)
                self.update_humanik_ui()
                break
            

    def select_hik_character(self, humanik):
        """Select the specified HumanIK character."""
        mel.eval('hikUpdateCurrentCharacterFromUI();')
        allCharacterChar = cmds.optionMenuGrp("hikCharacterList", query=True, itemListLong=True)

        for i,item in enumerate(allCharacterChar,start=1):
            optMenu = "hikCharacterList|OptionMenu"
            CharacterChar = cmds.menuItem(item, query=True, label=True)
            print(CharacterChar)
            if CharacterChar == f" {humanik}":
                cmds.optionMenu(optMenu, edit=True, select=i)
                self.update_humanik_ui()
                break
            


processor = SceneProcessor()
processor.createInputWindow()