#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import sys
import cv2
import random
import numpy as np

ref_path = '/home/mimi/rcap/annotation_file/'
img_path = '/home/mimi/rcap/dataset/'
dest_path = '/home/mimi/rcap/summary_dataset/'

def createDataset():
    for dir_name in os.listdir(ref_path):
        print dir_name
        for txt_name in os.listdir(ref_path+dir_name):
            img_name = txt_name.split('.')[0] + '.png'
            num = txt_name.split('.')[0].split('_')[1]
            os.system('cp ' + ref_path+dir_name+'/'+txt_name + ' ' + dest_path+'image_'+str(dir_name)+'_'+num+'.txt')
            os.system('cp ' + img_path+dir_name+'/'+img_name + ' ' + dest_path+'image_'+str(dir_name)+'_'+num+'.png')


if __name__ == '__main__':
    createDataset()
