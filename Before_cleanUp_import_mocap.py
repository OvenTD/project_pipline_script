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
        self.selected_fbx = None
        self.character_name = None
        self.root_directory = 'D:/Hijackers/MotionCaptureData/Baked'
        self.scene_directory = None
        self.fbx_file_paths = None
        self.fbx_file_names = None
        self.mocap_namespace = "motionCaptureData"
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
        
        cmds.button(label="Get Namespace", command=self.getNamespace)
        cmds.button(label="Process Scene and Cut", command=self.processSceneAndCut)
        
        self.fbx_scroll_list = cmds.textScrollList(height=100, allowMultiSelection=False)
        
        cmds.button(label="Process Selected FBX", command=self.processSelectedFBX)
        
        cmds.showWindow(window)

    def getNamespace(self, *args):
        selected = cmds.ls(selection=True)
        if selected:
            self.namespace = selected[0].split(':')[0] if ':' in selected[0] else ''
            cmds.textField(self.namespace_field, edit=True, text=self.namespace)
        else:
            cmds.warning("Please select an object to get its namespace.")

    def connectAttributes(self, *args):
        #self.select_hik_source(self.mocap_human_ik)
        self.select_hik_character(self.char_human_ik)

    def createHumanIKCharacter(self, *args):
        self.namespace_process()
        two_arms = [f'{self.namespace}:FKShoulder_L', f'{self.namespace}:FKShoulder_R']
        
        FKIK_list = ['FKIKLeg_R','FKIKLeg_L','FKIKArm_L','FKIKArm_R']
        for i in FKIK_list:
            cmds.setAttr(f'{self.namespace}:{i}.FKIKBlend',0)

        for obj in two_arms:
            cmds.setAttr(f"{obj}.rotateX", self.character_rotation_offset[0])
            cmds.setAttr(f"{obj}.rotateY", self.character_rotation_offset[1])
            cmds.setAttr(f"{obj}.rotateZ", self.character_rotation_offset[2])
    
        if not cmds.pluginInfo('mayaHIK', query=True, loaded=True):
            cmds.loadPlugin('mayaHIK')
    
        mel.eval('HIKCharacterControlsTool')
    
        self.char_human_ik = f'{self.character_name}HumanIK'
        mel.eval(f'hikCreateCharacter("{self.char_human_ik}")')

        self.assignJointsToHumanIKCharacter(self.char_human_ik,self.namespace,False)

    def namespace_process(self):
        self.namespace = cmds.textField(self.namespace_field, query=True, text=True)
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

    def processSceneAndCut(self, *args):
        cmds.namespace(set=':')
        self.scene = cmds.intField(self.scene_field, query=True, value=True)
        self.cut = cmds.intField(self.cut_field, query=True, value=True)
        
        self.namespace_process()
        if not self.namespace:
            cmds.warning("Please select an object to get its namespace.")
            return
    
        self.scene_directory = f'{self.root_directory}/Scene{self.scene:02d}/{self.character_name}'
    
        self.fbx_file_paths, self.fbx_file_names = self.find_fbx_files(self.scene_directory)
    
        search_prefix = f'{self.scene}-{self.cut}'
    
        matching_indices = [i for i, file_name in enumerate(self.fbx_file_names) if file_name.startswith(search_prefix)]

        if not matching_indices:
            cmds.warning("No matching files found.")
            return
    
        self.searched_fbxes = [self.fbx_file_names[i] for i in matching_indices]
        
        cmds.textScrollList(self.fbx_scroll_list, edit=True, removeAll=True)
        for fbx in self.searched_fbxes:
            cmds.textScrollList(self.fbx_scroll_list, edit=True, append=fbx)

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

    def processSelectedFBX(self, *args):
        selected_fbx = cmds.textScrollList(self.fbx_scroll_list, query=True, selectItem=True)
        self.createHumanIKCharacter()
        if not selected_fbx:
            cmds.warning("No FBX file selected.")
            return
        self.selected_fbx = selected_fbx[0]
        fbx_file_path = f"{self.scene_directory}/{self.selected_fbx}"
        
        if not cmds.namespace(exists=self.mocap_namespace):
            if cmds.namespaceInfo(currentNamespace=True) != self.mocap_namespace:
                cmds.namespace(add=self.mocap_namespace)
        try:
            cmds.namespace(set=self.mocap_namespace)
        except:
            print("No namespace")
        cmds.file(fbx_file_path, i=True, type="FBX", ignoreVersion=True, ra=True, namespace=self.mocap_namespace)
        cmds.namespace(set=':')
        
        if not cmds.pluginInfo('mayaHIK', query=True, loaded=True):
            cmds.loadPlugin('mayaHIK')
    
        mel.eval('HIKCharacterControlsTool')
    
        self.mocap_human_ik = 'MotionCaptureHumanIK'
        mel.eval(f'hikCreateCharacter("{self.mocap_human_ik}")')

        for joint in self.joint_pairs_dict:
            full_joint_name = f'{self.mocap_namespace}:{self.joint_pairs_dict[joint]}'
            self.assignJointsToHumanIKCharacter(self.mocap_human_ik, self.mocap_namespace, True)
 
        mel.eval('hikUpdateCurrentCharacterFromUI();')
        mel.eval('hikUpdateCurrentSourceFromUI()')
        mel.eval('hikUpdateContextualUI()')
        mel.eval('hikControlRigSelectionChangedCallback')

  # Optional: Add a short delay to ensure the UI updates correctly
        self.select_hik_character(self.char_human_ik)
        self.select_hik_source(self.mocap_human_ik)

        bake_items = list(self.joint_pairs_dict.keys()) 
        bake_items_with_namespace = [f"{self.namespace}:{item}" for item in bake_items]
        self.bake_keys(bake_items_with_namespace)


        cmds.delete(f'{self.mocap_namespace}:Reference')
        cmds.delete(self.char_human_ik)
        cmds.delete(self.mocap_human_ik)
        cmds.namespace(rm=self.mocap_namespace)


    def bake_keys(self, ctrls):
        reference_joint = f'{self.mocap_namespace}:Reference'

        keyframes = cmds.keyframe(reference_joint, query=True, timeChange=True)
        first_frame = math.floor(keyframes[0])
        last_frame = math.ceil(keyframes[-1])

        cmds.bakeResults(ctrls,
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
    def clean_up_baked_keys(self):
        bake_items = list(self.joint_pairs_dict.keys()) 
        bake_items_with_namespace = [f"{self.namespace}:{item}" for item in bake_items]
        reference_joint = f'{self.mocap_namespace}:Reference'
        all_descendants = []

        descendants = cmds.listRelatives(reference_joint, allDescendents=True, fullPath=True) or []
        all_descendants.append(reference_joint)
        all_descendants.extend(descendants)
        
        all_anim_curves = []
        for i in all_descendants:
            # Get all animation curves for the object
            anim_curves = cmds.listConnections(i, type='animCurve')
            
            if anim_curves:
                all_anim_curves.append(anim_curves)
        for n, obj in enumerate(bake_items_with_namespace):
        # Get all animation curves for the object
            anim_curves = cmds.listConnections(obj, type='animCurve')

            if anim_curves:
                for curve in anim_curves:
                    
                    if curve not in all_anim_curves[n]:
                        cmds.delete(curve)
                        continue
    def assignJointsToHumanIKCharacter(self, humanIK, namespace, IsMocap):
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
    
    def select_hik_source(self, humanik):
        mel.eval('hikUpdateCurrentCharacterFromUI();')
        allSourceChar = cmds.optionMenuGrp("hikSourceList", query=True, itemListLong=True)

        i = 1
        for item in allSourceChar:
            optMenu = "hikSourceList|OptionMenu"
            sourceChar = cmds.menuItem(item, query=True, label=True)
            print(sourceChar)
            if sourceChar == f" {humanik}":
                cmds.optionMenu(optMenu, edit=True, select=i)
                mel.eval('hikUpdateCurrentSourceFromUI()')
                mel.eval('hikUpdateContextualUI()')
                mel.eval('hikControlRigSelectionChangedCallback')
                break
            i += 1

    def select_hik_character(self, humanik):
        mel.eval('hikUpdateCurrentCharacterFromUI();')
        allCharacterChar = cmds.optionMenuGrp("hikCharacterList", query=True, itemListLong=True)

        i = 1
        for item in allCharacterChar:
            optMenu = "hikCharacterList|OptionMenu"
            CharacterChar = cmds.menuItem(item, query=True, label=True)
            print(CharacterChar)
            if CharacterChar == f" {humanik}":
                cmds.optionMenu(optMenu, edit=True, select=i)
                mel.eval('hikUpdateCurrentCharacterFromUI()')
                mel.eval('hikUpdateCurrentSourceFromUI()')
                mel.eval('hikUpdateContextualUI()')
                mel.eval('hikControlRigSelectionChangedCallback')
                break
            i += 1


processor = SceneProcessor()
processor.createInputWindow()