import streamlit as st
import numpy as np
import pickle
from PIL import Image
import pyttsx3
import os

# Load model and label encoder
model = pickle.load(open('model.pkl', 'rb'))
label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))

# Set Streamlit page config
st.set_page_config(page_title="FarmCast AI", layout="centered")

# Inject background image with custom CSS
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://tse3.mm.bing.net/th?id=OIP.K5BnxGupFhptX4eIG8LMjQHaEK&pid=Api&P=0&h=180");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .glass {
        background: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
    }
    </style>
""", unsafe_allow_html=True)

# Text-to-speech function
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        st.warning("TTS not supported on this system.")

# Main form in a glass effect box
with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.title("FarmCast AI")

    st.markdown("""
    Enter the following details to get the best crop suggestion based on your soil and weather conditions:
    """)

    with st.form("crop_form"):
        N = st.number_input("Nitrogen (N)", min_value=0.0, max_value=140.0, step=1.0)
        P = st.number_input("Phosphorus (P)", min_value=5.0, max_value=145.0, step=1.0)
        K = st.number_input("Potassium (K)", min_value=5.0, max_value=205.0, step=1.0)
        temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, step=0.1)
        humidity = st.number_input("Humidity (%)", min_value=10.0, max_value=100.0, step=0.1)
        ph = st.number_input("Soil pH", min_value=3.5, max_value=9.0, step=0.1)
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=300.0, step=1.0)

        submitted = st.form_submit_button("Predict")

    if submitted:
        try:
            features = [N, P, K, temperature, humidity, ph, rainfall]
            prediction = model.predict([features])
            crop = label_encoder.inverse_transform(prediction)[0]
            image_path = f"{crop.lower()}.jpg"

            st.success(f"FarmCast AI: **{crop}**")
            speak(f"The recommended crop is {crop}")

            if os.path.exists(image_path):
                img = Image.open(image_path)
                st.image(img, caption=f"{crop.capitalize()}", use_column_width=True)
            else:
                st.warning("Image not found for the predicted crop.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
