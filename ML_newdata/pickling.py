import tensorflow as tf

load_options = tf.saved_model.LoadOptions()
load_options.experimental_io_device = (
    "/job:localhost"  # Set the experimental_io_device option
)

model = tf.keras.models.load_model("model2")

print(model.predict())
