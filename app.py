from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(_name_)

# Load model and label encoder
model = pickle.load(open('model.pkl', 'rb'))
label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [
            float(request.form['N']),
            float(request.form['P']),
            float(request.form['K']),
            float(request.form['temperature']),
            float(request.form['humidity']),
            float(request.form['ph']),
            float(request.form['rainfall'])
        ]

        prediction = model.predict([features])
        crop = label_encoder.inverse_transform(prediction)[0]
        image_filename = f"{crop.lower()}.jpg"

        return render_template('result.html', crop=crop, image=image_filename)
    
    except Exception as e:
        return f"Error: {e}"

if _name_ == '_main_':
    app.run(debug=True)
