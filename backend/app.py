import os
from flask import Flask, request, render_template, send_from_directory
import cv2
import numpy as np
from joblib import load
from utils import compute_superpixels, superpixel_features, map_superpixel_labels_to_image

MODEL_PATH = "rf_model.pkl"
UPLOAD_FOLDER = "static/outputs"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = load(MODEL_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["image"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
    f.save(filepath)

    img = cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB)

    segments = compute_superpixels(img, n_segments=1200)
    feats = superpixel_features(img, segments)
    preds = model.predict(feats)

    out = map_superpixel_labels_to_image(segments, preds)
    out_bgr = cv2.cvtColor(out, cv2.COLOR_RGB2BGR)

    out_name = "classified_" + f.filename
    out_path = os.path.join(app.config["UPLOAD_FOLDER"], out_name)
    cv2.imwrite(out_path, out_bgr)

    return render_template(
        "index.html",
        input_image=f.filename,
        output_image=out_name
    )

@app.route("/static/outputs/<path:filename>")
def serve_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
