from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

def image_colorfulness(image):
    
    # load the image, resize it (to speed up computation), and
    # compute the colorfulness metric for the image
    image = cv2.imread(image)
    image = imutils.resize(image, width=250)
    
    # split the image into its respective RGB components
    (B, G, R) = cv2.split(image.astype("float"))
    # compute rg = R - G
    rg = np.absolute(R - G)
    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)
    # compute the mean and standard deviation of both `rg` and `yb`
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))
    # combine the mean and standard deviations
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    # derive the "colorfulness" metric and return it
    res = stdRoot + (0.3 * meanRoot)
    res = float(res)
    res = str(res)
    return res