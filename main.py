import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp

def main():
    cap = cv.VideoCapture(0)

    #camera not opened
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    cap.set(3, 1280) 
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.8, maxHands= 1)
    yellow = [0,255,255]
    red = [0,0,255]
    drawPoints = [[]]
    pointNum = -1
    drawCase = False

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
            fingers = detector.fingersUp(hands[0])

            if fingers == [0, 0, 0, 0 ,0]:
                drawPoints.clear()
                pointNum = -1

            if fingers == [0, 1, 1, 0 ,0]:
                cv.circle(img, indexFinger, 10, yellow, 2)
            
            if fingers == [0, 1, 0, 0 ,0]:
                cv.circle(img, indexFinger, 10, yellow, 2)
                if drawCase == False:
                    drawCase = True
                    pointNum = pointNum + 1
                    drawPoints.append([])
                drawPoints[pointNum].append(indexFinger)
            
            else:
                drawCase = False
        
        c = cv.waitKey(1)
        
        for i in range(len(drawPoints)):
            for j in range(len(drawPoints[i])):
                if j!=0:
                    cv.line(img, drawPoints[i][j-1], drawPoints[i][j], red, 12)
        
        cv.imshow("Image", cv.flip(img, 1))
        
        if c == 27:
            break
   
    cv.destroyAllWindows()
if __name__ == '__main__':
    main()


