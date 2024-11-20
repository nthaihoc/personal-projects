from PIL import Image
import numpy as np
import tensorflow as tf
import pandas as pd


file = "./prediction.jpg"
image = Image.open(file)
image_resize = image.resize((224, 224))

image_array = np.array(image_resize).astype("float32") / 255.0
image_array = np.expand_dims(image_array, axis=0)


model = tf.keras.models.load_model("InceptionResNetV2.keras")

pred = model.predict(image_array)


prob_asc_h = []
prob_asc_us = []
prob_hsil = []
prob_lsil = []
prob_scc = []

prob_asc_h.append(pred[0][0])
prob_asc_us.append(pred[0][1])
prob_hsil.append(pred[0][2])
prob_lsil.append(pred[0][3])
prob_scc.append(pred[0][4])    

df = pd.DataFrame()
df["Name"], df["ASC_H"], df["ASC_US"], df["HSIL"] = file, prob_asc_h, prob_asc_us, prob_hsil

print(df)







