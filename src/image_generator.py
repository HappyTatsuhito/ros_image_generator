#!/usr/bin/env python
# -*- coding: utf-8 -*

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np

class ImageGenerator(object):
    def __init__(self):
        rospy.Subscriber("/camera/color/image_raw", Image, self.imageCB)
        rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, self.depthImageCB)
        self.ros_image = Image()
        self.ros_depth_image = Image()
        self.count = 258

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
            color_image = bridge.imgmsg_to_cv2(self.ros_image, desired_encoding="bgr8")
            #Convert the depth image using the default passthrough encoding
            depth_array = bridge.imgmsg_to_cv2(self.ros_depth_image, desired_encoding="passthrough")
            depth_image = np.array(depth_array, dtype=np.float32)
            depth_image = depth_image/1500.0*255
            cv2.imwrite("/home/tatsuhito/pd3/bikkle-milk_tea/temporary_color_images/color_image_1_" + str(self.count) + ".png", color_image)
            cv2.imwrite("/home/tatsuhito/pd3/bikkle-milk_tea/temporary_depth_images/depth_image_1_" + str(self.count) + ".png", depth_image)
            self.viewImage(depth_image/255)
            self.count += 1
        except CvBridgeError, e:
            pass
            #print e
            #Convert the depth image to a Numpy array


if __name__ == '__main__':
    rospy.init_node('ImageGenerator')
    image_generator = ImageGenerator()
    while not rospy.is_shutdown():
        image_generator.convert_image()
    cv2.destroyAllWindows()
