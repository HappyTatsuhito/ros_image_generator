#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import cv2
import time
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np

SAVE_PATH = "~/rcap/dataset/"

class ImageGenerator(object):
    def __init__(self):
        rospy.Subscriber("/camera/color/image_raw", Image, self.imageCB)
        self.ros_image = Image()
        self.count = 0

    def imageCB(self,image):
        self.ros_image = image
        self.update_time = time.time()

    def viewImage(self,image):
        cv2.namedWindow("Show Image")
        cv2.imshow("Show Image", image)
        input_key = cv2.waitKey(0)

    def convert_image(self):
        if time.time()-self.update_time > 3.0: return
        bridge = CvBridge()

        try:
            image = bridge.imgmsg_to_cv2(self.ros_image, desired_encoding="bgr8")
            cv2.imwrite(SAVE_PATH + "image_" + str(self.count) + ".png", image)
            #self.viewImage(image)
            self.count += 1
        except CvBridgeError, e:
            pass


if __name__ == '__main__':
    rospy.init_node('ImageGenerator')
    image_generator = ImageGenerator()

    while not rospy.is_shutdown():
        image_generator.convert_image()
        print('ok')
        rospy.Rate(1/3.0).sleep()
    cv2.destroyAllWindows()
