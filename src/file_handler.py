#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import sys
import cv2
import json
import random
import numpy as np
sys.path.insert(0, "/usr/local/lib/python3.6/dist-packages/")
from labelme.utils import shape as label_shape

#reference_path = "/home/tatsuhito/pd3/dataset/new_data/"
reference_path = "/home/tatsuhito/pd3/segmentation_data/dataset/store/"
current_path = "/home/tatsuhito/pd3/dataset/unknown_object-unknown/spare_color_images/"
#destination_path = "/home/tatsuhito/pd3/dataset/unknown_object-unknown/"
destination_path = "/home/tatsuhito/pd3/segmentation_data/dataset/store/"
    
def alikeFileGenerator():
    for file_name in os.listdir(reference_path):
        name_list = file_name.split("_")
        file_number = name_list[-1].split(".")
        file_number = file_number[0]
        os.system("mv " + current_path + "color_image_" + file_number + ".png " + destination_path)
        
    print "finish"


def generateJson():
    for file_name in os.listdir(reference_path):
        name_list = file_name.split("_")
        file_extension = name_list[-1].split(".")[1]
        
        if file_extension == "png":
            continue
        
        reference_file_path = reference_path + file_name
        with open(reference_file_path) as f:
            data_lines = f.read()

        # 文字列置換
        data_lines = data_lines.replace("color", "depth")

        # 保存
        file_number = name_list[-1].split(".")[0]
        new_name = "depth_image_" + file_number + ".json"
        destination_file_path = destination_path + new_name
        with open(destination_file_path, mode="w") as f:
            f.write(data_lines)

            
def generateMask():
    for file_name in os.listdir(reference_path):
        name_list = file_name.split("_")
        file_extension = name_list[-1].split(".")[1]
        
        if file_extension == "png":
            continue
        
        reference_file_path = reference_path + file_name
        with open(reference_file_path) as f:
            dj = json.load(f)

        mask_num = len(dj['shapes'])

        mask_0 = np.zeros((480, 640))
        mask_1 = np.zeros((480, 640))
        mask_2 = np.zeros((480, 640))

        if mask_num >= 1:
            mask_0 = label_shape.shape_to_mask((dj['imageHeight'],dj['imageWidth']), dj['shapes'][0]['points'], shape_type=None,line_width=1, point_size=1)
        if mask_num >= 2:
            mask_1 = label_shape.shape_to_mask((dj['imageHeight'],dj['imageWidth']), dj['shapes'][1]['points'], shape_type=None,line_width=1, point_size=1)
        if mask_num >= 3:
            mask_2 = label_shape.shape_to_mask((dj['imageHeight'],dj['imageWidth']), dj['shapes'][2]['points'], shape_type=None,line_width=1, point_size=1)

        #booleanを0,1に変換
        if mask_num >= 1:
            mask_0_img = mask_0.astype(np.int)
            #mask_0_img *= 255
        if mask_num >= 2:
            mask_1_img = mask_1.astype(np.int)
            #mask_1_img *= 255
        if mask_num >= 3:
            mask_2_img = mask_2.astype(np.int)
            #mask_2_img *= 255
            
        if mask_num >= 1:
            composited_mask_img = mask_0_img
        if mask_num >= 2:
            composited_mask_img = cv2.bitwise_or(mask_0_img, mask_1_img)
        if mask_num >= 3:
            composited_mask_img = cv2.bitwise_or(composited_mask_img, mask_2_img)

        # 保存
        file_number = name_list[-1].split(".")[0]
        new_name = "depth_image_" + file_number + ".png"
        destination_file_path = destination_path + new_name
        cv2.imwrite(destination_file_path, composited_mask_img)
        # 確認用画像の保存
        visual_mask_img = composited_mask_img * 255
        visual_file_path = "/home/tatsuhito/pd3/visual_img/"
        visual_image_path = visual_file_path + new_name
        cv2.imwrite(visual_image_path, visual_mask_img)
        

def createDataset():
    count = 0
    for file_name in os.listdir(reference_path + "depth_images/"):
        name_list = file_name.split("_")
        file_extension = name_list[-1].split(".")[1]
        
        if file_extension == "json":
            continue

        left_image_path = destination_path + "left_store/"
        groundTruth_image_path = destination_path + "groundTruth_store/"
        os.system("cp " + reference_path + "depth_images/" + file_name + " " + left_image_path + "left_image_" + str(count) + ".png")
        os.system("cp " + reference_path + "mask_images/" + file_name + " " + groundTruth_image_path + "left_groundTruth_" + str(count) + ".png")
        count += 1

def shuffleDataset():
    file_list = os.listdir(reference_path + "left_store/")
    shuffled_list = random.sample(file_list, len(file_list))

    count = 0
    for file_name in shuffled_list:
        # left_image
        os.system("cp " + reference_path + "left_store/" + file_name + " " + destination_path + "left_images/left_image_" + str(count) + ".png")
        
        # left_groundTruth
        file_number = file_name.split("_")[-1].split(".")[0]
        ground_file_name = "left_groundTruth_" + file_number + ".png"
        os.system("cp " + reference_path + "groundTruth_store/" + ground_file_name + " " + destination_path + "left_groundTruth/left_groundTruth_" + str(count) + ".png")
        count += 1
        


if __name__ == '__main__':
    #alikeFileGenerator()
    #generateJson()
    #generateMask()
    #createDataset()
    #shuffleDataset()
    print "ok"
    
