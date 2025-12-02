from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from joblib import load
from utils import compute_superpixels, extract_features_for_labels, labels_to_mask

app = Flask(__name__)
CORS(app)

# Folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load model
MODEL_PATH = "model_rf.joblib"
model = None
if os.path.exists(MODEL_PATH):
    model = load(MODEL_PATH)
else:
    print("Warning: No model found. Run training first.")


@app.route("/")
def home():
    return jsonify({"status": "Backend running", "message": "Flask server is alive"})


# ---------------------------
# 1. IMAGE UPLOAD ROUTE
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return jsonify({
        "message": "File uploaded!",
        "filename": file.filename,
        "filepath": filepath
    })


# ---------------------------
# 2. PROCESS / CLASSIFY ROUTE
# ---------------------------
@app.route("/classify", methods=["POST"])
def classify():
    if not model:
        return jsonify({"error": "Model not loaded. Train or place model_rf.joblib first."}), 500

    if "filename" not in request.json:
        return jsonify({"error": "No filename provided"}), 400

    filename = request.json["filename"]
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found on server"}), 404

    # Load image
    img = Image.open(filepath).convert("RGB")
    img_np = np.array(img)

    # Compute superpixels
    sp_labels = compute_superpixels(img_np, n_segments=1500, compactness=10)

    # Extract features
    feats, ids = extract_features_for_labels(img_np, sp_labels)

    # Predict class per-superpixel
    predictions = model.predict(feats)

    # Construct pixel-wise mask
    pixel_mask = labels_to_mask(predictions, sp_labels)

    # Color overlay
    color_map = {
        0: (0, 255, 0),      # GREEN = good
        1: (255, 0, 0),      # RED
        2: (255, 255, 0)     # YELLOW
    }

    overlay = np.zeros_like(img_np)
    for cls, col in color_map.items():
        overlay[pixel_mask == cls] = col

    out = (0.55 * img_np + 0.45 * overlay).astype(np.uint8)

    # Save result
    out_name = "classified_" + filename
    out_path = os.path.join(OUTPUT_FOLDER, out_name)
    Image.fromarray(out).save(out_path)

    return jsonify({
        "message": "Classification complete",
        "output_image": out_name,
        "output_url": f"/outputs/{out_name}"
    })


# ---------------------------
# 3. SERVE FILES
# ---------------------------
@app.route("/uploads/<path:filename>")
def serve_uploaded(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/outputs/<path:filename>")
def serve_outputs(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
