import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os
import glob

# Set page configuration
st.set_page_config(page_title="Farmcast - Crop Predictor", page_icon="🌾")

# Load model and label encoder with caching
@st.cache_resource
def load_model_and_encoder():
    try:
        model = pickle.load(open("model.pkl", "rb"))
        label_encoder = pickle.load(open("label_encoder.pkl", "rb"))
        return model, label_encoder
    except Exception as e:
        st.error(f"Error loading model or label encoder: {e}")
        return None, None

model, label_encoder = load_model_and_encoder()

# App title
st.title("🌾 Farmcast - Smart Crop Predictor")
st.markdown("Provide soil and climate parameters to predict the most suitable crop for your farm.")

# Input form
with st.form("crop_prediction_form"):
    st.subheader("Enter Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        N = st.number_input("🧪 Nitrogen (N)", 0.0, 140.0, 50.0)
        P = st.number_input("🧪 Phosphorous (P)", 0.0, 140.0, 50.0)
        K = st.number_input("🧪 Potassium (K)", 0.0, 205.0, 50.0)

    with col2:
        temperature = st.number_input("🌡️ Temperature (°C)", 0.0, 50.0, 25.0)
        humidity = st.number_input("💧 Humidity (%)", 0.0, 100.0, 50.0)

    with col3:
        ph = st.number_input("⚖️ pH Level", 0.0, 14.0, 6.5)
        rainfall = st.number_input("🌧️ Rainfall (mm)", 0.0, 300.0, 100.0)

    submit = st.form_submit_button("🔍 Predict Crop")

# Prediction logic
if submit and model and label_encoder:
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    try:
        prediction = model.predict(features)
        crop = label_encoder.inverse_transform(prediction)[0]
        st.success(f"✅ Recommended Crop: **{crop.capitalize()}**")

        # Attempt to display image of the predicted crop
        image_folder = "images"
        image_pattern = os.path.join(image_folder, f"{crop.lower()}.*")
        image_files = glob.glob(image_pattern)

        if image_files:
            img = Image.open(image_files[0])
            st.image(img, caption=crop.capitalize(), use_column_width=True)
        else:
            st.info("ℹ️ No image available for this crop.")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
