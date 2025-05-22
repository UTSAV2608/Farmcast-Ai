import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os
import pyttsx3
import glob

# Configure Streamlit page
st.set_page_config(layout="centered", page_title="Farmcast AI")

# Inject background image & glass effect CSS
st.markdown(f"""
    <style>
    .stApp {{
        background: url('https://www.canowindraphoenix.com.au/wp-content/uploads/2020/05/samll-farms.jpeg') no-repeat center center fixed;
        background-size: cover;
    }}
    .form-container {{
        background-color: rgba(0, 0, 0, 0.65);
        padding: 40px 30px;
        border-radius: 15px;
        max-width: 500px;
        margin: 5% auto;
        color: white;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    }}
    .form-container h1 {{
        text-align: center;
        color: white;
        font-size: 2.4rem;
        margin-bottom: 25px;
    }}
    </style>
""", unsafe_allow_html=True)

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

# Render UI
st.markdown('<div class="form-container">', unsafe_allow_html=True)

# Logo (Optional - replace URL with your own if needed)
st.image("https://i.ibb.co/yV1fVKf/farmcast-logo.png", width=100)

st.markdown('<h1>FARMCAST AI</h1>', unsafe_allow_html=True)

with st.form("crop_form"):
    N = st.text_input("Nitrogen")
    P = st.text_input("Phosphorus")
    K = st.text_input("Potassium")
    temperature = st.text_input("Temperature")
    humidity = st.text_input("Humidity")
    ph = st.text_input("pH")
    rainfall = st.text_input("Rainfall")
    submitted = st.form_submit_button("Predict")

st.markdown('</div>', unsafe_allow_html=True)

# Prediction and Output
if submitted:
    try:
        features = [float(N), float(P), float(K), float(temperature), float(humidity), float(ph), float(rainfall)]
        prediction = model.predict([features])
        crop = label_encoder.inverse_transform(prediction)[0].capitalize()

        st.success(f"🌿 Recommended Crop: {crop}")
        speak(f"The recommended crop is {crop}")

        # Show crop image
        image_path = glob.glob(os.path.join("images", f"{crop.lower()}.*"))
        if image_path:
            st.image(Image.open(image_path[0]), caption=crop, use_column_width=True)
        else:
            st.warning("No image available for this crop.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
