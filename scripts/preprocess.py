import os
import cv2
from scripts.utils.image_utils import resize_image
# from utils.image_utils import resize_image
import numpy as np

def preprocess_images(region_folders, output_folders):
    """Preprocess images by resizing them and saving them to processed folders"""
    for region_folder, output_folder in zip(region_folders, output_folders):
        print(f"Processing region: {region_folder}")
        
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        images = [f for f in os.listdir(region_folder) if f.endswith('.tif')]
        print(f"Found {len(images)} images in {region_folder}")
        
        for image_file in images:
            image_path = os.path.join(region_folder, image_file)
            
            # Load the image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Warning: Could not load image {image_file}, skipping...")
                continue
            
            # Resize image if required (for training, resize to a fixed size)
            resized_image = resize_image(image)  # Assumes resize_image function exists
            
            # Save the processed image to the corresponding region output folder
            processed_image_path = os.path.join(output_folder, image_file)
            cv2.imwrite(processed_image_path, resized_image)
            print(f"Processed and saved {image_file} to {processed_image_path}")

def resize_image(image, target_size=(256, 256)):
    """Resize image to the target size"""
    return cv2.resize(image, target_size)

def main():
    """Main function to preprocess images in all regions"""
    region_folders = [
        os.path.join('data', 'raw', 'region_1'),
        os.path.join('data', 'raw', 'region_2'),
        os.path.join('data', 'raw', 'region_3')
    ]
    
    output_folders = [
        os.path.join('data', 'processed', 'region_1'),
        os.path.join('data', 'processed', 'region_2'),
        os.path.join('data', 'processed', 'region_3')
    ]
    
    preprocess_images(region_folders, output_folders)

if __name__ == "__main__":
    main()
