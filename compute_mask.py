import os
import argparse
import cv2
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('--dataRoot', type=str,
                    default='')
parser.add_argument('--savePath', type=str, default='./mask/')
args = parser.parse_args()

gts_path = os.path.join(args.dataRoot, 'gts')
images_path = os.path.join(args.dataRoot, 'images') 

for filename in os.listdir(gts_path):
    print(filename)
    gt_file = os.path.join(gts_path, filename)
    image_file = os.path.join(images_path, filename)
    gt = cv2.imread(gt_file)
    im = cv2.imread(image_file)
    kernel = np.ones((3,3),np.uint8) 
    threshold = 25
    diff_image = np.abs(im.astype(np.float32) - gt.astype(np.float32))
    mean_image = np.mean(diff_image, axis=-1)
    mask = np.greater(mean_image, threshold).astype(np.uint8)
    mask = (1 - mask) * 255
    mask = cv2.erode(np.uint8(mask),  kernel, iterations=1)
    cv2.imwrite(os.path.join(args.savePath, filename), np.uint8(mask))