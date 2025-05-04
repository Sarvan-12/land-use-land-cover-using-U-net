import os
import re

def rename_images_in_region(region_folder):
    """Rename images in a region folder to match the 'region_X_year.tif' format"""
    # Get all files in the region folder
    images = [f for f in os.listdir(region_folder) if f.endswith('.tif')]
    
    # Loop through all images and rename them
    for image_file in images:
        # Extract the year from the filename using a regex pattern (assuming year is in the filename)
        # Modify this pattern if the year is not in the expected position
        match = re.search(r'(\d{4})', image_file)
        
        if match:
            year = match.group(1)
            region_number = region_folder.split('_')[-1]  # Assuming the folder name is like 'region_1'
            new_name = f"region_{region_number}_{year}.tif"
            
            # Create the full path to the old and new filenames
            old_path = os.path.join(region_folder, image_file)
            new_path = os.path.join(region_folder, new_name)
            
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed {image_file} to {new_name}")
        else:
            print(f"Could not extract year from {image_file}. Skipping...")

def rename_all_images():
    """Rename images in all region folders"""
    region_folders = [
        os.path.join('data', 'raw', 'region_1'),  # Path to region 1
        os.path.join('data', 'raw', 'region_2'),  # Path to region 2
        os.path.join('data', 'raw', 'region_3')   # Path to region 3
    ]
    
    for region_folder in region_folders:
        print(f"Renaming images in {region_folder}...")
        rename_images_in_region(region_folder)

if __name__ == "__main__":
    # Call the function to rename all images in all regions
    rename_all_images()
