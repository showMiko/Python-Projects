import cv2
import time
import mediapipe
import os 
import Trackinghandmod as htm
import pyautogui
import numpy as np

wcam,hcam=1280,720

cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime=0
tipidd=[4,8,12,16,20]

detector=htm.handDetector(detectionCon=0.7)

while True:
    _,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    img=cv2.flip(img,1)
    #print(lmlist)

    if(len(lmlist)!=0):  
        fingers=[]       
        #For thumb
        if lmlist[tipidd[0]][1]<lmlist[tipidd [0]-1]  [1]    :
            fingers.append(0)
        else:
            fingers.append(1)
          
        #for remaining fingers 
        for id in range(1,5):
            if lmlist[tipidd[id]][2]< lmlist[tipidd[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        totfinger=fingers.count(1)
        print(totfinger)
        x=np.interp(lmlist[8][1],(100,740),(0,1920))
        y=np.interp(lmlist[8][2],(100,580),(0,1080))
        # cv2.circle(img,(lmlist[8][1],lmlist[8][2]),(5),(120,253,0),cv2.FILLED)
        
        pyautogui.moveTo(x,y)

        if totfinger==1:
            pyautogui.leftClick()
        if totfinger==2:
            pyautogui.rightClick()

    ctime=time.time()
    fps=1/(ctime-ptime)
    fps=round(fps)
    ptime=ctime

    cv2.putText(img,str(fps),(500,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(235,150,56),4)
    cv2.imshow("Image",img)

    if(cv2.waitKey(1) & 0xFF == ord("q")):
        break