# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi("I am Hamed-Mr Developer")

import cv2
import numpy as np
import mediapipe as mp
import autopy
import handtrackingmodule as htm
import time

#################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 5
#################
cap = cv2.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
plocX, plocY = 0,0
clocX, clocY = 0,0
detector = htm.handDetector(maxHands = 1)
wScr , hScr = autopy.screen.size()
#print(wScr, hScr)
finger = []

while True:

    #1. Find the hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)



    #2. Get the tip of the index and middle fingers
    if len(lmList)!= 0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList [12][1:]
        #print(x1, y1, x2, y2)


        #3. Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        #4. only index finger : moving mode
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
        (255, 0, 255), 2)
        if fingers[1] == 1 and fingers[2] ==0:

        #5. conver our cordinates


            x3 = np.interp(x1, (frameR, wCam-frameR),(0,wScr) )
            y3 = np.interp(y1, (frameR, hCam-frameR),(0,hScr) )

        #6. smoothen Values
            clocX = plocX + (x3-plocX)/smoothening
            clocY = plocY + (y3-plocY)/smoothening

        #7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED )
            plocX , plocY = clocX, clocY
        #8 Both Index and middle fingers are up : clicking mode
        if fingers[1] == 1 and fingers[2] ==1:
            cv2.circle(img, (x1,y1), 15,(0,255,0), cv2.FILLED)

            autopy.mouse.click()
        #10. click mouse if distance short
        #11 Frame rate

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0 ), 3)


    cv2.imshow("image", img)
    cv2.waitKey(1)

