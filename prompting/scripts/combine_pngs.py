# collect pngs from a directory and put them into one pdf file

import os
import sys
from PIL import Image
import glob
from pathlib import Path

# get the path to the directory with png files
png_directory = sys.argv[1]

# convert png_directory into a Path object
png_directory = Path(png_directory)

# get the name of the top directory
top_directory = png_directory.parts[-1]


if not os.path.exists("../plots/combined_results"):
    os.makedirs("../plots/combined_results")

# get the path to the directory where the pdf file will be saved
output_dir = "../plots/combined_results"

list_of_images = []

for png in png_directory.glob("*.png"):

    im = Image.open(png)
    list_of_images.append(im)

w = max(im.width for im in list_of_images)
h = max(im.height for im in list_of_images)

print(w)
print(h)

# create big empty image with place for images
new_image = Image.new('RGB', (w*2, h*3))


new_image.paste(list_of_images[0], (0, 0))
new_image.paste(list_of_images[1], (w, 0))
new_image.paste(list_of_images[2], (0, h))
new_image.paste(list_of_images[3], (w, h))
new_image.paste(list_of_images[4], (0, h*2))
new_image.paste(list_of_images[5], (w, h*2))
# new_image.paste(list_of_images[5], (0, h))

# save it
new_image.save(f'{output_dir}/{top_directory}.png')





