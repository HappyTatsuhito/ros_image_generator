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
        rospy.Subscriber("/zed2/zed_node/left_raw/image_raw_color", Image, self.imageCB)
        rospy.Subscriber("/zed2/zed_node/depth/depth_registered", Image, self.depthImageCB)
        self.ros_image = Image()
        self.ros_depth_image = Image()
        self.count = count

    def imageCB(self,image):
        self.ros_image = image

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
            # RGB Image
            color_image = bridge.imgmsg_to_cv2(self.ros_image, desired_encoding="bgr8")
            color_image_path = SAVE_PATH + COLOR_PATH
            self.viewImage(color_image)
            cv2.imwrite(color_image_path + "color_image_" + str(self.count) + ".png", color_image)

            # Depth Image
            depth_image = bridge.imgmsg_to_cv2(self.ros_depth_image, desired_encoding="passthrough")
            depth_image_path = SAVE_PATH + DEPTH_PATH
            depth_image = np.nan_to_num(depth_image)
            print depth_image[430][770]
            depth_image *= 100
            depth_image = depth_image.astype(np.uint8)
            print depth_image[430][770]
            print np.amax(depth_image)
            print np.amin(depth_image)
            '''
            for i in range(180, 530):
                print depth_image[i][600:800]
            '''
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
    while not rospy.is_shutdown():
        image_generator.convert_image()
    cv2.destroyAllWindows()
