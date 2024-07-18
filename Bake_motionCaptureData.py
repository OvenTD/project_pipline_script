#
# This code is for Bake and adjust first frame of the motion captured dataset. 
# Search fbx file in root directory and perform them. 
# adjust the first frame 1 to 1001.
#
import maya.cmds as cmds
import math
import os

def adjust_animation_start_frame(selection):
    keyframes = cmds.keyframe(selection, query=True, timeChange=True)
    first_frame = math.floor(keyframes[0])
    last_frame = math.ceil(keyframes[-1])
    
    all_descendants = []
    for obj in selection:
        all_descendants.append(selection)  # Include the selected object itself
    descendants = cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []
    all_descendants.extend(descendants)
    
    all_anim_curves = []
    for i in all_descendants:
        # Get all animation curves for the object
        anim_curves = cmds.listConnections(i, type='animCurve')
        
        if anim_curves:
            all_anim_curves.append(anim_curves)

    # Iterate over each selected object
    cmds.bakeResults(selection,
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
    
    for n, obj in enumerate(all_descendants):
        # Get all animation curves for the object
        anim_curves = cmds.listConnections(obj, type='animCurve')

        if anim_curves:
            for curve in anim_curves:
                
                if curve not in all_anim_curves[n]:
                    cmds.delete(curve)
                    continue
                
                keyframes = cmds.keyframe(curve, query=True, timeChange=True)

                if keyframes:
                    for i, new_frame in enumerate(keyframes):
                        cmds.keyframe(curve, edit=True, includeUpperBound=True, relative=True, option='over', time=(keyframes[i], keyframes[i]), timeChange=1000)


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

root_directory = 'D:/Hijackers/MotionCaptureData/OKcut'

fbx_file_paths, fbx_file_names = find_fbx_files(root_directory)

total_files = len(fbx_file_paths)
for i in range(total_files):
    fbx_file_path = fbx_file_paths[i]

    print(f"Processing file {i + 1} of {total_files}: {fbx_file_path}")

    cmds.file(fbx_file_path, i=True, type="FBX", ignoreVersion=True, ra=True)

    adjust_animation_start_frame(['Reference'])

    fbx_export_path = fbx_file_paths[i].replace('OKcut', 'Baked')
    print(f"Exporting to: {fbx_export_path}")
    cmds.file(fbx_export_path, force=True, options="", type="FBX export", pr=True, es=True)

    cmds.file(new=True, force=True)

    print(f"Completed file {i + 1} of {total_files}\n")
