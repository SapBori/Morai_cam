#! /usr/bin/env python

import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage, Image
import cv2
import numpy as np

class Lkas():
    def __init__(self):
        self.pub1 = rospy.Publisher('/modified_compressed_image',Image,queue_size=10)
        self.pub2 = rospy.Publisher('/warp_image',Image,queue_size=10)
        self.sub = rospy.Subscriber('/image_jpeg/compressed', CompressedImage, self.imgCB)
        self.bridge = CvBridge()
    
    def img_wrap(self,img):
        self.img_x,self.img_y = img.shape[1], img.shape[0]

        src_center_offset = [200,315]
        src = np.float32(
            [
                [0,479],
                [src_center_offset[0], src_center_offset[1]],
                [640-src_center_offset[0],src_center_offset[1]],
                [639,479]
            ]
        )
        cv2.circle(img,(0,479),10,255,5)
        cv2.circle(img,(src_center_offset[0], src_center_offset[1]),10,255,5)
        cv2.circle(img,(640-src_center_offset[0],src_center_offset[1]),10,255,5)
        cv2.circle(img,(639,479),10,255,5)


        dst_offset = [(round(self.img_x * 0.125)), 0]
        dst = np.float32(
            [
                [dst_offset[0],self.img_y],
                [dst_offset[0],0],
                [self.img_x - dst_offset[0],0],
                [self.img_x - dst_offset[0],self.img_y],
            ]
        )
        cv2.circle(img,(int(dst_offset[0]),int(self.img_y)), 10, (0,0,255), 5)
        cv2.circle(img,(int(dst_offset[0]),0),10,(0,0,255),5)
        cv2.circle(img,(int(self.img_x - dst_offset[0]),0),10,(0,0,255),5)
        cv2.circle(img,(int(self.img_x - dst_offset[0]),int(self.img_y)),10,(0,0,255),5)

        matrix = cv2.getPerspectiveTransform(src, dst)
        warp_img = cv2.warpPerspective(img, matrix, (self.img_x, self.img_y))
        return img, warp_img

    def imgCB(self,data):
        img = self.bridge.compressed_imgmsg_to_cv2(data)
        modi_img, warp_img = self.img_wrap(img)

        modi_img_msg = self.bridge.cv2_to_imgmsg(img)
        warp_img_msg = self.bridge.cv2_to_imgmsg(warp_img)
        self.pub1.publish(modi_img_msg)
        self.pub2.publish(warp_img_msg)
        cv2.imshow('Normal', modi_img)
        cv2.imshow('Brid',warp_img)
        cv2.waitKey(1)



def main():
    rospy.init_node('lkas_node',anonymous=True)
    lk = Lkas()
    rospy.spin()


if __name__ == '__main__':
    main()