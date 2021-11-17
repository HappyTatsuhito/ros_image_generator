#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import cv2
import time
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

SAVE_PATH = "~/rcap/dataset/"

class ImageGenerator(object):
    def __init__(self, count=0):
        rospy.Subscriber("/camera/color/image_raw", Image, self.imageCB)
        self.ros_image = Image()
        self.update_time = 0
        self.dir_count = count
        self.img_count = 0

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
            cv2.imwrite(SAVE_PATH + str(self.dir_count) + "/image_" + str(self.img_count) + ".png", image)
            #self.viewImage(image)
            self.img_count += 1
        except CvBridgeError, e:
            pass


if __name__ == '__main__':
    args = sys.argv
    count = args[-1]

    rospy.init_node('ImageGenerator')

    image_generator = ImageGenerator(int(count))
    while not rospy.is_shutdown():
        image_generator.convert_image()
        rospy.Rate(1/3.0).sleep()
    cv2.destroyAllWindows()
