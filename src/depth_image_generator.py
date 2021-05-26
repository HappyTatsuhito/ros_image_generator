#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np

###
SAVE_PATH = "/home/demulab/makino/invisible_marker_data"
COLOR_PATH = "/rgb_imgs/"
DEPTH_PATH = "/depth_imgs/"
###

class ImageGenerator(object):
    def __init__(self, count=0):
        rospy.Subscriber("/zed2/zed_node/depth/depth_registered", Image, self.depthImageCB)
        self.ros_image = Image()
        self.ros_depth_image = Image()
        self.count = count

    def depthImageCB(self,image):
        self.ros_depth_image = image
        
    def viewImage(self,image):
        cv2.namedWindow("Show Image")
        cv2.imshow("Show Image", image)
        input_key = cv2.waitKey(0)

    def convert_image(self):
        bridge = CvBridge()
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            # Depth Image
            depth_image = bridge.imgmsg_to_cv2(self.ros_depth_image, desired_encoding="passthrough")
            depth_image_path = SAVE_PATH + DEPTH_PATH

            depth_image = np.nan_to_num(depth_image)
            depth_image *= 100 

            cv2.imwrite(depth_image_path + "depth_image_" + str(self.count) + ".png", depth_image)
            self.viewImage(depth_image)

            self.count += 1

        except CvBridgeError, e:
            pass
            #print e
            #Convert the depth image to a Numpy array


if __name__ == '__main__':
    args = sys.argv
    count = args[-1]

    rospy.init_node('ImageGenerator')

    image_generator = ImageGenerator(int(count))
    test_image = np.full((720, 1280), 0)
    test_image = test_image.astype(np.uint8)
    image_generator.viewImage(test_image)
    while not rospy.is_shutdown():
        image_generator.convert_image()
    cv2.destroyAllWindows()
