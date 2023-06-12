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
import math as Math
# import autopy as ap
import time

def main():
    cap = cv.VideoCapture(0)

    #mediapipe variables
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    WB_DELAY = 20

    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    #setting webcam height and width
    cap.set(3, 1024) 
    cap.set(4, 720)

    #setting hand detection parameters, and choosing max number of hands to detect
    detector = HandDetector(detectionCon=0.7, maxHands= 1)
    poseDetector = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    yellow = [0,255,255]
    red = [0,0,255]
    blue = [255,0,0]
    green = [0,255,0]
    orange = [0,165,255]
    drawPoints = [[]]                       #drawPoints array of array to store multiple points of the line
    pointNum = -1
    drawCase = False
    counter = 10

    #mousePointer Variables
    mouseCounter = 10
    plockX, plockY = 0, 0
    clockX, clockY = 0, 0

    #button Variables
    buttonCounter = 10

    cv.namedWindow('Image',cv.WND_PROP_FULLSCREEN)
    # cv.setWindowProperty('Image', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    # cv.setWindowProperty('Image', cv.WND_PROP_TOPMOST, 1)

    while(True):
        success, img = cap.read()
        textDisplay = ""
        poseText = ""

        #camera not opened
        if img is None:
            print("Cannot open camera")
            exit()

        #detecting pose
        pose_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        pose_img.flags.writeable = False 
        results = poseDetector.process(pose_img)

        #detecting hands
        hands = detector.findHands(img, draw= False, flipType=True)

        #drawing pose landmarks
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        pose_points = results.pose_landmarks.landmark

        #for hands
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

            if (fingers == [1, 1, 1, 1, 1] and wrist[1] > indexFinger[1]) and counter >= WB_DELAY:
                cv.circle(img, (middleFinger[0], middleFinger[1]-20), 5, yellow, 2)
                redThickNess  = greenThickNess = blueThickNess = 12
                if drawCase == False:
                    cv.waitKey(100)
                    drawCase = True
                    redPoint = indexFinger[0], indexFinger[1]-20
                    greenPoint = ringFinger[0], ringFinger[1]-20
                    bluePoint = pinkyFinger[0], pinkyFinger[1]-20
                    redCase = False
                    greenCase = False
                    blueCase = False

                if Math.sqrt((redPoint[0]-middleFinger[0])**2 + (redPoint[1]-(middleFinger[1]-20))**2) <= 12:
                    redThickNess = 15

                    if redCase == False: 
                        redCase = True
                        greenCase = False
                        blueCase = False
                        buttonCounter = 0

                    cv.putText(img, "WhiteBoard", (redPoint[0]-50, redPoint[1]-50), cv.FONT_HERSHEY_DUPLEX, 0.7, orange, 0)

                    if buttonCounter >= WB_DELAY:
                        buttonCounter = 0
                        print("Whiteboard")
                        # counter = wh.generateWhiteBoard(cap,detector, WB_DELAY)

                elif Math.sqrt((greenPoint[0]-middleFinger[0])**2 + (greenPoint[1]-(middleFinger[1]-20))**2) <= 12:
                    greenThickNess = 15

                    if greenCase == False: 
                        redCase = False
                        greenCase = True
                        blueCase = False
                        buttonCounter = 0

                    cv.putText(img, "ASL Typing", (greenPoint[0]-50, greenPoint[1]-50), cv.FONT_HERSHEY_DUPLEX, 0.7, orange, 0)

                    if buttonCounter >= WB_DELAY:
                        buttonCounter = 0
                        print("ASL Typing")

                elif Math.sqrt((bluePoint[0]-middleFinger[0])**2 + (bluePoint[1]-(middleFinger[1]-20))**2) <= 12:
                    blueThickNess = 15

                    if blueCase == False:
                        redCase = False
                        greenCase = False
                        blueCase = True
                        buttonCounter = 0

                    cv.putText(img, "System Control", (bluePoint[0]-50, bluePoint[1]-50), cv.FONT_HERSHEY_DUPLEX, 0.7, orange, 0)

                    if buttonCounter >= WB_DELAY:
                        buttonCounter = 0
                        print("System Control")

                else:
                    redThickNess  = greenThickNess = blueThickNess = 12

                cv.circle(img, redPoint, redThickNess, red, -2)
                cv.circle(img, greenPoint, greenThickNess, green, -2)
                cv.circle(img, bluePoint, blueThickNess, blue, -2)   
            
            else:
                drawCase = False




            #condition for exiting the program
            # if fingers == [1, 1, 1, 1, 1] and counter >= WB_DELAY:

            #     #finding distance between TIP landmarks
            #     length1, info = detector.findDistance(middleFinger, indexFinger)
            #     length2, info = detector.findDistance(ringFinger, middleFinger)
            #     length3, info = detector.findDistance(pinkyFinger, ringFinger)
            #     if length1 <=30 and length2 >=50 and length3 <=45:
            #         textDisplay = "Live Long and Prosper"

            #whiteboard trigger
            # if (fingers == [0, 1, 0 , 0, 1] and wrist[1] > indexFinger[1]) and counter >= WB_DELAY and hands[0]["type"] == "Right":
            #     drawPoints.clear()
            #     pointNum = -1
            #     drawCase = False
            #     counter = wh.generateWhiteBoard(cap,detector, WB_DELAY)
            
            #mouseMove trigger
            # if hands[0]["type"] == "Left":
            #     textDisplay = "Mouse Mode"
            #     if fingers == [0, 1, 0, 0 ,0] and  wrist[1] > indexFinger[1]:
            #         cv.rectangle(img, (420, 100), (600, 300), red, 2)
            #         xMouse = np.interp(indexFinger[0], (420, 640-100), (0, 1920))
            #         yMouse = np.interp(indexFinger[1], (100, 480-200), (0, 1080))
            #         cv.circle(img, indexFinger, 10, yellow, cv.FILLED)

            #         #smoothing the mouse movement
            #         clockX = plockX + (xMouse - plockX) / 5
            #         clockY = plockY + (yMouse - plockY) / 5

            #         ap.mouse.move(1920-clockX, clockY)
            #         plockX, plockY = clockX, clockY
            #     if (fingers == [1, 0, 0, 0 ,0] or fingers == [1, 1, 0, 0 ,0]) and mouseCounter >= WB_DELAY:
            #         mouseCounter = 0
            #         ap.mouse.click()
            #     elif (fingers == [0, 0, 0, 0 ,1] or  fingers == [0, 1, 0, 0 ,1]) and mouseCounter >= WB_DELAY:
            #         mouseCounter = 0
            #         ap.mouse.click(ap.mouse.Button.RIGHT)
                    

            #if all fingers are closed then clear the screen
            # if fingers == [0, 0, 0, 0 ,0] and hands[0]["type"] == "Right":
            #     textDisplay = "Draw Mode"
            #     drawPoints.clear()
            #     pointNum = -1
            #     drawCase = False

            #if 2 fingers are open then draw a circle on the index finger
            # if fingers == [0, 1, 1, 0 ,0] and  wrist[1] > indexFinger[1] and hands[0]["type"] == "Right":
            #     textDisplay = "Draw Mode"
            #     cv.circle(img, indexFinger, 10, yellow, 2)
            
            #if index finger is open then draw a line
            # if fingers == [0, 1, 0, 0 ,0] and  wrist[1] > indexFinger[1] and hands[0]["type"] == "Right":
            #     textDisplay = "Draw Mode"
            #     cv.circle(img, indexFinger, 10, yellow, 2)
            #     #making a new array of points for a new line
            #     if drawCase == False:
            #         drawCase = True
            #         pointNum = pointNum + 1
            #         drawPoints.append([])
            #     drawPoints[pointNum].append(indexFinger)
            
            # else:
            #     drawCase = False
        
        if pose_points is not None:
            if pose_points[13].y < pose_points[11].y or pose_points[15].y < pose_points[13].y:
                poseText = "Left Arm Up"
                # print("Left Arm Up")
            if pose_points[14].y < pose_points[12].y or pose_points[16].y < pose_points[14].y:
                poseText = "Right Arm Up"
                # print("Right Arm Up")




        c = cv.waitKey(1)

        if textDisplay == "Live Long and Prosper":
            cv.putText(img, textDisplay, (0, 50), cv.FONT_HERSHEY_TRIPLEX, 1.5, orange, 2)
        else:
            cv.putText(img, textDisplay, (10, 50), cv.FONT_HERSHEY_PLAIN, 2, blue, 2)
        
        # cv.putText(img, poseText, (600, 600), cv.FONT_HERSHEY_PLAIN, 2, blue, 2)
        
        #drawing the lines
        for i in range(len(drawPoints)):
            for j in range(len(drawPoints[i])):
                if j!=0:
                    cv.line(img, drawPoints[i][j-1], drawPoints[i][j], red, 12)

        #resizing the window
        img = cv.resize(img, (1280,720), interpolation = cv.INTER_CUBIC)
        cv.resizeWindow('Image', 1280, 720)
        # cv.moveWindow('Image', 1920-320, 0)
        cv.imshow('Image', img)

        #counters for delay for whiteboard and mouse movements
        counter += 1
        mouseCounter += 1
        buttonCounter += 1
        
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


