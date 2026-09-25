from pathlib import Path
import json
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
import tensorflow as tf

ROOT = Path(__file__).resolve().parent

app = Flask(__name__, template_folder="templates", static_folder="static")

MODEL_PATH = ROOT / "plant_disease_model.keras"
CLASSES_PATH = ROOT / "class_names.json"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

IMG_SIZE = (224, 224)

def predict_image(image):
    image = image.convert("RGB").resize(IMG_SIZE)
    arr = np.asarray(image, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)

    probabilities = model.predict(arr, verbose=0)[0]
    top_indices = np.argsort(probabilities)[::-1][:5]

    top_predictions = [
        {
            "class": class_names[int(i)],
            "confidence": round(float(probabilities[i]) * 100, 2)
        }
        for i in top_indices
    ]

    return {
        "prediction": top_predictions[0]["class"],
        "confidence": top_predictions[0]["confidence"],
        "top_predictions": top_predictions
    }

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No image file uploaded."}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Please select an image."}), 400

    try:
        image = Image.open(file.stream)
        return jsonify(predict_image(image))
    except Exception as exc:
        return jsonify({"error": f"Prediction failed: {exc}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
