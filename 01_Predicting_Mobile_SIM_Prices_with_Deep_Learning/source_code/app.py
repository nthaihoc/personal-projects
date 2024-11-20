from keras.models import load_model, save_model
import streamlit as st 
from streamlit_option_menu import option_menu
import numpy as np

# load models

price_sim_models = load_model("model_predict_sim_value_1.h5")

# sidebar

with st.sidebar:
    selected = option_menu("Predict Systems",
                           ["Predict Sim Price Model"],
                           icons=["sim-fill"],
                           
                           default_index=0)

if (selected == "Predict Sim Price Model"):
    st.title("Predict Sim Price Using Long Short Term Memory")

    phone_number = st.text_input("Nhập số điện thoại của bạn")
    digits = [int(d) for d in str(phone_number)]
    digits = digits[1:10]
    phone_number_array = np.array(digits)
    phone_number_array = np.reshape(phone_number_array, (-1, 9, 1))

    dianogis = ''

    if st.button("Dự đoán"):
        results = price_sim_models.predict(phone_number_array)
        x = np.argmax(results)
        
        if x == 0:
            dianogis = "Sim có giá khoảng từ 0 -> 500.000"
        if x == 1:
            dianogis = "Sim có giá khoảng từ 500.000 -> 700.000"
        if x == 2:
            dianogis = "Sim có giá khoảng từ 700.000 -> 900.000"
        if x == 3:
            dianogis = "Sim có giá khoảng từ 900.000 -> 1.000.000"
        if x == 4:
            dianogis = "Sim có giá khoảng từ 1.000.000 -> 1.200.000"
        if x == 5:
            dianogis = "Sim có giá khoảng từ 1.200.000 -> 1.500.000"
        if x == 6:
            dianogis = "Sim có giá khoảng từ 1.500.000 -> 3.000.000"
        if x == 7:
            dianogis = "Sim có giá khoảng từ 3.000.000 -> 6.000.000"
        if x == 8:
            dianogis = "Sim có giá lớn hơn 6.000.000"

    st.success(dianogis)



