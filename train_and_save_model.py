import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load the dataset (make sure the filename is correct and in the same folder)
data = pd.read_csv("Crop_recommendation.csv")

# Define features and target
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# Encode crop labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train the model
model = RandomForestClassifier()
model.fit(X, y_encoded)

# Save the trained model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save the label encoder
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Model and label encoder saved successfully.")
