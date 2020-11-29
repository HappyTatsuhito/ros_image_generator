#!/usr/bin/env python
# -*- coding: utf-8 -*

import os

def main():
    reference_path = "/home/tatsuhito/pd3/cup_noodle-tea/spare_depth_images/"
    current_path = "/home/tatsuhito/pd3/cup_noodle-tea/color_images/"
    destination_path = "/home/tatsuhito/pd3/cup_noodle-tea/spare_color_images/"
    for file_name in os.listdir(reference_path):
        name_list = file_name.split("_")
        file_number = name_list[2].split(".")
        file_number = file_number[0]
        os.system("mv " + current_path + "color_image_" + file_number + ".png " + destination_path)
        
    print "finish"


if __name__ == '__main__':
    main()
