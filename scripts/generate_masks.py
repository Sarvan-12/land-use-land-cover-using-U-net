import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf

# Path to the regions
regions = ['region_1', 'region_2', 'region_3']
image_dir = 'data/processed'  # Adjust path if necessary
mask_dir = 'data/labels'  # Where masks will be saved

# Class values for segmentation (change as needed)
class_values = [11]  # For example, if you're detecting a particular class like "Water" with value 11

# Function to generate masks for each image
def generate_mask(image_path, class_values):
    image = load_img(image_path, color_mode='rgb')  # Load as RGB
    image_array = img_to_array(image)

    # Initialize mask with zeros (black)
    mask = np.zeros(image_array.shape[:2], dtype=np.uint8)

    for class_value in class_values:
        # Create a mask by checking if any pixel matches the class_value in any channel
        # For simplicity, we assume class_value is identified by specific pixel values.
        # Adjust logic to match your class identification strategy
        mask[np.all(image_array == class_value, axis=-1)] = 255

    return mask

# Function to process all regions
def generate_masks_for_all_regions():
    for region in regions:
        # Create a directory for masks if not exist
        region_mask_dir = os.path.join(mask_dir, region)
        if not os.path.exists(region_mask_dir):
            os.makedirs(region_mask_dir)

        # Loop through all images in the processed folder for this region
        region_image_dir = os.path.join(image_dir, region)
        for filename in os.listdir(region_image_dir):
            if filename.endswith('.tif'):  # Only process .tif files
                image_path = os.path.join(region_image_dir, filename)
                
                # Generate mask for the image
                mask = generate_mask(image_path, class_values)
                
                # Add a channel dimension to the mask (height, width, 1)
                mask = np.expand_dims(mask, axis=-1)

                # Save the mask to the corresponding region mask directory
                mask_filename = filename.replace('.tif', '.tif')
                mask_path = os.path.join(region_mask_dir, mask_filename)
                tf.keras.preprocessing.image.save_img(mask_path, mask)
                print(f"Mask saved at {mask_path}")

# Run the function to generate masks for all regions
generate_masks_for_all_regions()
