# 🛰️ Semi-Automated Labeling Tool for Orthomosaic Drone Images

A web-based application for efficient, scalable, and accurate annotation of drone-captured agricultural orthomosaics using superpixels, machine learning, and human refinement tools.

---

## 🎯 Project Objective

The objective of this web application is to provide a semi-automated labeling tool for orthomosaic drone images, enabling faster, more consistent, and more scalable creation of segmentation datasets for agricultural analysis.

Traditional pixel-by-pixel annotation of large orthomosaic images is slow and error-prone. This tool accelerates the process by:

- Automatically generating superpixels to break the image into meaningful regions
- Extracting features for each region
- Suggesting initial class labels using a machine learning model
- Allowing the user to visually review, correct, and export the final mask

This creates an efficient human-in-the-loop labeling pipeline, where the model handles the tedious work and the human ensures accuracy.

---

## ✨ Key Features

### Image Handling
- Upload large orthomosaic drone images
- Preview and inspect images

### Automated Assistance
- Superpixel segmentation
- Feature extraction
- ML-based preliminary label prediction
- Automatic color-coded mask generation

### Manual Correction Tools
- Brush tool for editing
- Region selection
- Class picker
- Mask refinement tools

### Export Options
- Export refined masks
- Export annotation dataset
- Export superpixel metadata

---

## 🔧 High-Level Architecture

### Frontend (React)
- Image upload interface
- Mask visualization and editing
- Human-in-the-loop correction tools
- Export functionality

### Backend (Flask)
- Image upload handling
- Superpixel computation
- Feature extraction
- ML model inference
- Mask generation
- Serving output masks to frontend

### Machine Learning Pipeline
- Superpixel segmentation (SLIC)
- Feature engineering (color, variance, optional NDVI)
- Texture features (optional GLCM)
- RandomForest classifier
- Training script for generating `.joblib` model file

---

## 📁 Project Structure
```
project/
│
├── backend/
│ ├── app.py
│ ├── uploads/
│ ├── outputs/
│ └── models/
│ └── model_rf.joblib
│
├── frontend/
│ ├── src/
│ ├── public/
│ └── package.json
│
├── images/ # Training images
├── masks/ # Ground truth masks
└── train.py # Model training pipeline
```

---

