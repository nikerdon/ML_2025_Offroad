#frontend streamlit app for ML 2025 project 2
#simple test script

import streamlit as st 
import cv2 as cv
import requests
from requests.exceptions import ConnectionError

ip_api = "127.0.0.1"
port_api = "5000"

# Заголовок приложения
st.title("Offroad Segmentation Prediction")

#https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
#https://docs.streamlit.io/develop/api-reference/media/st.image


img_types = ["bmp", "dip", "jpg", "jpeg", "jpe", "jp2", "png", "webp", "tiff", "tif", "pbm", "pgm", "ppm", "sr", "ras"]

uploaded_file = st.file_uploader("Choose an image", type=img_types)#, on_change=None, args=None, kwargs=None)

if uploaded_file is not None:
    img = cv.imread(uploaded_file.getvalue())
    if img == None:
        st.error("Image could not be read.")
    else:
        # pass image to backend, get an image as a result
        try:
            # Отправка запроса к Flask API
            response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json=uploaded_file.getvalue())

            # Проверка статуса ответа
            if response.status_code == 200:
                image = response.json()["prediction"]
                if image != None:
                    st.success(f"Predicted Segmentation:")
                    st.image(image, width=None, clamp=True, channels="BGR", output_format="PNG")
                else:
                    st.error(f"No image returned.")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except ConnectionError as e:
            st.error(f"Failed to connect to the server")


    





