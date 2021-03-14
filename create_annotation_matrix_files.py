import glob
import os
import sys

import natsort
import numpy as np
from scipy.io import savemat
from scipy.ndimage import label, zoom
from skimage.io import imread


path = sys.argv[1]
output_path = sys.argv[2]
downsample_factor = 3
factor = 2 ** (downsample_factor - 1)
image_paths = natsort.natsorted(
    glob.glob(os.path.join(path, "*.jpg")))

for path in image_paths:
    img = imread(path)
    ann_type = zoom(img, factor, order=0)
    binary_image = np.zeros_like(ann_type)
    binary_image[ann_type != 0] = 1
    ann_inst, num_cells = label(binary_image)
    mdict = {"inst_map": ann_inst, "type_map": ann_type}
    savemat(
        os.path.join(
            output_path, os.path.basename(path).split(".")[0] + ".mat"),
        mdict)