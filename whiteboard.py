import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import whiteboard as wh

def generateWhiteBoard(cap,detector, WB_DELAY) -> int:

    #webcam height and width
    hs, ws = 120, 230

    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    yellow = [0,255,255]
    red = [0,0,255]
    drawPoints = [[]]                       #drawPoints array of array to store multiple points of the line
    pointNum = -1
    drawCase = False
    counter = 0

    while(True):
        success, img = cap.read()
        #Declaring a whiteboard
        wBoard = np.ones((720, 1280, 3), dtype = np.uint8)
        wBoard = wBoard * 255

        #Adding webcam image to whiteboard
        imgSmall = cv.resize(img, (ws, hs))
        wBoard[0:hs,1280-ws:1280] = imgSmall

        #camera not opened
        if img is None:
            print("Cannot open camera")
            exit()

        hands, img = detector.findHands(img)


        if hands:
            lmlist = hands[0]["lmList"]

            if hands[0]["type"] == "Left":
                xInterp = int(np.interp(lmlist[8][0], [1280//2, 1280], [0, 1280]))
                yInterp = int(np.interp(lmlist[8][1], [150, 720-150], [0, 720]))
            else:
                xInterp = int(np.interp(lmlist[8][0], [0, 1280//2], [0, 1280]))
                yInterp = int(np.interp(lmlist[8][1], [150, 720-150], [0, 720]))
            indexFinger = xInterp, yInterp

            wrist = lmlist[0][0], lmlist[0][1]
            fingers = detector.fingersUp(hands[0])

            #close whiteboard trigger
            if (fingers == [0, 1, 0 , 0, 1] and wrist[1] > indexFinger[1]) and counter >= WB_DELAY:
                cv.destroyWindow("Whiteboard")
                return 0
            
            #if all fingers are closed then clear the screen
            if fingers == [0, 0, 0, 0 ,0]:
                drawCase = False
                drawPoints.clear()
                pointNum = -1
            
            #if 2 fingers are open then draw a circle on the index finger
            if fingers == [0, 1, 1, 0 ,0] and  wrist[1] > indexFinger[1]:
                cv.circle(wBoard, indexFinger, 10, red, cv.FILLED)
            
            #if index finger is open then draw a line
            if fingers == [0, 1, 0, 0 ,0] and  wrist[1] > indexFinger[1]:
                cv.circle(wBoard, indexFinger, 10, red, cv.FILLED)
                #making a new array of points for a new line
                if drawCase == False:
                    drawCase = True
                    pointNum = pointNum + 1
                    drawPoints.append([])
                drawPoints[pointNum].append(indexFinger)
            else:
                drawCase = False
        
        c = cv.waitKey(1)
        
        #drawing the lines
        for i in range(len(drawPoints)):
            for j in range(len(drawPoints[i])):
                if j!=0:
                    cv.line(wBoard, drawPoints[i][j-1], drawPoints[i][j], red, 12)

        cv.imshow("Image", cv.flip(img, 1))
        cv.imshow("Whiteboard", cv.flip(wBoard, 1))
        counter+=1
        
        if c == 27:
            break

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    cap.set(3, 1280) 
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.3, maxHands= 1)
    generateWhiteBoard(cap, detector, 20)


