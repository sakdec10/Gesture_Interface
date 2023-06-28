#Saksham Bansal, sb8255@rit.edu
#This file control whitboard funtionality.
#cvzone : https://github.com/cvzone/cvzone
#mediapipe : https://google.github.io/mediapipe/solutions/hands.html
#autopy : https://github.com/autopilot-rs/autopy

import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import whiteboard as wh
import pyautogui as pyg

def generateWhiteBoard(cap,detector, WB_DELAY) -> int:

    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    #getting screen size
    screen_width, screen_height = pyg.size()

    #declaring variables
    yellow = [0,255,255]
    red = [0,0,255]
    blue = [255,0,0]
    drawPoints = [[]]                       #drawPoints array of array to store multiple points of the line
    pointNum = -1
    drawCase = False
    counter = 0

    #creating a whiteboard window
    cv.namedWindow('Whiteboard',cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty('Whiteboard', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.setWindowProperty('Whiteboard', cv.WND_PROP_TOPMOST, 1)

    #creating a window for the camera
    cv.namedWindow('Image',cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty('Image', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.setWindowProperty('Image', cv.WND_PROP_TOPMOST, 1)

    while(True):
        success, img = cap.read()
        #Declaring a whiteboard
        wBoard = np.ones((720, 1280, 3), dtype = np.uint8)
        wBoard = wBoard * 255

        #camera not opened
        if img is None:
            print("Cannot open camera")
            exit()

        hands, img = detector.findHands(img)
        cv.putText(img, "WhiteBoard", (10, 50), cv.FONT_HERSHEY_PLAIN, 2, red, 2)

        if hands:
            lmlist = hands[0]["lmList"]
            indexFinger = lmlist[8][0], lmlist[8][1]

            #interpolating the index finger position to the whiteboard
            xInterp = int(np.interp(lmlist[8][0], [0, 640//2], [0, 1280]))
            yInterp = int(np.interp(lmlist[8][1], [150, 480-150], [0, 720]))
            
            #if the hand is right then interpolate the x coordinate from 0 to 640/2
            if hands[0]["type"] == "Left":
                xInterp = int(np.interp(lmlist[8][0], [640//2, 640], [0, 1280]))
            
            drawIndex = xInterp, yInterp

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
                cv.circle(wBoard, drawIndex, 10, red, cv.FILLED)
            
            #if index finger is open then draw a line
            if fingers == [0, 1, 0, 0 ,0] and  wrist[1] > indexFinger[1]:
                cv.circle(wBoard, drawIndex, 10, red, cv.FILLED)
                #making a new array of points for a new line
                if drawCase == False:
                    drawCase = True
                    pointNum = pointNum + 1
                    drawPoints.append([])
                drawPoints[pointNum].append(drawIndex)
            else:
                drawCase = False
        
        c = cv.waitKey(1)
        
        #drawing the lines
        for i in range(len(drawPoints)):
            for j in range(len(drawPoints[i])):
                if j!=0:
                    cv.line(wBoard, drawPoints[i][j-1], drawPoints[i][j], red, 12)

        #displaying the webcam
        # img = cv.resize(img, (1920,1080), interpolation = cv.INTER_CUBIC)
        cv.resizeWindow('Image', 320, 240)
        cv.moveWindow('Image', screen_width-320, 0)
        cv.imshow('Image', img)

        #displaying the whiteboard
        cv.resizeWindow('Whiteboard', 1280,720)
        cv.moveWindow('Whiteboard', (screen_width-1280)//2, (screen_height-720)//2)
        cv.imshow("Whiteboard", cv.flip(wBoard, 1))
        
        #counter to add delay to the close whiteboard trigger
        counter+=1
        
        if c == 27:
            break

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    detector = HandDetector(detectionCon=0.3, maxHands= 1)
    generateWhiteBoard(cap, detector, 20)


