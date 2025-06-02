import cv2
import HandTrackingModule as htm
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
import time
import math
import  numpy as np

length=0
wCam,hCam=640,480
cap=cv2.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

detector=htm.handDetector(detectionCon=0.7)

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]
vol=0
volBar=400
volPer=0

while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    print(lmList)
    if lmList!=([],[]):
        length, img, [x1, y1, x2, y2, cx, cy] = detector.Distance(img, 4, 8, draw=True)


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,"FPS:"+str(int(fps)),(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),3)
    volBar = np.interp(length, [50, 300], [400, 150])

    vol = np.interp(length, [50, 300], [minVol, maxVol])
    volPer = np.interp(length, [50, 300], [0, 100])

    volume.SetMasterVolumeLevel(vol, None)
    print("length:" + str(length) + ",vol:" + str(vol))

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)

    cv2.imshow("Gesture Volume Control",img)
    k=cv2.waitKey(1)
    if k%256==27:
        print("Escape hit,closing...")
        break



cap.release()
cv2.destroyAllWindows()