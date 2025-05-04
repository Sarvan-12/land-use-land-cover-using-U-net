import numpy as np
from PIL import Image

def load_image(image_path, target_size=(256, 256)):
    image = Image.open(image_path).convert('RGB')
    image = image.resize(target_size)
    return np.array(image) / 255.0  # Normalize if model expects it

def save_image(image_array, path):
    img = Image.fromarray(np.uint8(image_array))
    img.save(path)

def resize_image(image, target_size=(256, 256)):
    return image.resize(target_size)

def mask_to_label(mask):
    return np.array(mask).argmax(axis=-1) if mask.ndim == 3 else np.array(mask)
