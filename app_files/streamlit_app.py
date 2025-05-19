#frontend streamlit app for ML 2025 project 2
#simple test script

import streamlit as st 
import requests
from requests.exceptions import ConnectionError
#in order to read the image
from PIL import Image 
import cv2 as cv
# in order to send the image in the correct format
import numpy as np 
import json

ip_api = "127.0.0.1"
port_api = "5000"

# Заголовок приложения
st.title("Offroad Segmentation Prediction")

#https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
#https://docs.streamlit.io/develop/api-reference/media/st.image


#img_types = ["bmp", "dip", "jpg", "jpeg", "jpe", "jp2", "png", "webp", "tiff", "tif", "pbm", "pgm", "ppm", "sr", "ras"]
img_types = ["jpg", "jpeg"]

uploaded_file = st.file_uploader("Choose an image", type=img_types)#, on_change=None, args=None, kwargs=None)

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img.save('img.jpg') # I could send the file path instead, but this way there will not be an issue regarding where the image is stored
    img = cv.imread('img.jpg')
    if img is None:
        st.error("Image could not be read.")
    else:
        st.image(img, width=None, clamp=True, channels="BGR", output_format="PNG")
        # change the type of the image
        #st.text(img.shape) HWC
        #json_img = json.dumps(img.tolist())
        #st.image(arr, width=None, clamp=True, channels="BGR", output_format="PNG")
        # pass image to backend, get an image as a result
        try:
            # Отправка запроса к Flask API
            #response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json={"image": "img.jpg"})
            response = requests.get(f"http://{ip_api}:{port_api}/predict_model")

            # Проверка статуса ответа
            if response.status_code == 200:
                image = cv.imread('mask.png')#response.json()["prediction"]
                if image is not None:
                    st.success(f"Predicted Segmentation:")
                    #python_img = json.loads(image)
                    #img_ret = np.array(python_img)
                    st.image(image, width=None, clamp=True, channels="BGR", output_format="PNG")
                else:
                    st.error(f"No image returned.")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except ConnectionError as e:
            st.error(f"Failed to connect to the server")


    





