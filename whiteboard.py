import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import whiteboard as wh

def generateWhiteBoard(cap,detector) -> int:

    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    cap.set(3, 1280) 
    cap.set(4, 720)

    yellow = [0,255,255]
    red = [0,0,255]
    drawPoints = [[]]                       #drawPoints array of array to store multiple points of the line
    pointNum = -1
    drawCase = False
    wBoard = np.ones((720, 1280, 3), dtype = np.uint8)
    wBoard = wBoard * 255
    counter = 0

    while(True):
        success, img = cap.read()

        #camera not opened
        if img is None:
            print("Cannot open camera")
            exit()

        hands, img = detector.findHands(img)


        if hands:
            lmlist = hands[0]["lmList"]
            indexFinger = lmlist[8][0], lmlist[8][1]
            wrist = lmlist[0][0], lmlist[0][1]
            fingers = detector.fingersUp(hands[0])

            if (fingers == [0, 1, 0 , 0, 1] and wrist[1] > indexFinger[1]) and counter >= 10:
                cv.destroyWindow("Whiteboard")
                return 0    
        
        c = cv.waitKey(1)
        
        cv.imshow("Image", cv.flip(img, 1))
        cv.imshow("Whiteboard", wBoard)
        counter+=1
        
        if c == 27:
            break

if __name__ == '__main__':
    generateWhiteBoard()


