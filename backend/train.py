import argparse
import numpy as np
import cv2
from utils import compute_superpixels, superpixel_features
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

def label_superpixels_from_mask(segments, gt_mask):
    n = segments.max() + 1
    sp_labels = np.zeros(n, dtype=np.int32)

    for sp_id in range(n):
        mask = segments == sp_id
        values = gt_mask[mask]
        if len(values) == 0:
            sp_labels[sp_id] = 0
        else:
            vals, counts = np.unique(values, return_counts=True)
            sp_labels[sp_id] = vals[np.argmax(counts)]

    return sp_labels

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", required=True)
    parser.add_argument("--mask", required=True)
    parser.add_argument("--out", default="rf_model.pkl")
    parser.add_argument("--n_segments", type=int, default=1000)
    args = parser.parse_args()

    img = cv2.cvtColor(cv2.imread(args.img), cv2.COLOR_BGR2RGB)
    gt_mask = cv2.imread(args.mask, cv2.IMREAD_GRAYSCALE)

    segments = compute_superpixels(img, n_segments=args.n_segments)
    feats = superpixel_features(img, segments)
    sp_labels = label_superpixels_from_mask(segments, gt_mask)

    clf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    clf.fit(feats, sp_labels)

    dump(clf, args.out)
    print("Model saved to:", args.out)

if __name__ == "__main__":
    main()
