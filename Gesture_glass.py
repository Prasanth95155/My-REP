import numpy as np
import cv2
from pynput.mouse import Button,Controller
import wx
import time
'''def resize(img):
    img=cv2.resize(img,(852,480))
    return img'''
def func(a):
    pass
    return
def distance(cx1,cy1,cx3,cy3):
    distance = pow( pow(cx3-cx1,2) + pow(cy3-cy1,2) , 0.5)
    return distance
'''cv2.namedWindow('Trackbar')
cv2.resizeWindow('Trackbar',(800,400))
cv2.createTrackbar('Hue_min','Trackbar',0,179,func)
cv2.createTrackbar('Hue_max','Trackbar',179,179,func)
cv2.createTrackbar('Sat_min','Trackbar',0,255,func)
cv2.createTrackbar('Sat_max','Trackbar',255,255,func)
cv2.createTrackbar('Val_min','Trackbar',0,255,func)
cv2.createTrackbar('Val_max','Trackbar',255,255,func)'''
def ret_mask(img_HSV,lower,upper,KernelOpen,KernelClose):
    mask = cv2.inRange(imgHSV,lower,upper)
    mask_open = cv2.morphologyEx(mask,cv2.MORPH_OPEN,KernelOpen)
    mask_close = cv2.morphologyEx(mask_open,cv2.MORPH_CLOSE,KernelClose)
    return mask_close
def calib():
    hmin=cv2.getTrackbarPos('Hue_min','Trackbar')
    hmax=cv2.getTrackbarPos('Hue_max','Trackbar')
    smin=cv2.getTrackbarPos('Sat_min','Trackbar')
    smax=cv2.getTrackbarPos('Sat_max','Trackbar')
    vmin=cv2.getTrackbarPos('Val_min','Trackbar')
    vmax=cv2.getTrackbarPos('Val_max','Trackbar')
    lower= np.array([hmin,smin,vmin])
    upper= np.array([hmax,smax,vmax])
    return(lower,upper)
openx,openy,openw,openh=(0,0,0,0)
flag=0
flagb=0
mouse = Controller()
app = wx.App(False)
(sx,sy) = wx.GetDisplaySize()
(camx,camy)=(420,300)
#img=cv2.imread('pic.jpg')
#img=resize(img)
var=cv2.VideoCapture(1,cv2.CAP_DSHOW)
#cv2.imshow('Original',img)
KernelOpen=np.ones((5,5))
KernelClose=np.ones((20,20))
mouseOld=np.array([0,0])
mouseLoc=np.array([0,0])
DampingFactor=3
while True:
    success,img = var.read()
    img=cv2.resize(img,(camx,camy))
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    g_lower = np.array([79,145,36])
    g_upper = np.array([94,255,205])
    r_lower= np.array([104,112,107])
    r_upper= np.array([114,255,255])
    g_mask_final = ret_mask(imgHSV,g_lower,g_upper,KernelOpen,KernelClose)
    r_mask_final = ret_mask(imgHSV,r_lower,r_upper,KernelOpen,KernelClose)
    #cv2.imshow("RED mask",r_mask_final)
    #result = cv2.bitwise_and(img,img,mask=r_mask_final)
    g_cont,hier = cv2.findContours(g_mask_final,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    r_cont,hier1 = cv2.findContours(r_mask_final,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(img,cont,-1,(0,255,0),3)
    #cv2.imshow("and",result)
    #print(len(g_cont)+len(r_cont))
    if (len(r_cont) == 1 and len(g_cont) == 2):
        x1,y1,w1,h1 = cv2.boundingRect(g_cont[0])
        x2,y2,w2,h2 = cv2.boundingRect(g_cont[1])
        x3,y3,w3,h3 = cv2.boundingRect(r_cont[0])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(0,255,0),2)
        cv2.rectangle(img,(x3,y3),(x3+w3,y3+h3),(0,255,0),2)
        #draw_line(x1,y1,w1,h1 , x2,y2,w2,h2, img)
        cx1 = x1+w1//2
        cy1 = y1+h1//2
        cx2 = x2+w2//2
        cy2 = y2+h2//2
        cx3 = x3+w3//2
        cy3 = y3+h3//2
        cx = (cx1+cx2)//2
        cy = (cy1+cy2)//2
        cv2.line(img,(cx1,cy1),(cx2,cy2),(255,0,255),2)
        cv2.circle(img,(cx,cy),2,(0,0,255),2)
        cv2.circle(img,(cx3,cy3),2,(0,0,255),2)
        if flag==1:
            flag=0
            mouse.release(Button.left)
        if flagb==1:
            flagb=0
            mouse.release(Button.right)
        if flagb==0:
            if abs(distance(cx1,cy1,cx3,cy3))<30 or abs(distance(cx2,cy2,cx3,cy3))<30:
                #print(distance(cx1,cy1,cx3,cy3))
                #print(distance(cx2,cy2,cx3,cy3))
                flagb=1
                mouse.press(Button.right)
        if distance(cx1,cy1,cx2,cy2) > 130 and (distance(cx1,cy1,cx3,cy3)>100 and distance(cx2,cy2,cx3,cy3)>100):
            mouse.scroll(0,-2)
            time.sleep(0.3)
        if distance(cx1,cy1,cx2,cy2) > 125 and (distance(cx1,cy1,cx3,cy3)<100 or distance(cx2,cy2,cx3,cy3)<100):
            mouse.scroll(0,2)
            time.sleep(0.3)
        mouseLoc=mouseOld+((cx,cy)-mouseOld)/DampingFactor
        #mouseLoc=(sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy)
        mouse.position=(sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy)
        while mouse.position != (sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy):
            pass
        mouseOld=mouseLoc
        openx,openy,openw,openh = cv2.boundingRect(np.array([[[x1,y1],[x1+w1,y1+h1],[x2,y2],[x2+w2,y2+h2]]]))
        print("Green distances: ")
        print(distance(cx1,cy1,cx2,cy2))
        print("Between green and blue: ")
        print(distance(cx1,cy1,cx3,cy3))
        print(distance(cx2,cy2,cx3,cy3))
    elif len(g_cont) == 1:
        x,y,w,h = cv2.boundingRect(g_cont[0])
        if flag==0:
            #print((abs((w*h - openw*openh)*100/(w*h))))
            if (abs((w*h - openw*openh)*100/(w*h))) < 200:
                flag=1
                mouse.press(Button.left)
                openx,openy,openw,openh=(0,0,0,0)
        else:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cx = x+w//2
            cy = y+h//2
            cv2.circle(img,(cx,cy),(w+h)//4,(0,0,255),2)
            mouseLoc=mouseOld+((cx,cy)-mouseOld)/DampingFactor
            mouse.position=(sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy)
            while mouse.position != (sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy):
                pass
            mouseOld=mouseLoc
    cv2.imshow('video',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        cv2.destroyAllWindows()
        break
