import cv2
import time
import numpy as np
import htmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######################################
wCam, hCam = 640 , 480
###################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0



detector = htm.handDectector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#volume.GetMute()
#volume.GetMasterVolummeLevel()
volRange = volume.GetVolumeRange()

minVOl = volRange[0]
maxVol = volRange[1]
vol =0
volBar = 400
volPer = 0


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist =detector.findpostion(img, draw=False)
    if len(lmlist) !=0:
        #print(lmlist[4], lmlist[8])

        x1, y1 = lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx,cy = (x1+x2)//2 , (y1 +y2) // 2

        cv2.circle(img, (x1,y1), 7,(128,45,23),cv2.FILLED)
        cv2.circle(img, (x2,y2),7, (128, 45, 53), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,245,54),3)
        cv2.circle(img, (cx, cy), 7, (255, 0,225), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        print(length)

        # Hand range 50 -300
        # volume range -65

        vol = np.interp(length,[50,300],[minVOl,maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length,[50,300],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length<50:
            cv2.circle(img, (cx, cy), 7, (0, 0, 253), cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 5, 255), cv2.FILLED)
    cv2.putText(img, f' {int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (25, 25, 255), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'fps: {int(fps)}', (40, 50 ),cv2.FONT_HERSHEY_COMPLEX,
                1,(25, 23 , 255),3)


    cv2.imshow("img" , img )
    cv2.waitKey(1)

