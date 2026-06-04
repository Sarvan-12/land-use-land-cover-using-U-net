import os
import numpy as np
from PIL import Image

# Class definitions
class_mapping = {
    11: 'Water',
    21: 'Developed, Open Space',
    22: 'Developed, Low Intensity',
    23: 'Developed, Medium Intensity',
    24: 'Developed, High Intensity',
    31: 'Barren Land',
    41: 'Deciduous Forest',
    42: 'Evergreen Forest',
    43: 'Mixed Forest',
    52: 'Shrub/Scrub',
    71: 'Grassland',
    81: 'Pasture/Hay',
    82: 'Cultivated Crops',
    90: 'Woody Wetlands',
    95: 'Emergent Herbaceous Wetlands',
}

# Hex to RGB mapping
brutalist_color_map = {
    'Water': (0, 194, 255),                       # #00C2FF
    'Developed, Open Space': (255, 164, 164),        # #FFA4A4
    'Developed, Low Intensity': (255, 126, 126),     # #FF7E7E
    'Developed, Medium Intensity': (255, 77, 77),  # #FF4D4D
    'Developed, High Intensity': (208, 28, 28),    # #D01C1C
    'Barren Land': (255, 221, 0),                 # #FFDD00
    'Deciduous Forest': (46, 125, 50),             # #2E7D32
    'Evergreen Forest': (27, 94, 32),             # #1B5E20
    'Mixed Forest': (76, 175, 80),                 # #4CAF50
    'Shrub/Scrub': (129, 199, 132),                  # #81C784
    'Grassland': (200, 230, 201),                    # #C8E6C9
    'Pasture/Hay': (255, 241, 118),                  # #FFF176
    'Cultivated Crops': (251, 192, 45),              # #FBC02D
    'Woody Wetlands': (179, 136, 255),               # #B388FF
    'Emergent Herbaceous Wetlands': (124, 77, 255), # #7C4DFF
}

def generate_images():
    processed_dir = './data/processed'
    labels_dir = './data/raw'
    
    # Target directory in assets folder for Dash static files
    assets_raw_dir = './scripts/assets/images/raw'
    assets_class_dir = './scripts/assets/images/classified'
    
    os.makedirs(assets_raw_dir, exist_ok=True)
    os.makedirs(assets_class_dir, exist_ok=True)

    regions = ['region_1', 'region_2', 'region_3']
    
    for region in regions:
        print(f"Generating web assets for {region}...")
        
        region_raw_path = os.path.join(processed_dir, region)
        region_label_path = os.path.join(labels_dir, region)
        
        if not os.path.exists(region_raw_path) or not os.path.exists(region_label_path):
            print(f"Skipping {region} (missing source raw or label directory)")
            continue
            
        for file_name in os.listdir(region_raw_path):
            if file_name.endswith('.tif'):
                # 1. Convert and save raw satellite image as PNG
                raw_tif_path = os.path.join(region_raw_path, file_name)
                raw_img = Image.open(raw_tif_path).convert('RGB')
                
                # Save compressed PNG
                png_name = file_name.replace('.tif', '.png')
                raw_png_path = os.path.join(assets_raw_dir, f"{region}_{png_name}")
                raw_img.save(raw_png_path, "PNG", optimize=True)
                
                # 2. Convert, colorize, and save classification mask as PNG
                label_tif_path = os.path.join(region_label_path, file_name)
                if os.path.exists(label_tif_path):
                    mask_img = Image.open(label_tif_path)
                    mask_img = mask_img.resize((256, 256), Image.NEAREST)
                    mask_arr = np.array(mask_img)
                    
                    # Create empty RGB canvas
                    h, w = mask_arr.shape
                    color_arr = np.zeros((h, w, 3), dtype=np.uint8)
                    
                    # Map pixels
                    for code, class_name in class_mapping.items():
                        color = brutalist_color_map.get(class_name, (255, 255, 255))
                        color_arr[mask_arr == code] = color
                        
                    # Also handle background / zero values as white
                    color_arr[mask_arr == 0] = (255, 255, 255)
                    
                    classified_img = Image.fromarray(color_arr)
                    classified_png_path = os.path.join(assets_class_dir, f"{region}_{png_name}")
                    classified_img.save(classified_png_path, "PNG", optimize=True)

    print("All web-friendly PNG images generated.")

if __name__ == "__main__":
    generate_images()
