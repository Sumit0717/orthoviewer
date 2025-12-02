import rasterio
from PIL import Image
import numpy as np

# Path to your TIFF
path = "/Users/ajayyy/Desktop/DRONE-PROJECT/orthom_classifer/data/692cdf6c21834247599259d4.tif"

# Read the TIFF safely using rasterio
with rasterio.open(path) as src:
    print("Bands:", src.count)
    print("Width:", src.width)
    print("Height:", src.height)

    # Read first 3 bands (usually RGB)
    img = src.read([1, 2, 3]).transpose(1, 2, 0)

# Normalize if needed (multi-bit depths)
if img.dtype != np.uint8:
    img = (img / img.max() * 255).astype(np.uint8)

# Save as PNG
out_path = "/Users/ajayyy/Desktop/DRONE-PROJECT/orthom_classifer/data/ortho_rgb.png"
Image.fromarray(img).save(out_path)

print("Saved:", out_path)