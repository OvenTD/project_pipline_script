
import maya.cmds as cmds
import os

# Ensure the FBX plugin is loaded
if not cmds.pluginInfo("fbxmaya", query=True, loaded=True):
    cmds.loadPlugin("fbxmaya")

def export_camera_as_fbx():
    # Define camera name
    camera_name = "AnimCam"
    
    if not cmds.objExists(camera_name):
        cmds.warning(f"Camera '{camera_name}' not found.")
        return
    
    # Get the animation start and end frames
    start_frame = cmds.findKeyframe(camera_name, which="first")
    end_frame = cmds.findKeyframe(camera_name, which="last")
    export_start_frame = start_frame - 10
    export_end_frame = end_frame + 10

    # Get the current scene file name and transform it to the desired format
    current_scene = cmds.file(query=True, sceneName=True, shortName=True)
    file_name_parts = current_scene.split('_')
    if len(file_name_parts) >= 3:
        scene_part = file_name_parts[1][:2]
        cut_part = file_name_parts[2].split('.')[0]
        export_file_name = f"{scene_part}_{cut_part}_Camera.fbx"
    else:
        cmds.warning("Scene file name is not in the expected format.")
        export_file_name = "default_Camera.fbx"

    # Define the export path
    export_path = os.path.join("D:/Hijackers_UE/USD/Camera", export_file_name)
    
    # Set FBX export options and export selected object with frame range
    cmds.select(camera_name)

        
    export_options = ";".join([
        "exportUVs=1",
        "exportSkels=none",
        "exportSkin=none",
        "exportBlendShapes=1",
        "exportDisplayColor=0",
        "exportColorSets=1",
        "exportComponentTags=1",
        "defaultMeshScheme=catmullClark",
        "animation=0",
        "eulerFilter=0",
        "staticSingleSample=1",
        f"startTime={export_start_frame}",
        f"endTime={export_end_frame}",
        "frameStride=1",
        "frameSample=0.0",
        "defaultUSDFormat=usda",
        "parentScope=",
        "shadingMode=useRegistry",
        "convertMaterialsTo=[UsdPreviewSurface]",
        "exportInstances=1",
        "exportVisibility=1",
        "mergeTransformAndShape=1",
        "stripNamespaces=0",
        "materialsScopeName=mtl"
    ])

    # Define the export path and file type
    file_type = "FBX export"

    # Execute the export command
    cmds.file(export_path, force=True, options=export_options, type=file_type, preserveReferences=True, exportSelected=True)
    cmds.FBXExport(f=export_path, s=True)
        
    cmds.textField("exportPathField", edit=True, text=export_path)
    cmds.confirmDialog(title="Export Complete", message=f"Camera exported successfully to: {export_path}")

def create_export_ui():
    # Check if the window exists
    if cmds.window("fbxExportWindow", exists=True):
        cmds.deleteUI("fbxExportWindow")
    
    # Create window
    window = cmds.window("fbxExportWindow", title="Export Camera as FBX", widthHeight=(400, 150))
    cmds.columnLayout(adjustableColumn=True)

    # Display Export Path
    cmds.text(label="Export Path:")
    cmds.textField("exportPathField", editable=False, text="Path will display here after export")

    # Export button
    cmds.button(label="Export AnimCam as FBX", command=lambda x: export_camera_as_fbx())

    # Show window
    cmds.showWindow(window)

# Create the UI
create_export_ui()
