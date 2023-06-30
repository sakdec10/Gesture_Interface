import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import pyautogui as pyg
import platform
# import autopy as ap

def controlSystem(cap,detector, WB_DELAY) -> int:
    
    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    #checking if the platform is mac or not
    if "mac" in platform.platform().lower():
        mac = True
    else:
        mac = False

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

    #mouse variables
    mouseCounter = 10
    plockX, plockY = 0, 0
    clockX, clockY = 0, 0

    #creating a window for the camera
    cv.namedWindow('Image',cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty('Image', cv.WND_PROP_TOPMOST, 1)

    while(True):
        success, img = cap.read()

        if img is None:
            print("Cannot open camera")
            exit()

        hands, img = detector.findHands(img)
        cv.putText(img, "System Control", (10, 50), cv.FONT_HERSHEY_PLAIN, 2, red, 2)

        if hands:
            lmlist = hands[0]["lmList"]
            indexFinger = lmlist[8][0], lmlist[8][1]
            wrist = lmlist[0][0], lmlist[0][1]
            fingers = detector.fingersUp(hands[0])
        
            #closing system control
            if hands[0]["type"] == "Left":
                if (fingers == [0, 1, 0 , 0, 1] and wrist[1] > indexFinger[1]) and counter >= WB_DELAY:
                    return 0

            # mouseMove trigger
            if hands[0]["type"] == "Right":
                if fingers == [0, 1, 0, 0 ,0] and  wrist[1] > indexFinger[1]:
                    # cv.rectangle(img, (420, 100), (600, 300), red, 2)
                    # xMouse = np.interp(indexFinger[0], (420, 640-100), (0, 1920))
                    # yMouse = np.interp(indexFinger[1], (100, 480-200), (0, 1080))
                    xMouse = int(np.interp(lmlist[8][0], [50, 1024//2], [0, screen_width]))
                    yMouse = int(np.interp(lmlist[8][1], [50, 400], [0, screen_height]))
                    cv.circle(img, indexFinger, 10, yellow, cv.FILLED)

                    # smoothing the mouse movement
                    # clockX = plockX + (xMouse - plockX) / 5
                    # clockY = plockY + (yMouse - plockY) / 5

                    pyg.moveTo(xMouse, yMouse, 0.1, pyg.easeInQuad, _pause=False)

                    # ap.mouse.move(1920-clockX, clockY)
                    # plockX, plockY = clockX, clockY

                if (fingers == [1, 0, 0, 0 ,0] or fingers == [1, 1, 0, 0 ,0]) and mouseCounter >= WB_DELAY:
                    mouseCounter = 0
                    pyg.click(button='left')
                elif (fingers == [0, 0, 0, 0 ,1] or  fingers == [0, 1, 0, 0 ,1]) and mouseCounter >= WB_DELAY:
                    mouseCounter = 0
                    pyg.click(button='right')
                    








        c = cv.waitKey(1)

        #displaying the webcam
        # img = cv.resize(img, (1920,1080), interpolation = cv.INTER_CUBIC)
        cv.resizeWindow('Image', 320, 240)
        if mac:
            cv.moveWindow('Image', screen_width-320, -200)
        else:
            cv.moveWindow('Image', screen_width-320, 0)
        cv.imshow('Image', img)

        #counter to add delay to the close whiteboard trigger
        counter+=1
        mouseCounter+=1
        
        if c == 27:
            break

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    cap.set(3, 1024)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.3, maxHands= 1)
    controlSystem(cap, detector, 20)