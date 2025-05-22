import streamlit as st
import pickle
import numpy as np
from PIL import Image
import os

# Load model and label encoder once
model = pickle.load(open(r"C:\Users\Utsav\OneDrive\Desktop\FARMCAST AI\model.pkl", "rb"))
label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))

st.title("Farmcast Crop Prediction")

st.write("Enter the following parameters:")

N = st.number_input("Nitrogen (N)", min_value=0.0, max_value=140.0, value=50.0)
P = st.number_input("Phosphorous (P)", min_value=0.0, max_value=140.0, value=50.0)
K = st.number_input("Potassium (K)", min_value=0.0, max_value=205.0, value=50.0)
temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)
ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=6.5)
rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=300.0, value=100.0)

if st.button("Predict Crop"):
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    prediction = model.predict(features)
    crop = label_encoder.inverse_transform(prediction)[0]

    st.success(f"Predicted Crop: {crop}")

    # Show crop image if available
    image_path = os.path.join('images', f"{crop.lower()}.jpg")
    if os.path.exists(image_path):
        img = Image.open(image_path)
        st.image(img, caption=crop)
    else:
        st.warning("No image available for this crop.")
