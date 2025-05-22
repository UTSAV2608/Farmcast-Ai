from flask import Flask, render_template, request
import pickle
import numpy as np
from keras.preprocessing import image
import io
import os  # Add this for path operations

app = Flask(__name__)

# Assuming your model is saved as 'crop_recommendation_model.pkl'
model_path = os.path.join(app.root_path, 'crop_recommendation_model.pkl')  # Get the model path
with open(model_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']
        img_data = file.read()
        img = image.load_img(io.BytesIO(img_data), target_size=(64, 64))

        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        prediction = model.predict(img_array)
        # Process prediction and return result
        # ...
        return "Prediction result"  # Replace with actual prediction handling

if __name__ == '__main__':
    app.run(debug=True)
    
