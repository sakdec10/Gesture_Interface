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
    white = [255,255,255]
    black = [0,0,0]
    gray = [128,128,128]
    counter = 0
    kb_text = ""
    kb_text_posx, kb_text_posy = 0, 0

    #creating a window for the camera
    cv.namedWindow('Image',cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty('Image', cv.WND_PROP_TOPMOST, 1)

    qkeys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<--"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Done"]]

    keylist = []
    for i in range(4):
        for j in range(11):
            keylist.append([j*50+25, i*55+200, qkeys[i][j]])
            if qkeys[i][j] == 'Z':
                kb_text_posx = j*50+25
                kb_text_posy = i*55+290

    def drawkb(img, keylist):
        for key in keylist:
            x, y, key = key
            if key == "Done" or key == "<--":
                cv.rectangle(img, (x, y), (x+85, y+45), gray, cv.FILLED)
            else:
                cv.rectangle(img, (x, y), (x+35, y+45), gray, cv.FILLED)
            cv.putText(img, key, (x+5, y+30), cv.FONT_HERSHEY_DUPLEX, 1, white, 2)
        return img                                                         

    while(True):
        success, img = cap.read()

        if img is None:
            print("Cannot open camera")
            exit()
        
        hands, img = detector.findHands(img)

        backg = np.ones_like(img, np.uint8)
        backg = backg * 255
        blended_img = cv.addWeighted(backg, 0.5, img, 0.5, 0)
        blended_img = drawkb(blended_img, keylist)

        if hands:
            lmlist = hands[0]["lmList"]
            indexFinger = lmlist[8][0], lmlist[8][1]
            wrist = lmlist[0][0], lmlist[0][1]
            thumb_tip = lmlist[4][0], lmlist[4][1]
            index_mcp = lmlist[5][0], lmlist[5][1]
            fingers = detector.fingersUp(hands[0])

            for key in keylist:
                w, h = 35, 45
                x, y, key = key
                if key == "Done" or key == "<--":
                    w, h = 85, 45
                if x < indexFinger[0] < x+w and y < indexFinger[1] < y+h:
                    cv.rectangle(blended_img, (x-5, y-5), (x+w+5, y+h+5), black, cv.FILLED)
                    cv.putText(blended_img, key, (x+5, y+30), cv.FONT_HERSHEY_DUPLEX, 1, white, 2)
                    length, info= detector.findDistance(index_mcp, thumb_tip)
                    print(length)
                    if length < 43 and counter > WB_DELAY:
                        counter = 10
                        if key == "<--":
                            kb_text = kb_text[:-1]
                        elif key == "Done":
                            print(kb_text)
                            return kb_text
                        else:
                            kb_text += key
                    
                cv.putText(blended_img, kb_text, (kb_text_posx, kb_text_posy), cv.FONT_HERSHEY_DUPLEX, 1, black, 2)
                        

        c = cv.waitKey(1)
        img = cv.resize(blended_img, (1920,1080), interpolation = cv.INTER_CUBIC)
        img = cv.flip(img, 1)
        cv.resizeWindow('Image', screen_width, screen_height)
        if mac:
            cv.moveWindow('Image', 0, -200)
        else:
            cv.moveWindow('Image', 0, 0)
        cv.imshow('Image', blended_img)

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