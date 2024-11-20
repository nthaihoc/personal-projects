import base64
import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image, ImageOps

def set_background(image_file):

    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


def classification(file, model):

    image_resize = file.resize((224, 224))

    image_array = np.array(image_resize).astype("float32") / 255.0

    image_array = np.expand_dims(image_array, axis=0)

    pred = model.predict(image_array)

    return pred

def encode_y(y):
    if y == 0:
        return "ASC_H"
    if y == 1:
        return "ASC_US"
    if y == 2:
        return "HSIL"
    if y == 3 :
        return "LSIL"
    if y == 4 :
        return "SCC"
