#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import sys
import cv2
import json
import random
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image

sys.path.insert(0, "/usr/local/lib/python3.6/dist-packages/")
from labelme.utils import shape as label_shape


class PixelDisplay(object):
    def __init__(self):
        rospy.Subscriber("/zed2/zed_node/depth/depth_registered", Image, self.imageCB)
        self.ros_image = Image()
        self.gray_image = Image()

    def imageCB(self, image):
        self.ros_image = image

    def onMouse(self, event, x, y, flags, params):
        '''
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)
        '''
        print self.gray_image[y][x]

    def viewImage(self, image):
        cv2.namedWindow("Show Image")
        cv2.imshow("Show Image", image)
        cv2.setMouseCallback('Show Image', self.onMouse)
        input_key = cv2.waitKey(0)

    def convert_image(self):
        bridge = CvBridge()
        try:
            self.gray_image = bridge.imgmsg_to_cv2(self.ros_image, desired_encoding="passthrough")
            self.viewImage(self.gray_image)
        except CvBridgeError, e:
            pass



if __name__ == '__main__':
    rospy.init_node('pixel_display')

    pixel_display = PixelDisplay()
    while not rospy.is_shutdown():
        pixel_display.convert_image()
    cv2.destroyAllWindows()
