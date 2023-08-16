#! /usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge
import cv2

class Lkas():
    def __init__(self):
        self.pub = rospy.Publisher('/modified_compressed_image',Image,queue_size=10)
        self.sub = rospy.Subscriber('/image_jpeg/compressed', CompressedImage, self.imgCB)
        self.bridge = CvBridge()

    def imgCB(self,data):
        img = self.bridge.compressed_imgmsg_to_cv2(data)
        
        (rows,cols,channels) = img.shape
        if cols > 320 and rows > 320 :
            #cv2.circle(img,(cols/2,rows/2),10,90,10)
            cv2.rectangle(img,((cols/2)-10, (rows/2)-10), ((cols/2) + 10,(rows/2)+10),(0,255,0),5)
        modi_img = self.bridge.cv2_to_imgmsg(img,'bgr8')

        self.pub.publish(modi_img)
        #cv2.imshow('Image Window',modi_img)
        #cv2.waitKey(1)




def main():
    rospy.init_node('lkas_node',anonymous=True)
    lk = Lkas()
    rospy.spin()


if __name__ == '__main__':
    main()