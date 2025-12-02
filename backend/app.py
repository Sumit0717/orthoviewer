from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return jsonify({
        "message": "File uploaded!",
        "filename": file.filename
    })

@app.route("/uploads/<path:filename>")
def serve_uploaded(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
@app.route("/")
def home():
    return jsonify({"status": "Backend running", "message": "Flask server is alive"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)



# import os
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import cv2
# import numpy as np
# from joblib import load
# from utils import compute_superpixels, superpixel_features, map_superpixel_labels_to_image

# MODEL_PATH = "rf_model.pkl"
# UPLOAD_FOLDER = "static/outputs"

# app = Flask(__name__)
# CORS(app)  # allow React to talk to backend

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# model = load(MODEL_PATH)

# @app.route("/upload", methods=["POST"])
# def upload():
#     if "image" not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     f = request.files["image"]
#     filepath = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
#     f.save(filepath)

#     # Load + process image
#     img = cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB)

#     segments = compute_superpixels(img, n_segments=1200)
#     feats = superpixel_features(img, segments)
#     preds = model.predict(feats)

#     # Map results to image
#     out = map_superpixel_labels_to_image(segments, preds)
#     out_bgr = cv2.cvtColor(out, cv2.COLOR_RGB2BGR)

#     out_name = "classified_" + f.filename
#     out_path = os.path.join(app.config["UPLOAD_FOLDER"], out_name)
#     cv2.imwrite(out_path, out_bgr)

#     return jsonify({
#         "output_image": out_name
#     })

# @app.route("/static/outputs/<path:filename>")
# def serve_output(filename):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
