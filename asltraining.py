import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import whiteboard as wh
import system as sys
import math as Math
import pyautogui as pyg
import time
import platform
from matplotlib import pyplot as plt

def main():
    
    cap = cv.VideoCapture(0)

    #checking if the platform is mac or not
    if "mac" in platform.platform().lower():
        mac = True
    else:
        mac = False

    #getting screen size
    screen_width, screen_height = pyg.size()

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
    pose_points = None

    #mousePointer Variables
    mouseCounter = 10
    plockX, plockY = 0, 0
    clockX, clockY = 0, 0
    handBox = False

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
        # mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        try:
            pose_points = results.pose_landmarks.landmark
        except:
            pass

        #for hands
        if hands:
            #getting landmarks of the hand flattened
            lmlist = np.array(hands[0]["lmList"]).flatten()
            

        c = cv.waitKey(1)

        #resizing the window
        img = cv.resize(img, (1280,720), interpolation = cv.INTER_CUBIC)
        cv.resizeWindow('Image', 1280, 720)
        cv.moveWindow('Image', (screen_width-1280)//2, (screen_height-720)//2)
        cv.imshow('Image', img)

        #counters for delay for whiteboard and mouse movements
        counter += 1
        mouseCounter += 1
        buttonCounter += 1
    
        #exit with escape key
        if c == 27:
            break
    
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
