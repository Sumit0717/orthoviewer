'''tile creation'''
# from PIL import Image, ImageFile
# import os

# # allow huge images
# Image.MAX_IMAGE_PIXELS = None
# ImageFile.LOAD_TRUNCATED_IMAGES = True

# img = Image.open("data/ortho_rgb.png")
# tile_size = 1024

# w, h = img.size
# os.makedirs("data/tiles", exist_ok=True)

# count = 0
# for i in range(0, w, tile_size):
#     for j in range(0, h, tile_size):
#         box = (i, j, i + tile_size, j + tile_size)
#         tile = img.crop(box)
#         tile.save(f"data/tiles/tile_{i}_{j}.png")
#         count += 1

# print("Tiles created:", count)

'''read images'''
import cv2
import numpy as np
import os

tiles = os.listdir("data/tiles")

for t in tiles:
    path = f"data/tiles/{t}"
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue
    mean_val = img.mean()

    if mean_val < 5:  # almost black
        print("BLANK:", t)



# from PIL import Image

# # allow large images
# Image.MAX_IMAGE_PIXELS = None

# path = "data/ortho_rgb.png"

# img = Image.open(path)
# print("File:", path)
# print("Format:", img.format)
# print("Mode:", img.mode)
# print("Width:", img.width)
# print("Height:", img.height)
# print("Size:", img.size)
