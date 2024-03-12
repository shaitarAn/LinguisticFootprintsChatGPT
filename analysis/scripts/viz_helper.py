import os

def collect_special_pngs(path):
    pngs = []
    # check if path is a directory
    if os.path.isdir(path):    
        for png in os.listdir(path):
            print(png)
            if png.endswith(".png"):
                pngs.append(f"{path}{png}")

    return pngs