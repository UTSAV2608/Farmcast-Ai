from gtts import gTTS
import os

# Create the output folder if it doesn't exist
audio_path = os.path.join('static', 'audio')
os.makedirs(audio_path, exist_ok=True)

# List of crop names (make sure these match the ones your model predicts)
crop_names = [
    "apple", "banana", "blackgram", "chickpea", "coconut", "coffee",
    "cotton", "grapes", "jute", "kidneybeans", "lentil", "maize",
    "mango", "mothbeans", "mungbean", "muskmelon", "orange", "papaya",
    "pigeonpeas", "pomegranate", "rice", "watermelon", "wheat"
]

# Generate audio for each crop
for crop in crop_names:
    text = crop.upper()  # Optional: Make it sound emphasized
    tts = gTTS(text=text, lang='en')
    filename = f"{crop.lower()}.mp3"
    filepath = os.path.join(audio_path, filename)
    tts.save(filepath)
    print(f"Saved: {filepath}")
