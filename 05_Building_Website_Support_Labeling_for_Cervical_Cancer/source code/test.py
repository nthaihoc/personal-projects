import pandas as pd
import json
import tensorflow as tf
import cv2
import os
import gradio as gr
from PIL import Image
import numpy as np

def process_upload_file(root_folder):
    """
    Define function return list image then user upload folder
        Args: path_folder
        Results: [image1.jpg, image2.jpg,.v.v]
    """

    img = []
    for i in root_folder:
        img.append(i)

    return img

def information(img_path):
    """
    Define a function to show index, name, height and width fog images, after user
    selects any image in galery
        - Args: image_path
        - Result: [0, image1.jpg, 200, 300]
    """
    
    img_name = img_path.value['image']['path']
    img = cv2.imread(img_name)

    h, w, _ = img.shape

    return img_path.index, img_name, h, w

def suggestion_label(img_path):
    """
    Define a function to predict label for image, after user selects any image in gallery
        - Args: image_path
        - Result: [20%, 30%, 40%, v.v.]
    """

    model = tf.keras.models.load_model("/home/thaihocit02/thaihoc/iast-ictu/resources/alone/224/model/InceptionV3.keras")
    img = img_path.value["image"]["path"]
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resize = cv2.resize(img, (224, 224))
    img_array = np.array(img_resize).astype("float32") / 255.0
    img_batch = np.expand_dims(img_array, axis=0)
    results = model.predict(img_batch)

    return (
        f"- ASC_H: {results[0][0]*100:.2f}%\n"
        f"- ASC_US: {results[0][1]*100:.2f}%\n"
        f"- HSIL: {results[0][2]*100:.2f}%\n"
        f"- LSIL: {results[0][3]*100:.2f}%\n"
        f"- SCC: {results[0][4]*100:.2f}%\n"
    )

def process_image(img_path: gr.SelectData):
    """
    Define a function to process two functions information and suggestion_label simultaneously
    """

    index, img_name, h, w = information(img_path)
    label = suggestion_label(img_path)

    return f"- Index: {index}\n- Filename: {img_name.split("/")[-1]}\n- Size: {w} x {h}", label, img_name

def add_option_label(new_label):
    """
    Define a function to add label if user wants extend label
    """

    add = gr.Radio(choices=[new_label])
    return add

def show_and_update_dataframe(img_path, label, df_current):
    """
    Define a function show and update dataframe
    """

    filename = img_path.split("/")[-1]
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    
    new_row = pd.DataFrame(data=[[filename, h, w, label]], columns=["Filename", "Height", "Width", "Label"])

    df_state = pd.concat([df_current, new_row], ignore_index=True)

    return df_state, df_state

def download_dataframe(df_current, file_format):
    """
    Define a function to download dataframe, user can download file
    """
    if file_format == ".csv":
        path = "datasets.csv"
        df_current.to_csv(path, index=False)
    elif file_format == ".txt":
        path = "datasets.txt"
        df_current.to_csv(path, index=False)
    else:
        pass

    return path
        
"""
Setup layouts for upload file state
"""
upload_file = gr.UploadButton(label="Upload File",
                              file_count="directory",
                              size="lg",
                              variant="stop")

"""
Setup layouts for show all image in galery
"""
show_file = gr.Gallery(label="Show Image",
                      show_label=True,
                      columns=5,
                      rows=2,
                      object_fit="fill",
                      height=300,
                      interactive=False,
                      allow_preview=True)

"""
Setup layouts for show information image state
"""
show_info_file = gr.Textbox(lines=3, show_label=True, label="Information of image")

"""
Setup layouts for show suggetion label model state
"""
show_suggest_model = gr.Textbox(lines=5, show_label=True, label="Recommended label for images")

"""
Setup layouts for show select label state
"""
select_label = gr.Radio(choices=["ASC_H", "ASC_US", "HSIL", "LSIL", "SCC"], label="Option label", show_label=True, interactive=True)

"""
Setup layouts for add label state
"""
add_label = gr.Textbox(label="Add label", show_label=True)

"""
Setup layouts for show images, after user select image to galery
"""
show_single_image = gr.Image(label="You select image", 
                             show_label=True, 
                             image_mode="RGB", 
                             type="filepath",
                             height=500,
                             width=500,
                             interactive=False)

"""
Setup layouts for dataframe live
"""
show_dataframe = gr.Dataframe(label="Datasets in the current session", show_label=True, interactive=True)

"""
Setup layouts for select file format
"""
show_format_file = gr.Dropdown([".csv", ".txt", ".json"], 
                               label="File format selection", 
                               show_label=True,
                               interactive=True)

with gr.Blocks(theme="citrus", fill_height=True, fill_width=True) as demo:
    """
    Setup application with name is demo
    """

    df_state = gr.State(value=pd.DataFrame(columns=["Filename", "Height", "Width", "Label"]))

    with gr.Row():
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("<h3 style='text-align: center;'>Live Datasets</h3>")
            show_dataframe.render()
            show_format_file.render()
            download = gr.Button(value="Get Link Download", variant="huggingface")
            download_file = gr.File(label="Link download", type="filepath", interactive=False)

        with gr.Column(scale=2, variant="panel"):
            gr.Markdown("<h1 style='text-align: center;'>Welcome to IAST LabelMaster </h1>")
            gr.Markdown("<h4 style='text-align: center;'><i>Accelerate labeling - Optimize efficiency</i></h4>")
            upload_file.render()
            show_file.render()
            show_single_image.render()

        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("<h3 style='text-align: center;'>Image Information</h3>")
            show_info_file.render()
            gr.Markdown("<h3 style='text-align: center;'>Label Suggestion Model</h3>")
            show_suggest_model.render()
            gr.Markdown("<h3 style='text-align: center;'>Image Annotation</h3>")
            select_label.render()
            add_label.render()
            save = gr.Button(variant="huggingface",value="Save")

    
    """
    Process events when user iteracts
    """

    upload_file.upload(fn=process_upload_file, inputs=upload_file, outputs=show_file)

    show_file.select(fn=process_image, inputs=None, outputs=[show_info_file, show_suggest_model, show_single_image])

    add_label.submit(fn=add_option_label, inputs=add_label, outputs=select_label)

    save.click(fn=show_and_update_dataframe, inputs=[show_single_image, select_label, df_state], outputs=[show_dataframe, df_state])
    download.click(fn=download_dataframe, inputs=[df_state, show_format_file], outputs=download_file)

if __name__ == "__main__":
    demo.queue()
    demo.launch()
