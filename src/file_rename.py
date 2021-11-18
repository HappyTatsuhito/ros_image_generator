#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import sys
import cv2
import random
import numpy as np

reference_path = "/home/mimi/rcap/dataset/"
destination_path = "/home/mimi/rcap/summary_dataset/"

def createDataset():
    count = 0
    for dir_name in os.listdir(reference_path):
        for file_name in os.listdir(reference_path+dir_name):
            if file_name.split('.')[1] == 'txt': continue
            txt_file = file_name.split('.')[0]+'.txt'
            os.system("cp " + reference_path+dir_name+'/'+file_name + " " + destination_path + "image_" + str(count) + ".png")
            os.system("cp " + reference_path+dir_name+'/'+txt_file + " " + destination_path + "image_" + str(count) + ".txt")
            count += 1


if __name__ == '__main__':
    createDataset()
