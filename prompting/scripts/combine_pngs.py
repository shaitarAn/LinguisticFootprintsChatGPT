# collect pngs from a directory and put them into one pdf file

import os
import sys
from PIL import Image
import glob
from pathlib import Path

# convert png_directory into a Path object
png_directory = Path("../plots")

if not os.path.exists("../plots/combined_results"):
    os.makedirs("../plots/combined_results")

if not os.path.exists("../results/combined_results"):
    os.makedirs("../results/combined_results")

# get the path to the directory where the pdf file will be saved
output_dir = "../results/combined_results"

# iterate through the directories in the png_directory
for top_directory in os.listdir(png_directory):
    # print(top_directory)

    list_of_images = []
    # iterate through the png files in the top_directory
    for png in glob.glob(f"{png_directory}/{top_directory}/*.png"):
        # print(png)
        im = Image.open(png)
        list_of_images.append(im)

        w = max(im.width for im in list_of_images)
        h = max(im.height for im in list_of_images)

        # print(w)
        # print(h)

        if len(list_of_images) == 6:
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
        else:
            print(f"not enough images in {top_directory}")
            print(len(list_of_images))





