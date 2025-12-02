# utils.py
import numpy as np
from skimage.segmentation import slic
from skimage.color import rgb2gray
from skimage import img_as_float
import cv2

def compute_superpixels(img_rgb, n_segments=2000, compactness=10):
    """
    img_rgb: HxWx3 uint8
    returns: labels (HxW) with superpixel IDs
    """
    img = img_as_float(img_rgb)  # skimage expects float in [0,1]
    labels = slic(img, n_segments=n_segments, compactness=compactness, start_label=0)
    return labels

def extract_features_for_labels(img_rgb, labels):
    """
    img_rgb: HxWx3 uint8
    labels: HxW int
    returns:
      features: [num_superpixels x F] numpy array
      ids: [num_superpixels] list of label ids (0..)
    Basic features:
      - mean R,G,B
      - std R,G,B
      - area (#pixels)
      - mean grayscale
    """
    h, w = labels.shape
    img = img_rgb.astype(np.float32)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)

    max_label = labels.max()
    num = max_label + 1

    # Preallocate
    sums = np.zeros((num, 3), dtype=np.float64)
    sums_sq = np.zeros((num, 3), dtype=np.float64)
    gray_sums = np.zeros((num,), dtype=np.float64)
    counts = np.zeros((num,), dtype=np.int64)

    # Flattened iteration faster
    flat_img = img.reshape(-1, 3)
    flat_gray = gray.reshape(-1)
    flat_labels = labels.reshape(-1)

    for i in range(flat_labels.shape[0]):
        l = flat_labels[i]
        counts[l] += 1
        pix = flat_img[i]
        sums[l] += pix
        sums_sq[l] += pix * pix
        gray_sums[l] += flat_gray[i]

    # Compute features
    mean_rgb = sums / counts[:, None]
    var_rgb = (sums_sq / counts[:, None]) - mean_rgb * mean_rgb
    std_rgb = np.sqrt(np.clip(var_rgb, a_min=0, a_max=None))
    mean_gray = gray_sums / counts

    area = counts.astype(np.float32)  # could normalize later

    # Stack features
    features = np.hstack([mean_rgb, std_rgb, mean_gray.reshape(-1, 1), area.reshape(-1, 1)])
    ids = np.arange(num)

    return features, ids

def labels_to_mask(pred_labels, superpixel_labels):
    """
    pred_labels: array where index = superpixel id -> predicted class label (0,1,2)
    superpixel_labels: HxW map
    returns: HxW mask with predicted label per pixel
    """
    out = pred_labels[superpixel_labels]
    return out.astype(np.uint8)
