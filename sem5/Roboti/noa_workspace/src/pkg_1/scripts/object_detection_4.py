#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image

ROS_NODE_NAME ="image_processing_node"

#Define color range for detection
COLOR_LOWER = np.array([0, 0, 135]) #lower bound
COLOR_UPPER = np.array([255, 110, 255]) #upper bound

def img_process(img):
	#rospy.loginfo("Processing image with width: %s and height: %s" % (img.width, img.height))
	frame = np.ndarray(shape=(img.height, img.width, 3), dtype=np.uint8, buffer=img.data)
	frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
	poza = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
	mask = cv2.inRange(poza, COLOR_LOWER, COLOR_UPPER)
	contours, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cv2.imshow("Processed mask", mask)
	if contours:
            
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 100:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 255), 2)
	cv2.imshow("Processed frame", frame)
	cv2.waitKey(1)

def cleanup():
	rospy.loginfo("Shutting down...")
	cv2.destroyAllWindows()

if __name__ == "__main__":
	rospy.init_node(ROS_NODE_NAME, log_level = rospy.INFO)
	rospy.on_shutdown(cleanup)
	rospy.Subscriber("/usb_cam/image_raw", Image, img_process)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		pass