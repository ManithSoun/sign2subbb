import tensorflow as tf

# Load the model
model = tf.keras.models.load_model("../frontend/model/keras_model.h5")


# Save in TensorFlow's SavedModel format
model.save("saved_model")

# Export to TFLite as well
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open("model.tflite", "wb") as f:
    f.write(tflite_model)
