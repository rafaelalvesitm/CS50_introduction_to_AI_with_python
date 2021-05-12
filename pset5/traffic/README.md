# Process taken

This file contains additional information on the parameters used to train a machine learning algorithm to identify road signs. 

#  Tested 
model = tf.keras.models.Sequential([
tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),

tf.keras.layers.Conv2D(32, (2, 2), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),

tf.keras.layers.Flatten(),

tf.keras.layers.Dense(256, activation="relu"),
tf.keras.layers.Dropout(0.5),


tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])

Accuracy train data = 0.9496
Accuracy test data = 0.9701
