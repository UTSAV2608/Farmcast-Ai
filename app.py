import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os
import glob
import pyttsx3

# Set page config
st.set_page_config(page_title=" FarmCast Logo FARMCAST AI", page_icon="🌱")

# Background Image Setup using Custom CSS
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded = img_file.read()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:https://www.canowindraphoenix.com.au/wp-content/uploads/2020/05/samll-farms.jpeg;base64,{encoded.hx()}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Apply the background image (replace 'background.jpg' with your image)
set_background("https://www.canowindraphoenix.com.au/wp-content/uploads/2020/05/samll-farms.jpeg")

# Load model and label encoder
@st.cache_resource
def load_model():
    model = pickle.load(open('model.pkl', 'rb'))
    label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))
    return model, label_encoder

model, label_encoder = load_model()

# Initialize TTS engine
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

# UI Content
st.markdown("<h1 style='color:white;'>🌾 Farmcast - Crop Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:white;'>Enter the values below to get the best crop recommendation:</p>", unsafe_allow_html=True)

# Input Form
with st.form("prediction_form"):
    N = st.number_input("Nitrogen (N)", 0.0, 140.0, 50.0)
    P = st.number_input("Phosphorous (P)", 0.0, 140.0, 50.0)
    K = st.number_input("Potassium (K)", 0.0, 205.0, 50.0)
    temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, 50.0)
    ph = st.number_input("pH", 0.0, 14.0, 6.5)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 100.0)
    submitted = st.form_submit_button("🔍 Predict Crop")

# Prediction Logic
if submitted:
    try:
        features = [N, P, K, temperature, humidity, ph, rainfall]
        prediction = model.predict([features])
        crop = label_encoder.inverse_transform(prediction)[0]
        crop_name = crop.capitalize()

        st.success(f"✅ Recommended Crop: {crop_name}")
        speak(f"The recommended crop is {crop_name}")

        # Show image if exists
        image_folder = "images"
        image_pattern = os.path.join(image_folder, f"{crop.lower()}.*")
        image_files = glob.glob(image_pattern)

        if image_files:
            img = Image.open(image_files[0])
            st.image(img, caption=crop_name, use_column_width=True)
        else:
            st.info("ℹ️ No image available for this crop.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
