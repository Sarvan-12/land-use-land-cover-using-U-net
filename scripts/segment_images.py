import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img
from scripts.utils.image_utils import save_image, mask_to_label

def segment_images():
    print("Starting segmentation...")

    # Define paths
    processed_dir = './data/processed'
    labels_dir = './data/labels'

    os.makedirs(labels_dir, exist_ok=True)

    # ✅ Load the TensorFlow U-Net model
    model = load_model('./models/unet_best_model.h5')

    for region in ['region_1', 'region_2', 'region_3']:
        region_folder = os.path.join(processed_dir, region)
        region_labels_folder = os.path.join(labels_dir, region)
        os.makedirs(region_labels_folder, exist_ok=True)

        for image_file in os.listdir(region_folder):
            if image_file.endswith('.tif'):  # process only .tif files
                image_path = os.path.join(region_folder, image_file)

                # Load and preprocess image
                image = load_img(image_path, target_size=(256, 256))
                image_array = img_to_array(image) / 255.0
                image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

                # Predict segmentation
                prediction = model.predict(image_array)
                predicted_mask = np.argmax(prediction[0], axis=-1)  # Remove batch & get class index

                # Convert to uint8 image
                label_image = (predicted_mask).astype(np.uint8)

                # Save image using existing utility or fallback
                save_path = os.path.join(region_labels_folder, image_file)
                save_image(label_image, save_path)

    print("✅ Image segmentation completed.")

if __name__ == "__main__":
    segment_images()
