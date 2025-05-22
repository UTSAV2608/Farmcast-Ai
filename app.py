import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os
import glob
import pyttsx3

# Set page config
st.set_page_config(page_title="🌾 Farmcast - Crop Predictor", page_icon="🌱")

# Inject custom CSS for background from URL
def set_bg_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background image
bg_url = "https://www.canowindraphoenix.com.au/wp-content/uploads/2020/05/samll-farms.jpeg"
set_bg_from_url(bg_url)

# Load model and label encoder
@st.cache_resource
def load_model():
    model = pickle.load(open('model.pkl', 'rb'))
    label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))
    return model, label_encoder

model, label_encoder = load_model()

# TTS function
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

# Title and instructions
st.markdown("<h1 style='color:white;'>🌾 Farmcast - Crop Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:white;'>Enter your soil and climate parameters to get the best crop recommendation:</p>", unsafe_allow_html=True)

# Input form
with st.form("prediction_form"):
    N = st.number_input("Nitrogen (N)", 0.0, 140.0, 50.0)
    P = st.number_input("Phosphorous (P)", 0.0, 140.0, 50.0)
    K = st.number_input("Potassium (K)", 0.0, 205.0, 50.0)
    temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, 50.0)
    ph = st.number_input("pH", 0.0, 14.0, 6.5)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 100.0)
    submitted = st.form_submit_button("🔍 Predict Crop")

# Prediction logic
if submitted:
    try:
        features = [N, P, K, temperature, humidity, ph, rainfall]
        prediction = model.predict([features])
        crop = label_encoder.inverse_transform(prediction)[0]
        crop_name = crop.capitalize()

        st.success(f"✅ Recommended Crop: {crop_name}")
        speak(f"The recommended crop is {crop_name}")

        # Show crop image
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
