from pathlib import Path
import json
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory
import tensorflow as tf

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
MODEL_PATH = ROOT / "plant_disease_model.keras"
CLASSES_PATH = ROOT / "class_names.json"

app = Flask(__name__)

# Load once per serverless instance.
model = tf.keras.models.load_model(MODEL_PATH)
with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

IMG_SIZE = (224, 224)

def predict_image(image):
    image = image.convert("RGB").resize(IMG_SIZE)
    arr = np.asarray(image, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)

    probs = model.predict(arr, verbose=0)[0]
    top_idx = np.argsort(probs)[::-1][:5]

    predictions = [
        {
            "class": class_names[int(i)],
            "confidence": round(float(probs[i]) * 100, 2)
        }
        for i in top_idx
    ]

    best = predictions[0]
    return {
        "prediction": best["class"],
        "confidence": best["confidence"],
        "top_predictions": predictions
    }

@app.get("/")
def home():
    return send_from_directory(PUBLIC, "index.html")

@app.get("/<path:filename>")
def frontend_files(filename):
    # Keep API routes separate from frontend assets.
    if filename.startswith("api/"):
        return jsonify({"error": "Not found"}), 404
    file_path = PUBLIC / filename
    if file_path.is_file():
        return send_from_directory(PUBLIC, filename)
    return send_from_directory(PUBLIC, "index.html")

@app.post("/predict")
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No image file uploaded."}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Please select an image."}), 400

    try:
        image = Image.open(file.stream)
        result = predict_image(image)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

# Vercel discovers the Flask app object above.
