from flask import Flask, render_template, request
import numpy as np
import pickle
import os

app = Flask(__name__)

# Load the trained model and label encoder
model = pickle.load(open('model.pkl', 'rb'))
label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from form
        features = [
            float(request.form['N']),
            float(request.form['P']),
            float(request.form['K']),
            float(request.form['temperature']),
            float(request.form['humidity']),
            float(request.form['ph']),
            float(request.form['rainfall'])
        ]

        # Predict using the model
        prediction = model.predict([features])
        crop = label_encoder.inverse_transform(prediction)[0]

        # Image filename (should be in static/images/)
        image_filename = f"images/{crop.lower()}.jpg"

        return render_template('result.html', crop=crop, image=image_filename)

    except Exception as e:
        return render_template('error.html', message=str(e))

# Run the app (Render requires host='0.0.0.0' and dynamic port)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
