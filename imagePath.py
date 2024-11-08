import os
import json
import re

# Path to the folder containing images
image_directory = "fullRangeData"

# Get a list of all image files in the directory
image_files = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# Function to extract the sample number from the filename
def get_sample_number(filename):
    match = re.search(r"(\d+)", filename)  # Finds the first occurrence of digits in the filename
    return int(match.group(0)) if match else float('inf')  # Returns number or infinity if no number found

# Sort images by the sample number
sorted_image_files = sorted(image_files, key=get_sample_number)

# Create a dictionary with the ordered list of image paths
images_dict = {"images": [os.path.join(image_directory, f) for f in sorted_image_files]}

# Save the dictionary to a JSON file
with open('cnv_image_paths.json', 'w') as json_file:
    json.dump(images_dict, json_file, indent=4)

print("JSON file 'ordered_image_paths.json' created successfully with ordered image paths.")
