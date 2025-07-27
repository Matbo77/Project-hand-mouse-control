


from cv2 import *
import mediapipe as mp  #pip install --user mediapipe
import time
import math

## cmd launch : jupyter lab
##

class handDetector():
    def __init__(self, mode=False,maxHands=2, detectionCon =0.5, trackCon=0.5 ):
        self.mode=mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon) #default parameters
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw :
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True ):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                #print(id,cx,cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 10, (255,0,255),cv2.FILLED)
        return lmList

    def test_class(self):
        print("wouah la fonction de la class !")
        return True

    def detect_touch(self, img, lmList, ref_landmark=4, landmark=8 , thresh=40 ):
        xref,yref = lmList[ref_landmark][1],lmList[ref_landmark][2]
        x1,y1 = lmList[landmark][1],lmList[landmark][2]
        cx1,cy1 = (xref+x1)//2, (yref+y1)//2
        cv2.line(img,(xref,yref),(x1,y1),(0,0,255), 2)
        cv2.circle(img, (cx1,cy1), 11, (0,0,255),cv2.FILLED)
        self.dist = math.hypot(xref-x1,yref-y1)
        if abs(self.dist)<36:
            #cv2.circle(img, (cx,cy), 11, (0,255,0),cv2.FILLED)
            return True
        else :
            return False

def filter_low_pass(dx1,dy1,last_value=[[0,0],[0,0]]):
    move_x, move_y = (dx1+last_value[0][0]+last_value[0][1])/3,(dy1+last_value[1][0]+last_value[1][1])/3
    print(last_value)
    last_value[0][1],last_value[1][1] = last_value[0][0],last_value[1][0]
    last_value[0][0],last_value[1][0] = dx1,dy1
    return move_x,move_y



def main():

    # pTime = 0
    # cTime = 0
    # cap = cv2.VideoCapture(1)
    # size = cap.get(1)
    #detector = handDetector(detectionCon =0.8, trackCon=0.8)

    #
    # while True:
    #     success,img = cap.read()
    #     img = detector.findHands(img)
    #     lmList = detector.findPosition(img)
    #     if len(lmList)!=0:
    #         print(lmList[4])
    #
    #     cTime = time.time()
    #     fps = 1/(cTime-pTime)
    #     pTime = cTime
    #
    #
    #     cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(250,250,250),1)
    #
    #     cv2.imshow("Image",img)
    #
    #     if (cv2.waitKey(1) & 0xFF == ord('q')) | (cv2.waitKey(1) & 0xFF == ord('x')) :
    #
    #     # test si on appuie sur q ou x
    #         break
    #
    # # When everything done, release the capture
    # cap.release()
    # cv2.destroyAllWindows()

    if __name__ == "__main__":
        main()