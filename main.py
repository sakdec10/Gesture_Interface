#Sakshma Bansal , sb8255@rit.edu
#This file is the main file for the project. It contains control for the mouse pointer and gestures and calls the whiteboard function.
#References:
#cvzone : https://github.com/cvzone/cvzone
#mediapipe : https://google.github.io/mediapipe/solutions/hands.html
#autopy : https://github.com/autopilot-rs/autopy

import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import whiteboard as wh
import autopy as ap
import time

def main():
    cap = cv.VideoCapture(0)

    WB_DELAY = 20

    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    #setting webcam height and width
    cap.set(3, 640) 
    cap.set(4, 480)

    #setting hand detection parameters, and choosing max number of hands to detect
    detector = HandDetector(detectionCon=0.7, maxHands= 1)
    yellow = [0,255,255]
    red = [0,0,255]
    blue = [255,0,0]
    orange = [0,165,255]
    drawPoints = [[]]                       #drawPoints array of array to store multiple points of the line
    pointNum = -1
    drawCase = False
    counter = 10

    #mousePointer Variables
    mouseCounter = 10
    plockX, plockY = 0, 0
    clockX, clockY = 0, 0
    

    cv.namedWindow('Image',cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty('Image', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.setWindowProperty('Image', cv.WND_PROP_TOPMOST, 1)

    while(True):
        success, img = cap.read()
        textDisplay = ""

        #camera not opened
        if img is None:
            print("Cannot open camera")
            exit()

        hands, img = detector.findHands(img, flipType=True)


        if hands:
            #getting list of hand landmarks
            lmlist = hands[0]["lmList"] 

            #getting coordinates of landmarks                            
            indexFinger = lmlist[8][0], lmlist[8][1]
            wrist = lmlist[0][0], lmlist[0][1]
            middleFinger = lmlist[12][0], lmlist[12][1]
            ringFinger = lmlist[16][0], lmlist[16][1]
            pinkyFinger = lmlist[20][0], lmlist[20][1]

            #getting list of fingers that are up. 1 for up and 0 for down
            fingers = detector.fingersUp(hands[0])

            #condition for exiting the program
            if fingers == [1, 1, 1, 1, 1] and counter >= WB_DELAY:

                #finding distance between TIP landmarks
                length1, info = detector.findDistance(middleFinger, indexFinger)
                length2, info = detector.findDistance(ringFinger, middleFinger)
                length3, info = detector.findDistance(pinkyFinger, ringFinger)
                if length1 <=30 and length2 >=50 and length3 <=45:
                    textDisplay = "Live Long and Prosper"

            #whiteboard trigger
            if (fingers == [0, 1, 0 , 0, 1] and wrist[1] > indexFinger[1]) and counter >= WB_DELAY and hands[0]["type"] == "Right":
                drawPoints.clear()
                pointNum = -1
                drawCase = False
                counter = wh.generateWhiteBoard(cap,detector, WB_DELAY)
            
            #mouseMove trigger
            if hands[0]["type"] == "Left":
                textDisplay = "Mouse Mode"
                if fingers == [0, 1, 0, 0 ,0] and  wrist[1] > indexFinger[1]:
                    cv.rectangle(img, (420, 100), (600, 300), red, 2)
                    xMouse = np.interp(indexFinger[0], (420, 640-100), (0, 1920))
                    yMouse = np.interp(indexFinger[1], (100, 480-200), (0, 1080))
                    cv.circle(img, indexFinger, 10, yellow, cv.FILLED)

                    #smoothing the mouse movement
                    clockX = plockX + (xMouse - plockX) / 5
                    clockY = plockY + (yMouse - plockY) / 5

                    ap.mouse.move(1920-clockX, clockY)
                    plockX, plockY = clockX, clockY
                if (fingers == [1, 0, 0, 0 ,0] or fingers == [1, 1, 0, 0 ,0]) and mouseCounter >= WB_DELAY:
                    mouseCounter = 0
                    ap.mouse.click()
                elif (fingers == [0, 0, 0, 0 ,1] or  fingers == [0, 1, 0, 0 ,1]) and mouseCounter >= WB_DELAY:
                    mouseCounter = 0
                    ap.mouse.click(ap.mouse.Button.RIGHT)
                    

            #if all fingers are closed then clear the screen
            if fingers == [0, 0, 0, 0 ,0] and hands[0]["type"] == "Right":
                textDisplay = "Draw Mode"
                drawPoints.clear()
                pointNum = -1
                drawCase = False

            #if 2 fingers are open then draw a circle on the index finger
            if fingers == [0, 1, 1, 0 ,0] and  wrist[1] > indexFinger[1] and hands[0]["type"] == "Right":
                textDisplay = "Draw Mode"
                cv.circle(img, indexFinger, 10, yellow, 2)
            
            #if index finger is open then draw a line
            if fingers == [0, 1, 0, 0 ,0] and  wrist[1] > indexFinger[1] and hands[0]["type"] == "Right":
                textDisplay = "Draw Mode"
                cv.circle(img, indexFinger, 10, yellow, 2)
                #making a new array of points for a new line
                if drawCase == False:
                    drawCase = True
                    pointNum = pointNum + 1
                    drawPoints.append([])
                drawPoints[pointNum].append(indexFinger)
            
            else:
                drawCase = False
        
        c = cv.waitKey(1)

        if textDisplay == "Live Long and Prosper":
            cv.putText(img, textDisplay, (0, 50), cv.FONT_HERSHEY_TRIPLEX, 1.5, orange, 2)
        else:
            cv.putText(img, textDisplay, (10, 50), cv.FONT_HERSHEY_PLAIN, 2, blue, 2)
        
        #drawing the lines
        for i in range(len(drawPoints)):
            for j in range(len(drawPoints[i])):
                if j!=0:
                    cv.line(img, drawPoints[i][j-1], drawPoints[i][j], red, 12)

        #resizing the window
        img = cv.resize(img, (1920,1080), interpolation = cv.INTER_CUBIC)
        cv.resizeWindow('Image', 320, 240)
        cv.moveWindow('Image', 1920-320, 0)
        cv.imshow('Image', img)

        #counters for delay for whiteboard and mouse movements
        counter += 1
        mouseCounter += 1
        
        #exit condition
        if(textDisplay == "Live Long and Prosper"):
            counter = 0
            while counter < 10:
                cv.waitKey(1)
                cv.imshow('Image', img)
                counter +=1
            time.sleep(3)
            break
        
        #exit with escape key
        if c == 27:
            break
    
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()


