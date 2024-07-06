from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from keras.models import load_model

def detect(image_path):
    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    with open("labels.txt", "r") as file:
        class_names = file.readlines()

    # Open the image
    image = Image.open(image_path).convert("RGB")

    # Define the size for resizing and cropping
    size = (224, 224)

    # Resize and crop the image to 224x224
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Convert the image to a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Prepare the data for prediction
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Predict the class of the image
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    return class_name, confidence_score