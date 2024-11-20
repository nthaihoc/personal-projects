import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import pandas as pd
import os
from config import set_background, classification, encode_y
from streamlit_option_menu import option_menu


# create option menu
with st.sidebar:
    selected = option_menu("Menu",
                           ["Trang chủ", "Tài liệu hướng dẫn", "Giới thiệu", "Dự đoán", "Xem lịch sử"],
                           icons=["bi bi-house", "brush","file-earmark-pdf", "bullseye", "clock-history"],
                           menu_icon="cast",
                           default_index=0)

# processing option
if (selected=="Trang chủ"):
    set_background("./images/back_ground.jpg")
    st.markdown('<h1 style="text-align:center;">Website Hỗ Trợ Phân Loại Ung Thư Cổ Tử Cung</h1>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<h3 style="color:white"> Tên của bạn là gì ?</h3>', unsafe_allow_html=True)
    name_user = st.text_input(" ", "")
    name_user = name_user.title()
    st.markdown("---")
    if name_user:
        st.markdown('<h3 style="color:white;"> Hello {}. Chào mừng bạn đến với Website của chúng tôi !</h3>'.format(name_user), unsafe_allow_html=True)

if (selected=="Giới thiệu"):
    set_background("./images/introduction.jpg")
    st.markdown('<h1 style="text-align:center"> Giới thiệu về Website </h1>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown('<p style="text-align:left";>Ung thư cổ tử cung là một trong những nguyên nhân gây tử vong hàng đầu ở phụ nữ. Chúng thường xảy ra ở các tế bào phía dưới của tử cung, do virus và có nguy cơ lây nhiễm cao qua quan hệ tình dục. Các con số thống kê cho thấy, ung thư cổ tử cung là một trong những nguyên nhân gây tử vong thứ hai, trong số các bệnh ác tính ở phụ nữ.</p>', unsafe_allow_html=True)
    st.image('./images/ccs.jpg', caption="Ung thư cổ tử cung", use_column_width=True)
    st.markdown("Những năm gần đây với sự phát triển của khoa học dữ liệu và trí tuệ nhân tạo. Đã có rất nhiều nghiên cứu xoay quanh việc phát hiện sớm căn bệnh này, bằng cách sử dụng các phương pháp học máy và học sâu, nhằm làm giảm đi sự nguy hiểm mà chúng mang lại. Tuy nhiên các nghiên cứu cũng gặp rất nhiều khó khăn, do sự khan hiếm về dữ liệu thực tế bên cạnh đó y tế cũng là một lĩnh vực mang tính nhạy cảm.")   
    st.markdown("Trong Website này chúng tôi đã tích hợp lõi là các phương pháp học sâu và mô hình hiện đại, đã được huấn luyện trên các bộ dữ liệu rất lớn và dữ liệu thực tế. Các mô hình này, được chúng tôi thiết kế và triển khai huấn luyện trên tập dữ liệu bao gồm 5 loại tế bào ung thư cổ tử cung phổ biến: ASC_H, ASC_US, HSIL, LSIL và SCC.")
    st.image("./images/datasets.png", caption="5 loại tế bào ung thư cổ tử cung phổ biến", use_column_width=True)
    st.markdown("Với niềm đam mê về AI, đặc biệt là trong lĩnh vực y tế. Chúng tôi đã triển khai ứng dụng website này với mục tiêu cùng hi vọng rằng: Website này là một công cụ, có thể giúp đỡ người dùng đặc biệt là các bác sĩ trong lĩnh vực tế bào học, trong việc chẩn đoán và đưa ra các quyết định, góp phần gia tăng năng suất và tối ưu hóa thời gian công việc.")
    st.markdown("---")
    st.markdown('<h6 style="text-align:center";>Trân Trọng</h6>', unsafe_allow_html=True)
    st.markdown('<h6 style="text-align:center";>Admin</h6>', unsafe_allow_html=True)

if (selected=="Tài liệu hướng dẫn"):
    set_background("./images/doccumentation.jpg")
    st.markdown('<h1 style="text-align:center"> Tài liệu hướng dẫn </h1>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## I. Thông tin")
    st.markdown("Đây là tài liệu hướng dẫn sử dụng các chức năng của website. Website được thiết kế với giao diện đơn giản, gần gũi và dễ sử dụng. Một số chức năng cơ bản của Website như: giới thiệu về Website, hướng dẫn sử dụng, phân loại hình ảnh và giúp người dùng xem lại lịch sử.")
    st.image("./images/1.png", caption="Website Interface")
    st.markdown("## II. Các chức năng của Website")
    st.markdown("### 1. Giới thiệu")
    st.markdown("Phần này là giới thiệu tổng quan về Website. Giúp người dùng nắm bắt được các thông tin, công nghệ được áp dụng và mục tiêu của Website.")
    st.image("./images/2.png", caption="Introduction of Website")
    st.markdown("### 2. Dự đoán")
    st.markdown("Đây là chức năng chính và quan trọng nhất của Website. Chức năng này được tích hợp cùng với các mô hình AI để đưa ra các kết quả cho người dùng.")

    

if "list_name" not in st.session_state:
    st.session_state.list_name = []
if "prob_asc_h" not in st.session_state:
    st.session_state.prob_asc_h = []
if "prob_asc_us" not in st.session_state:
    st.session_state.prob_asc_us = []
if "prob_hsil" not in st.session_state:
    st.session_state.prob_hsil = []
if "prob_lsil" not in st.session_state:
    st.session_state.prob_lsil = []
if "prob_scc" not in st.session_state:
    st.session_state.prob_scc = []
if "label" not in st.session_state:
    st.session_state.label = []


if (selected=="Dự đoán"):
    set_background("./images/prediction.jpg")
    st.markdown('<h1 style="text-align:center;"> Dự đoán và phân loại hình ảnh tế bào </h1>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<h3> --> Xin hãy tải ảnh của bạn ở đây </h3>', unsafe_allow_html=True)

    file_upload = st.file_uploader("", type=["jpeg", "jpg", "png"])

    if file_upload is not None:
        image = Image.open(file_upload).convert("RGB")

        st.image(image, use_column_width=True)
        
        model = tf.keras.models.load_model("InceptionResNetV2.keras")

        predicted = classification(image, model)
        preds = np.argmax(predicted)
        preds = encode_y(preds)

        st.session_state.list_name.append(file_upload.name)
        st.session_state.prob_asc_h.append("{:.2f}".format(predicted[0][0]*100))
        st.session_state.prob_asc_us.append("{:.2f}".format(predicted[0][1]*100))
        st.session_state.prob_hsil.append("{:.2f}".format(predicted[0][2]*100))
        st.session_state.prob_lsil.append("{:.2f}".format(predicted[0][3]*100))
        st.session_state.prob_scc.append("{:.2f}".format(predicted[0][4]*100))
        st.session_state.label.append(preds)

        labels = ["ASC_H", "ASC_US", "HSIL", "LSIL", "SCC"]

        st.markdown("---")
        st.markdown('<h3> --> Kết quả phân loại </h3>', unsafe_allow_html=True)

        for name, prob in zip(labels, predicted[0]*100):
            st.markdown('*<h5 style="color:red; text-align:center ">@ Tế bào {} -> Xác suất mô hình dự đoán là : {:.2f}%</h5>*'.format(name, prob), unsafe_allow_html=True)

         
if (selected=="Xem lịch sử"):
    set_background("./images/history.jpg")
    st.markdown('<h1 style="text-align:center"> Lịch sử dự đoán hình ảnh </h1>', unsafe_allow_html=True)
    st.markdown("---")
    #st.markdown('<p style="text-align:center; color:red;">Chú ý: Những giá trị bôi vàng tương ứng với nhãn mà mô hình đề xuất cho hình ảnh của bạn.</p>', unsafe_allow_html=True)

    df = pd.DataFrame()

    df["Tên ảnh"] = st.session_state.list_name
    df["ASC_H"] = st.session_state.prob_asc_h
    df["ASC_US"] = st.session_state.prob_asc_us
    df["HSIL"] = st.session_state.prob_hsil
    df["LSIL"] = st.session_state.prob_lsil
    df["SCC"] = st.session_state.prob_scc
    df["Đề xuất"] = st.session_state.label

    st.dataframe(df.style.highlight_max(axis=0), width=1200, height=400)

