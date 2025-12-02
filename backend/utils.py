import numpy as np
from skimage.segmentation import slic
from skimage.color import rgb2gray
from skimage.measure import regionprops
from skimage.util import img_as_float

def compute_superpixels(img, n_segments=1000, compactness=10):
    img_f = img_as_float(img)
    segments = slic(
        img_f,
        n_segments=n_segments,
        compactness=compactness,
        start_label=0
    )
    return segments

def superpixel_features(img, segments):
    img_f = img_as_float(img)
    n = segments.max() + 1
    feats = []

    gray = rgb2gray(img_f)

    for sp_id in range(n):
        mask = segments == sp_id
        pixels = img_f[mask]

        if pixels.size == 0:
            feats.append([0] * 11)
            continue

        mean_rgb = pixels.mean(axis=0)
        std_rgb = pixels.std(axis=0)
        area = mask.sum()

        h, _ = np.histogram(gray[mask], bins=4, range=(0, 1), density=True)

        feat = np.concatenate([mean_rgb, std_rgb, [area], h])
        feats.append(feat)

    return np.array(feats)

def map_superpixel_labels_to_image(segments, sp_labels):
    h, w = segments.shape
    out = np.zeros((h, w, 3), dtype=np.uint8)

    palette = {
        0: (34, 139, 34),
        1: (0, 0, 255),
        2: (255, 255, 0)
    }

    for sp_id, lbl in enumerate(sp_labels):
        color = palette.get(int(lbl), (255, 0, 255))
        out[segments == sp_id] = color

    return out
