import maya.cmds as cmds

def get_vector_values():
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("No objects selected.")
        return []

    vector_values = []
    for obj in selected_objects:
        keyframes = cmds.keyframe(obj, query=True, time=(1, cmds.playbackOptions(maxTime=True)), valueChange=True)
        for i in range(0, len(keyframes), 3):  # x, y, z 값
            vector_values.append((keyframes[i], keyframes[i + 1], keyframes[i + 2]))

    return vector_values

vectors = get_vector_values()
print(vectors)
