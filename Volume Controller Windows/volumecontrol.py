import cv2
import time
import numpy
import numpy as np
import mediapipe as mp
import Trackinghandmod as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam,hcam=1280,720


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volrange=volume.GetVolumeRange()
print(volume.GetVolumeRange())
minvol= volrange[0]
maxvol= volrange[1]
volforbar=400


cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime=0

detector=htm.handdetector(detectionconfi=0.7)


while True:
    _,img=cap.read()

    img=detector.findhand(img)
    lmlist=detector.findposition(img,draw=False)

    if len(lmlist)!=0:
       #print(lmlist[4],lmlist[8])

        x1,y1=lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy=(x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),8,(0,255,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (0, 255, 255), cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(0, 255, 255),3)
        cv2.circle(img, (cx, cy), 8, (0, 255, 255), cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        print(length)
        vol=np.interp(length,[30,130],[minvol,maxvol])
        volforbar = np.interp(length, [30, 130], [400, 150])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length<30:
            cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

    cv2.rectangle(img,(50,150),(100,400),(0,255,255),5)
    cv2.rectangle(img, (50, int(volforbar)), (100, 400), (0, 255, 255), cv2.FILLED)

    ctime=time.time()
    fps=1/(ctime-ptime)
    fps=round(fps)
    ptime=ctime

    cv2.putText(img,f"fps,{str(fps)}",(40,70),cv2.FONT_HERSHEY_PLAIN,3,(200,178,0),3)

    cv2.imshow("Image",img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break