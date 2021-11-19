#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import sys
import cv2
import random
import numpy as np

ref_path = '/home/mimi/rcap/annotation/'
dest_path= '/home/mimi/rcap/annotation_file/'

def EditAnnotation():
    for dir_name in os.listdir(ref_path):
        dir_num = dir_name.split('_')[-1]
        print dir_num

        for file_name in os.listdir(ref_path+dir_name):
            if file_name.split('_')[0]!='image': continue

            annotation = open(ref_path+dir_name+os.sep+file_name, 'r')
            lines = annotation.readlines()

            new_anno = open(dest_path+dir_num+os.sep+file_name, 'w')
            for line in lines:
                print line
                new_line = '0'
                for i, txt in enumerate(line.split(' ')):
                    if i==0: continue
                    new_line += (' '+txt)
                print new_line
                new_anno.writelines(new_line)

            annotation.close()
            new_anno.close()


if __name__ == '__main__':
    EditAnnotation()
