import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import whiteboard as wh

def main():
    cap = cv.VideoCapture(0)

    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    cap.set(3, 1280) 
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.3, maxHands= 1)
    yellow = [0,255,255]
    red = [0,0,255]
    drawPoints = [[]]                       #drawPoints array of array to store multiple points of the line
    pointNum = -1
    drawCase = False
    wBoard = False
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
                counter = wh.generateWhiteBoard(cap,detector)
            

            #if all fingers are closed then clear the screen
            elif fingers == [0, 0, 0, 0 ,0]:
                drawPoints.clear()
                pointNum = -1

            #if 2 fingers are open then draw a circle on the index finger
            elif fingers == [0, 1, 1, 0 ,0] and  wrist[1] > indexFinger[1]:
                cv.circle(img, indexFinger, 10, yellow, 2)
            
            #if index finger is open then draw a line
            elif fingers == [0, 1, 0, 0 ,0] and  wrist[1] > indexFinger[1]:
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
        
        #drawing the lines
        for i in range(len(drawPoints)):
            for j in range(len(drawPoints[i])):
                if j!=0:
                    cv.line(img, drawPoints[i][j-1], drawPoints[i][j], red, 12)
        
        cv.imshow("Image", cv.flip(img, 1))
        counter += 1
        print(counter)
        
        if c == 27:
            break
    
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()


