#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import cv2
import numpy as np

def viewImage(image):
    cv2.namedWindow("Show Image")
    cv2.imshow("Show Image", image)
    input_key = cv2.waitKey(0)

if __name__ == '__main__':
    image_path = "/home/demulab/makino/invisible_marker_data/depth_imgs/"

    image = cv2.imread(image_path+"depth_image_100.png", cv2.IMREAD_GRAYSCALE)
    print image.shape
    print np.amax(image)
    print np.amin(image)
    viewImage(image)

    image = cv2.imread(image_path+"depth_image_101.png", cv2.IMREAD_GRAYSCALE)
    print image.shape
    print image.dtype
    print np.amax(image)
    print np.amin(image)
    viewImage(image)
