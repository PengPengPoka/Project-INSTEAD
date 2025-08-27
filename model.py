import tensorflow as tf
import keras
from keras.applications import resnet50
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from keras.applications import ResNet50
from keras.applications.resnet import preprocess_input
from rembg import remove
from PIL import Image
from keras.preprocessing.image import load_img
import numpy as np
from pathlib import Path

"""
nambah library:
    - tensorflow
    - keras
    - rembg
    - lib yang kurang lainnya
"""

# need to revise path to be dynamic
BASE_DIR = Path(__file__).absolute().parent
WEIGHT_PATH = BASE_DIR / "ml_utils" / "best_model 2.hdf5"
BACKGROUND_PATH = BASE_DIR / "ml_utils" / "bg.jpg"
data_path = "C:\\Users\\OMEN\\Downloads\\teh_sample_10.jpg"

# Hyperparameter
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
IMG_DIMENSION = 224
IMG_SIZE = (IMG_DIMENSION, IMG_DIMENSION)
INPUT_SHAPE = (IMG_DIMENSION, IMG_DIMENSION, 3)
NUM_CLASSES = 10

def create_model():
    # Load pre-trained ResNet50 model
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=INPUT_SHAPE)

    # Freeze the layers in the base model
    for layer in base_model.layers:
        layer.trainable = False

    # Add custom classification layers on top of the base model
    x = base_model.output
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dense(1024, activation='relu')(x)
    predictions = keras.layers.Dense(NUM_CLASSES, activation='softmax')(x)

    # Create the final model
    model = Model(inputs=base_model.input, outputs=predictions)

    # Compile the model
    optimizer = keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    checkpoint = ModelCheckpoint(filepath=WEIGHT_PATH, verbose=1, save_best_only=True, monitor='val_accuracy', mode='max')
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

def ImageSegmentation():
    #load image and image sementation
    sample_test = load_img(data_path)
    mask = remove(sample_test)
    bg = load_img(BACKGROUND_PATH)
    segmented_img = Image.composite(sample_test, bg, mask)
    segmented_img = segmented_img.crop((80, 0, 560, 480))
    segmented_img.save(f"segmented_sample.jpg")

    return segmented_img

def classify():
    model = create_model()

    # Checking model best performance score with data test
    model.load_weights(WEIGHT_PATH)

    #load segmented_image
    my_image = load_img(data_path, target_size=IMG_SIZE)

    #preprocess the image
    my_image = img_to_array(my_image)
    my_image = my_image.reshape((1, my_image.shape[0], my_image.shape[1], my_image.shape[2]))
    my_image = preprocess_input(my_image)

    #make the prediction
    class_names = ["BOHEA", "BOP", "BOPF", "DUST", "DUST2", "F1", "F2", "PF", "PF2", "PF3"]
    class_probability = model.predict(my_image)
    class_name = np.argmax(class_probability, axis=1)
    print(class_names[class_name[0]])

def main():
    classify()

if __name__ == "__main__":
    main()