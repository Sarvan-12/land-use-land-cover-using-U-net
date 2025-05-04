import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Load images and masks
def load_data(image_dir, mask_dir, img_size=(256, 256)):
    images = []
    masks = []
    
    # Loop through the image directories and corresponding mask directories
    for region in ['region_1', 'region_2', 'region_3']:  # Update region names as per your folder names
        region_images = os.listdir(os.path.join(image_dir, region))
        for image_name in region_images:
            if image_name.endswith('.tif'):  # Add any condition if necessary
                image_path = os.path.join(image_dir, region, image_name)
                mask_path = os.path.join(mask_dir, region, image_name)  # Assuming mask names match image names
                
                image = load_img(image_path, target_size=img_size)
                image = img_to_array(image) / 255.0  # Normalize the image
                images.append(image)
                
                mask = load_img(mask_path, target_size=img_size, color_mode='grayscale')
                mask = img_to_array(mask)
                mask = to_categorical(mask, num_classes=12)  # Adjust num_classes as per your class values
                masks.append(mask)
    
    return np.array(images), np.array(masks)

# Define U-Net model
def unet_model(input_size=(256, 256, 3)):
    inputs = layers.Input(input_size)
    
    # Contracting Path
    c1 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    c1 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(c1)
    p1 = layers.MaxPooling2D((2, 2))(c1)
    
    c2 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(p1)
    c2 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(c2)
    p2 = layers.MaxPooling2D((2, 2))(c2)
    
    c3 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(p2)
    c3 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(c3)
    p3 = layers.MaxPooling2D((2, 2))(c3)
    
    c4 = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(p3)
    c4 = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(c4)
    p4 = layers.MaxPooling2D((2, 2))(c4)
    
    c5 = layers.Conv2D(1024, (3, 3), activation='relu', padding='same')(p4)
    c5 = layers.Conv2D(1024, (3, 3), activation='relu', padding='same')(c5)
    
    # Expansive Path
    u6 = layers.Conv2DTranspose(512, (2, 2), strides=(2, 2), padding='same')(c5)
    u6 = layers.concatenate([u6, c4])
    c6 = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(u6)
    c6 = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(c6)
    
    u7 = layers.Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same')(c6)
    u7 = layers.concatenate([u7, c3])
    c7 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(u7)
    c7 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(c7)
    
    u8 = layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c7)
    u8 = layers.concatenate([u8, c2])
    c8 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(u8)
    c8 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(c8)
    
    u9 = layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c8)
    u9 = layers.concatenate([u9, c1])
    c9 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(u9)
    c9 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(c9)
    
    outputs = layers.Conv2D(12, (1, 1), activation='softmax')(c9)  # 12 classes (adjust if necessary)
    
    model = models.Model(inputs, outputs)
    
    return model

# Train model
def train_model():
    image_dir = 'data/processed'  # Adjust your image directory path
    mask_dir = 'data/labels'     # Adjust your mask directory path
    
    # Load data
    images, masks = load_data(image_dir, mask_dir)
    
    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(images, masks, test_size=0.2, random_state=42)
    
    # Create model
    model = unet_model(input_size=(256, 256, 3))  # Increase image size to 512x512
    
    # Compile model with a lower learning rate for better fine-tuning
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),  # Lower learning rate
                  loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Define callbacks
    checkpoint = ModelCheckpoint('models/unet_best_model.h5', save_best_only=True, monitor='val_loss', mode='min')
    
    # Train model with increased epochs and batch size
    model.fit(X_train, y_train, validation_data=(X_val, y_val),
              epochs=50,  # Increase epochs for better convergence
              batch_size=8,  # Increase batch size for larger training batches
              callbacks=[checkpoint])

if __name__ == '__main__':
    train_model()
