
## Project HandTracking
pathtomodules = "C:\\Users\\matbo\Documents\\Programmation\\Python\\E3\\Traitement_images"
sys.path.append(pathtomodules)
##
from cv2 import *
import mediapipe as mp  #pip install --user mediapipe
import time
import math
import autopy
import sys

#import HandTrackingModule #as htrm
from pynput.mouse import Button, Controller

#import HandTrackingModule
## cmd launch : jupyter lab
##



m = 1.4;
hcam = int(480*m) #720
wcam = int(640*m) #1280
cap = cv2.VideoCapture(1)
size = cap.get(1)
cap.set(3,wcam)
cap.set(4,hcam)
smoothering = 4 #smoothering factor to implement 8
wScreen, hScreen = autopy.screen.size()
detector = handDetector(detectionCon =0.7, trackCon=0.7)
detector.test_class();
mouse = Controller()
pTime = 0
cTime = 0
px1, py1 = 0,0
pdx1, pdy1 = 0,0


while True:
    success,img = cap.read()
    img = detector.findHands(img)
    h, w, c = img.shape
    rw,rh = w/1900, h/1060 #w/1917, h/1075 # size plus faible 1900 / 1060
    lmList = detector.findPosition(img, handNo=0, draw = False)
    rect_min_x = int(w*0.08)
    rect_max_x = int(w*0.94)
    rect_min_y = int(h*0.1)
    rect_max_y = int(h*0.85)


    if len(lmList)!=0:
        # print(lmList[4])
        # print(lmList[8])
        x1,y1 = lmList[8][1],lmList[8][2]
        x2,y2 = lmList[12][1],lmList[12][2]
        xt,yt = lmList[4][1],lmList[4][2]
        x3,y3 = lmList[16][1],lmList[16][2]
        x4,y4 = lmList[20][1],lmList[20][2]
        cx1,cy1 = (xt+x1)//2, (yt+y1)//2
        cx2,cy2 = (xt+x2)//2, (yt+y2)//2
        cx3,cy3 = (xt+x3)//2, (yt+y3)//2
        cx4,cy4 = (xt+x4)//2, (yt+y4)//2
        # cv2.line(img,(xt,yt),(x1,y1),(0,0,255), 2)
        # cv2.line(img,(xt,yt),(x2,y2),(0,0,255), 2)
        # cv2.line(img,(xt,yt),(x3,y3),(0,0,255), 2)
        # cv2.line(img,(xt,yt),(x4,y4),(0,0,255), 2)
        # cv2.circle(img, (cx1,cy1), 11, (0,0,255),cv2.FILLED)
        # cv2.circle(img, (cx2,cy2), 11, (0,0,255),cv2.FILLED)
        # cv2.circle(img, (cx3,cy3), 11, (0,0,255),cv2.FILLED)
        # cv2.circle(img, (cx4,cy4), 11, (0,0,255),cv2.FILLED)
    # # dt1 = math.hypot(xt-x1,yt-y1)
        # dt2 = math.hypot(xt-x2,yt-y2)
        # dt3 = math.hypot(xt-x3,yt-y3)
        # dt4 = math.hypot(xt-x4,yt-y4)
        test8 = detector.detect_touch(img,lmList,ref_landmark=4,landmark=8,thresh=34)
        test12 = detector.detect_touch(img,lmList,ref_landmark=4,landmark=12,thresh=36)
        test16 = detector.detect_touch(img,lmList,ref_landmark=4,landmark=16,thresh=36)
        test20 = detector.detect_touch(img,lmList,ref_landmark=4,landmark=20,thresh=35)
        if test8:
            cv2.circle(img, (cx1,cy1), 11, (0,255,0),cv2.FILLED)
            cv2.rectangle(img,[int(w*0.08),int(h*0.1)],[int(w*0.92),int(h*0.9)],[255,255,255],3)
            #mouse.position = (int(cx1/rw/0.83-w*0.2),int(cy1/rh/0.83-h*0.2))
            move_x, move_y = filter_low_pass(pdx1,pdy1)
            mouse.move(-(move_x)/0.5,(move_y)/0.5)
            #mouse.move(-(pdx1 + x1-px1)/1.2,(pdy1 + y1-py1)/1.3) #smoothering
        pdx1 = x1 - px1
        pdy1 = y1 - py1
        px1 =x1;
        py1 =y1;


        mouse.release(Button.left)
        if test12: #plus difficile à capter précisément
            cv2.circle(img, (cx2,cy2), 11, (0,255,0),cv2.FILLED)
            mouse.click(Button.left,1)
            time.sleep(0.05)
        if test16:
            cv2.circle(img, (cx3,cy3), 11, (0,255,0),cv2.FILLED)
            mouse.click(Button.right,1)
            time.sleep(0.05)
        if test20:
            cv2.circle(img, (cx4,cy4), 11, (0,255,0),cv2.FILLED)
            mouse.press(Button.left)
            if test8 and test12 and test16 :
                break

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    #cv2.line(img,(0,int(0.9*h)),(w,int(0.9*h)),(255,255,255), 4)
    cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(250,250,250),1)

    cv2.imshow("Image",img)

    if (cv2.waitKey(1) & 0xFF == ord('q')) :

    # test si on appuie sur q (ou x)
        break

# When everything done, release the capture
mouse.release(Button.left)
cap.release()
cv2.destroyAllWindows()