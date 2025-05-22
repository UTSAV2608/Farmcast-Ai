import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os
import glob
# Title
st.set_page_config(page_title="Crop Predictor", page_icon="🌱")
st.title("🌾 Farmcast - Crop Prediction")

st.write("Enter the following parameters to predict the suitable crop:")
# Load model and label encoder
@st.cache_resource
def load_model():
    model = pickle.load(open('model.pkl', 'rb'))
    label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))
    return model, label_encoder

model, label_encoder = load_model()



# Input form to mimic HTML form
with st.form("prediction_form"):
    N = st.number_input("Nitrogen (N)", 0.0, 140.0, 50.0)
    P = st.number_input("Phosphorous (P)", 0.0, 140.0, 50.0)
    K = st.number_input("Potassium (K)", 0.0, 205.0, 50.0)
    temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, 50.0)
    ph = st.number_input("pH", 0.0, 14.0, 6.5)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 100.0)

    submitted = st.form_submit_button("Predict Crop")

# Prediction logic on submit
if submitted:
    try:
        features = [N, P, K, temperature, humidity, ph, rainfall]
        prediction = model.predict([features])
        crop = label_encoder.inverse_transform(prediction)[0]
        st.success(f"✅ Predicted Crop: **{crop.capitalize()}**")

        # Display image of the crop if available
        image_folder = "images"
        image_pattern = os.path.join(image_folder, f"{crop.lower()}.*")
        image_files = glob.glob(image_pattern)

        if image_files:
            img = Image.open(image_files[0])
            st.image(img, caption=crop.capitalize(), use_column_width=True)
        else:
            st.info("ℹ️ No image available for this crop.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
