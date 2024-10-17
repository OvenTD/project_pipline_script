import maya.cmds as cmds

def cleanup_animation_keys(tolerance):
    # Get the selected objects
    selected_objects = cmds.ls(selection=True)
    
    if not selected_objects:
        cmds.warning("Please select objects.")
        return
    
    for obj in selected_objects:
        # Get all animation curves connected to the object
        anim_curves = cmds.listConnections(obj, type="animCurve", destination=False) or []
        
        for curve in anim_curves:
            # Get keyframe times and values
            key_times = cmds.keyframe(curve, query=True, timeChange=True)
            key_values = cmds.keyframe(curve, query=True, valueChange=True)
            
            # Need at least 3 keys to compare
            if len(key_times) < 3:
                continue
            
            keys_to_delete = []
            
            # Compare slopes between frames
            for i in range(1, len(key_times) - 1):
                prev_time, cur_time, next_time = key_times[i-1], key_times[i], key_times[i+1]
                prev_value, cur_value, next_value = key_values[i-1], key_values[i], key_values[i+1]
                
                # Calculate slope between previous and current frame
                prev_slope = (cur_value - prev_value) / (cur_time - prev_time)
                # Calculate slope between current and next frame
                next_slope = (next_value - cur_value) / (next_time - cur_time)
                
                # If the difference in slopes is within tolerance, mark the key for deletion
                if abs(prev_slope - next_slope) < tolerance:
                    keys_to_delete.append(cur_time)
            
            # Delete unnecessary keys
            for time in keys_to_delete:
                cmds.cutKey(curve, time=(time,))
                print(f"Deleted key at frame {time} in {curve} of object {obj}")
            
            # Recheck keyframe times after cleanup
            remaining_key_times = cmds.keyframe(curve, query=True, timeChange=True)
            
            # If only two keys remain, delete both of them and reset to default values
            if remaining_key_times and len(remaining_key_times) == 2:
                cmds.cutKey(curve, time=(remaining_key_times[0], remaining_key_times[1]))
                print(f"Deleted the remaining two keys at frames {remaining_key_times[0]} and {remaining_key_times[1]} in {curve}")
                
                # Set translation, rotation to 0 and scale to 1 for XYZ
                if 'translate' in curve or 'rotate' in curve:
                    cmds.setAttr(f"{obj}.translateX", 0)
                    cmds.setAttr(f"{obj}.translateY", 0)
                    cmds.setAttr(f"{obj}.translateZ", 0)
                    cmds.setAttr(f"{obj}.rotateX", 0)
                    cmds.setAttr(f"{obj}.rotateY", 0)
                    cmds.setAttr(f"{obj}.rotateZ", 0)
                    print(f"Set translation and rotation of {obj} to 0.")
                elif 'scale' in curve:
                    cmds.setAttr(f"{obj}.scaleX", 1)
                    cmds.setAttr(f"{obj}.scaleY", 1)
                    cmds.setAttr(f"{obj}.scaleZ", 1)
                    print(f"Set scale of {obj} to 1.")

def cleanup_selected_keys(tolerance):
    # Get selected keyframes from Graph Editor
    selected_curves = cmds.keyframe(query=True, selected=True, name=True)
    
    if not selected_curves:
        cmds.warning("No keys selected. Please select keyframes.")
        return
    
    for curve in selected_curves:
        # Get selected key times and values
        key_times = cmds.keyframe(curve, query=True, selected=True, timeChange=True)
        key_values = cmds.keyframe(curve, query=True, selected=True, valueChange=True)
        
        # Need at least 3 keys to compare slopes
        if len(key_times) < 3:
            continue
        
        keys_to_delete = []
        
        # Compare slopes between selected frames
        for i in range(1, len(key_times) - 1):
            prev_time, cur_time, next_time = key_times[i-1], key_times[i], key_times[i+1]
            prev_value, cur_value, next_value = key_values[i-1], key_values[i], key_values[i+1]
            
            # Calculate slope between previous and current frame
            prev_slope = (cur_value - prev_value) / (cur_time - prev_time)
            # Calculate slope between current and next frame
            next_slope = (next_value - cur_value) / (next_time - cur_time)
            
            # If the difference in slopes is within tolerance, mark the key for deletion
            if abs(prev_slope - next_slope) < tolerance:
                keys_to_delete.append(cur_time)
        
        # Delete unnecessary selected keys
        for time in keys_to_delete:
            cmds.cutKey(curve, time=(time,))
            print(f"Deleted selected key at frame {time} in {curve}")

def run_cleanup(*args):
    # Get the tolerance value from the slider for all keys
    tolerance = cmds.floatSliderGrp(tolerance_all_slider, query=True, value=True)
    # Run the key cleanup function
    cleanup_animation_keys(tolerance)

def run_selected_cleanup(*args):
    # Get the tolerance value from the slider for selected keys
    tolerance = cmds.floatSliderGrp(tolerance_selected_slider, query=True, value=True)
    # Run the selected key cleanup function
    cleanup_selected_keys(tolerance)

def create_ui():
    # Delete existing UI if it exists
    if cmds.window("cleanupWindow", exists=True):
        cmds.deleteUI("cleanupWindow")
    
    # Create a new window
    window = cmds.window("cleanupWindow", title="Animation Key Cleanup", widthHeight=(300, 200))
    
    cmds.columnLayout(adjustableColumn=True)
    
    # Add the tolerance slider for all keys
    global tolerance_all_slider
    tolerance_all_slider = cmds.floatSliderGrp(label="Tolerance for All Keys:", field=True, minValue=0.0, maxValue=0.5, value=0.02, step=0.01)
    
    # Add a button to run the cleanup for all keys
    cmds.button(label="Run Cleanup for All Keys", command=run_cleanup)
    
    # Add the tolerance slider for selected keys
    global tolerance_selected_slider
    tolerance_selected_slider = cmds.floatSliderGrp(label="Tolerance for Selected Keys:", field=True, minValue=0.0, maxValue=0.5, value=0.02, step=0.01)
    
    # Add a button to run the cleanup for selected keys only
    cmds.button(label="Run Cleanup for Selected Keys", command=run_selected_cleanup)
    
    cmds.showWindow(window)

# Create the UI
create_ui()
