import tkinter as tk
import pyautogui
import cv2
import numpy as np
import time

# Constants
DELAY_TIME = 0.3  # Adjust delay time as needed

def find_and_click_image(image_path):
    # Get the current mouse position
    original_position = pyautogui.position()
    
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    # Load the image to search for
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    # Find the best match location
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Set a threshold to determine if the match is good enough
    threshold = 0.8
    if max_val >= threshold:
        # Calculate the center of the matched image
        img_w, img_h = template.shape[1], template.shape[0]
        center_x = max_loc[0] + img_w // 2
        center_y = max_loc[1] + img_h // 2
        
        # Click on the found location
        pyautogui.click(center_x, center_y)
        
        # Wait for the specified delay time (if necessary)
        time.sleep(DELAY_TIME)
    else:
        print(f"Image not found: {image_path}")
    
    # Return to the original mouse position
    pyautogui.moveTo(original_position)
    print(f"Moved back to original position: {original_position}")

def find_and_click_image_right(image_path):
    # Get the current mouse position
    original_position = pyautogui.position()
    
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    # Load the image to search for
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    # Find the best match location
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Set a threshold to determine if the match is good enough
    threshold = 0.8
    if max_val >= threshold:
        # Calculate the center of the matched image
        img_w, img_h = template.shape[1], template.shape[0]
        center_x = max_loc[0] + img_w - img_h
        center_y = max_loc[1] + img_h // 2
        
        # Click on the found location
        pyautogui.click(center_x, center_y)
        
        # Wait for the specified delay time (if necessary)
        time.sleep(DELAY_TIME)
    else:
        print(f"Image not found: {image_path}")
    
    # Return to the original mouse position
    pyautogui.moveTo(original_position)
    
def click_export_button():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\export_button.png')

def click_prism_export_button():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\prism_export_button.png')

def click_mb_type_button():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\abc_type_button.png')
    time.sleep(DELAY_TIME)  # Delay before the next action
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\mb_type_button.png')

def type_selected_folder_name():
    pyautogui.typewrite("first")

def click_comment_field_button():
    find_and_click_image(r'project_pipline_script/export_crowling/imgs/comment_textfield.png')
    type_selected_folder_name()

def click_prism_publish_button():
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\asset_publish_button.png')
    time.sleep(DELAY_TIME)
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\publish_continue_button.png')
    time.sleep(DELAY_TIME)
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\publish_ok_button.png')

def click_close_button():
    find_and_click_image_right(r'D:\GIT\project_pipline_script\export_crowling\imgs\delete_window.png')

# New function to execute all actions in sequence
def execute_all_actions_in_sequence():
    click_export_button()
    time.sleep(DELAY_TIME)
    click_prism_export_button()
    time.sleep(DELAY_TIME)
    click_mb_type_button()
    time.sleep(DELAY_TIME)
    click_comment_field_button()
    time.sleep(DELAY_TIME)
    click_prism_publish_button()
    time.sleep(DELAY_TIME)
    click_close_button()
    find_and_click_image(r'D:\GIT\project_pipline_script\export_crowling\imgs\open_prism.png')

# Tkinter GUI setup
root = tk.Tk()
root.title("Image Clicker")

# Set the size of the window (half the previous width, keep height the same)
root.geometry("400x600")  # Reduced width to 400, height remains 600

# Create and place buttons
button1 = tk.Button(root, text="Click export Button", command=click_export_button)
button1.pack(pady=20)

button2 = tk.Button(root, text="Click prism export Button", command=click_prism_export_button)
button2.pack(pady=20)

button3 = tk.Button(root, text="Click MB Type Button", command=click_mb_type_button)
button3.pack(pady=20)

button4 = tk.Button(root, text="Click comment field", command=click_comment_field_button)
button4.pack(pady=20)

button5 = tk.Button(root, text="Publish", command=click_prism_publish_button)
button5.pack(pady=20)

# Add a button to click the close button
button6 = tk.Button(root, text="Close Window", command=click_close_button)
button6.pack(pady=20)

# Add the new button to execute all actions in sequence
execute_all_button = tk.Button(root, text="Execute All Actions", command=execute_all_actions_in_sequence)
execute_all_button.pack(pady=20)

# Run the GUI event loop
root.mainloop()
