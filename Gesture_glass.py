import numpy as np
import cv2
from pynput.mouse import Button,Controller
import wx
'''def resize(img):
    img=cv2.resize(img,(852,480))
    return img'''
def func(a):
    pass
    return
'''def draw_line(x1,y1,h1,w1,x2,y2,h2,w2,img):
    cx1 = x1+w1//2
    cy1 = y1+h1//2
    cx2 = x2+w2//2
    cy2 = y2+h2//2
    cx = (cx1+cx2)//2
    cy = (cy1+cy2)//2
    cv2.line(img,(cx1,cy1),(cx2,cy2),(255,0,255),2)
    cv2.circle(img,(cx,cy),2,(0,0,255),2)'''
openx,openy,openw,openh=(0,0,0,0)
flag=0
mouse = Controller()
app = wx.App(False)
(sx,sy) = wx.GetDisplaySize()
(camx,camy)=(420,300)
#img=cv2.imread('pic.jpg')
#img=resize(img)
var=cv2.VideoCapture(1)
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
    lower = np.array([79,145,36])
    upper = np.array([94,255,205])
    mask = cv2.inRange(imgHSV,lower,upper)
    mask_open = cv2.morphologyEx(mask,cv2.MORPH_OPEN,KernelOpen)
    mask_close = cv2.morphologyEx(mask_open,cv2.MORPH_CLOSE,KernelClose)
    mask_final = mask_close
    result = cv2.bitwise_and(img,img,mask=mask_final)
    cont,hier = cv2.findContours(mask_final,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(img,cont,-1,(0,255,0),3)


    if len(cont)== 2:
        x1,y1,w1,h1 = cv2.boundingRect(cont[0])
        x2,y2,w2,h2 = cv2.boundingRect(cont[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(0,255,0),2)
        #draw_line(x1,y1,w1,h1 , x2,y2,w2,h2, img)
        cx1 = x1+w1//2
        cy1 = y1+h1//2
        cx2 = x2+w2//2
        cy2 = y2+h2//2
        cx = (cx1+cx2)//2
        cy = (cy1+cy2)//2
        cv2.line(img,(cx1,cy1),(cx2,cy2),(255,0,255),2)
        cv2.circle(img,(cx,cy),2,(0,0,255),2)
        if flag==1:
            flag=0
            mouse.release(Button.left)
        mouseLoc=mouseOld+((cx,cy)-mouseOld)/DampingFactor
        #mouseLoc=(sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy)
        mouse.position=(sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy)
        while mouse.position != (sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy):
            pass
        mouseOld=mouseLoc
        openx,openy,openw,openh = cv2.boundingRect(np.array([[[x1,y1],[x1+w1,y1+h1],[x2,y2],[x2+w2,y2+h2]]]))
        #cv2.rectangle(img,(openx,openy),(openx+openw,openy+openh),(0,255,0),2)
        #print("printing opens")
        #print(openx,openy,openw,openh)
    elif len(cont) == 1:
        x,y,w,h = cv2.boundingRect(cont[0])
        if flag==0:
            print((abs((w*h - openw*openh)*100/(w*h))))
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