import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import pyautogui as pyg
import platform

def drawKB(cap,detector, WB_DELAY)-> str:

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

    #creating a window for the camera
    cv.namedWindow('Image',cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty('Image', cv.WND_PROP_TOPMOST, 1)

    while(True):
        success, img = cap.read()

        if img is None:
            print("Cannot open camera")
            exit()
        
        hands, img = detector.findHands(img)
         

















        c = cv.waitKey(1)
        img = cv.resize(img, (1920,1080), interpolation = cv.INTER_CUBIC)
        cv.resizeWindow('Image', screen_width, screen_height)
        if mac:
            cv.moveWindow('Image', 0, -200)
        else:
            cv.moveWindow('Image', 0, 0)
        cv.imshow('Image', img)

        #counter to add delay to the close whiteboard trigger
        counter+=1
        
        if c == 27:
            break

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    cap.set(3, 1024)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.3, maxHands= 1)
    drawKB(cap, detector, 20)