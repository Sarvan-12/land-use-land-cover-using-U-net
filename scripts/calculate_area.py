import os
import numpy as np
import pandas as pd
from PIL import Image

LABELS_DIR = './data/labels'
OUTPUT_CSV = './data/area_by_class.csv'
NUM_CLASSES = 12  # Number of land cover classes (adjust if needed)

def count_class_pixels(mask_array):
    return np.bincount(mask_array.flatten(), minlength=NUM_CLASSES)

def extract_year(filename):
    # Assumes filename like: 1994_region1.tif or region1_1994.tif
    digits = [s for s in filename.split('_') if s.isdigit()]
    return digits[0] if digits else 'unknown'

def calculate_area():
    records = []

    for region in os.listdir(LABELS_DIR):
        region_path = os.path.join(LABELS_DIR, region)
        if not os.path.isdir(region_path):
            continue

        for file in os.listdir(region_path):
            if file.endswith('.tif'):
                image_path = os.path.join(region_path, file)
                mask = np.array(Image.open(image_path))

                class_counts = count_class_pixels(mask)
                year = extract_year(file)

                record = {
                    'region': region,
                    'year': year
                }
                for class_id in range(NUM_CLASSES):
                    record[f'class_{class_id}'] = class_counts[class_id]

                records.append(record)

    df = pd.DataFrame(records)
    df.sort_values(by=['region', 'year'], inplace=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Area data saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    calculate_area()
