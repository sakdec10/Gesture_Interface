import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import pyautogui as pyg
import platform
import os
import pickle

def generateASL(cap,detector, WB_DELAY)-> str:

    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    WB_DELAY = 30

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
    green = [0,255,0]
    counter = 0
    asl_text = ""
    aslTextX, aslTextY = 15, 200
    temp_pred = ""

    #creating a window for the camera
    cv.namedWindow('Image',cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty('Image', cv.WND_PROP_TOPMOST, 1)

    #prediction variables
    model_dict = pickle.load(open('./model.p', 'rb'))
    model = model_dict['model']
    labels_dict = {0: "A", 1: "B", 2: "C" , 3: "D", 4: "E", 5: 'F', 6: 'G', 7: 'H', 
                   8: 'I', 9: 'K', 10: 'L', 11: 'M', 12: 'N' , 13: 'O', 14: 'P', 
                   15: 'Q', 16: 'R', 17: 'S', 18: 'T', 19: 'U', 20: 'V', 21: 'W',
                   22: 'X', 23: 'Y'}                          

    while(True):
        success, img = cap.read()

        if img is None:
            print("Cannot open camera")
            exit()
        
        hands, img = detector.findHands(img)
        
        backg = np.ones_like(img, np.uint8)
        backg = backg * 255
        blended_img = cv.addWeighted(backg, 0.5, img, 0.5, 0)
        data_aux = []

        cv.putText(blended_img, "ASL Typing", (0, 30), cv.FONT_HERSHEY_PLAIN, 2, green, 2)

        if hands:
            temp_lmlist = hands[0]["lmList"]
            indexFinger = temp_lmlist[8][0], temp_lmlist[8][1]
            wrist = temp_lmlist[0][0], temp_lmlist[0][1]
            fingers = detector.fingersUp(hands[0])

            #closing asl typing
            if hands[0]["type"] == "Left":
                if (fingers == [0, 1, 0 , 0, 1] and wrist[1] > indexFinger[1]) and counter >= WB_DELAY:
                    return 0

            #for asl typing
            if hands[0]["type"] == "Right":
                lmlist = np.array(hands[0]["lmList"])
                for i in range(len(lmlist)):
                    x = lmlist[i][0]
                    y = lmlist[i][1]
                    data_aux.append(x)
                    data_aux.append(y)
                
                #prediction of the model
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])]
                # cv.putText(blended_img, predicted_character, (15,12), 
                #                     cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
                
                #adding the predicted character to the asl_text
                if temp_pred != predicted_character:
                    counter = 0
                    temp_pred = predicted_character
                else:
                    if counter > WB_DELAY:
                        asl_text += predicted_character
                        counter = 0

        #displaying the increasing text
        cv.rectangle(blended_img, (aslTextX, aslTextY-30), (aslTextX+(20*len(asl_text)), aslTextY+10), white, cv.FILLED)
        if not hands: temp_pred = ""           
        cv.putText(blended_img, asl_text+temp_pred,  (aslTextX, aslTextY), 
                                    cv.FONT_HERSHEY_DUPLEX, 1, black, 1, cv.LINE_AA)   
        c = cv.waitKey(1)
        img = cv.resize(blended_img, (screen_width,screen_height), interpolation = cv.INTER_CUBIC)
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
    detector = HandDetector(detectionCon=0.7, maxHands= 1)
    generateASL(cap, detector, 20)