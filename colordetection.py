import numpy as np
import cv2
def resize(img):
	img=cv2.resize(img,(500,300))
	return img
def func(a):
	pass
	return
img=cv2.imread('pic.jpg')
img=resize(img)
cv2.imshow('Original',img)
cv2.namedWindow('Trackbar')
cv2.resizeWindow('Trackbar',(800,400))
cv2.createTrackbar('Hue_min','Trackbar',0,179,func)
cv2.createTrackbar('Hue_max','Trackbar',179,179,func)
cv2.createTrackbar('Sat_min','Trackbar',0,255,func)
cv2.createTrackbar('Sat_max','Trackbar',255,255,func)
cv2.createTrackbar('Val_min','Trackbar',0,255,func)
cv2.createTrackbar('Val_max','Trackbar',255,255,func)
while True:
	imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	hmin=cv2.getTrackbarPos('Hue_min','Trackbar')
	hmax=cv2.getTrackbarPos('Hue_max','Trackbar')
	smin=cv2.getTrackbarPos('Sat_min','Trackbar')
	smax=cv2.getTrackbarPos('Sat_max','Trackbar')
	vmin=cv2.getTrackbarPos('Val_min','Trackbar')
	vmax=cv2.getTrackbarPos('Val_max','Trackbar')
	#print(hmin,hmax,smin,smax,vmin,vmax)
	lower=np.array([hmin,smin,vmin])
	upper=np.array([hmax,smax,vmax])
	mask=cv2.inRange(imgHSV,lower,upper)
	result=cv2.bitwise_and(img,img,mask=mask)
	cont,hier=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(mask,cont,-1,(0,255,0),3)
	#print(cont)
	cv2.imshow('HSV',imgHSV)
	cv2.imshow('HSV range',mask)
	cv2.imshow('Result',result)
	if cv2.waitKey(1) & 0xFF==ord('q'):
		cv2.destroyAllWindows()
		break
