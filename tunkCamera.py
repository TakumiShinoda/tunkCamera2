import pygame.mixer
import cv2
import RPi.GPIO as GPIO
import time
import os

forwardPinR = 27
forwardPinL = 23
backPinR = 17
backPinL = 24

projectPath = os.path.abspath(os.path.dirname(__file__))
cascade_path = projectPath + "/xml/cascade.xml"
cascade = cv2.CascadeClassifier(cascade_path)
color = (255, 255, 255)
cap = cv2.VideoCapture(0)
minsize = 80

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(forwardPinR, GPIO.OUT)
    GPIO.setup(forwardPinL, GPIO.OUT)
    GPIO.setup(backPinR, GPIO.OUT)
    GPIO.setup(backPinL, GPIO.OUT)

def display(frame):
    cv2.imshow("frame",frame)

def playMusic():
    pygame.mixer.init()
    pygame.mixer.music.load(projectPath + "/music/dog.mp3")
    pygame.mixer.music.play(1)
    time.sleep(3)
    pygame.mixer.music.stop()

def goRight():
    GPIO.output(forwardPinR, True)
    GPIO.output(backPinL, True)
    time.sleep(1)
    GPIO.output(forwardPinR, False)
    GPIO.output(backPinL, False)

def goLeft():
    GPIO.output(forwardPinL, True)
    GPIO.output(backPinR, True)
    time.sleep(1)
    GPIO.output(forwardPinL, False)
    GPIO.output(backPinR, False)

def colorDetect(rect,frame):
    detectedRect = []
    
    for colorRect in rect:
        cx = colorRect[0] + (colorRect[2] / 2)
        cy = colorRect[1] + (colorRect[2] / 2)
        frameSmooth = cv2.medianBlur(frame,7);
        frameHSV = cv2.cvtColor(frameSmooth,cv2.cv.CV_BGR2HSV)
        h = frameHSV[cy][cx][0]
        s = frameHSV[cy][cx][1]
        v = frameHSV[cy][cx][2]

        if h >= 15 and s >= 50 and s <= 255 and v >= 50 and v <= 255:
            detectedRect.append([colorRect[0],colorRect[1],colorRect[2],colorRect[3]])

    return detectedRect

def detection():
    while True:
        left = 0
        right = 0
        lastRect = []
        ret,frame = cap.read()
        image_gray = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
        rect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=3, minSize=(minsize,minsize))

        lastRect = colorDetect(rect,frame)

        if len(lastRect) > 0:
            for handRect in lastRect:
                cv2.rectangle(frame, tuple((handRect[0],handRect[1])),tuple((handRect[0]+handRect[2],handRect[1]+handRect[2])), color, thickness=2)
                center = handRect[0] + (handRect[2] / 2)

                if center > frame.shape[1] / 2:
                    left += 1
                else:
                    right += 1

        if left > right:
	    print("left")
            goLeft()
	    playMusic()
        elif left < right:
	    print("right")
            goRight()
            playMusic()

        display(frame)        
        cv2.waitKey(1)

setupGPIO()
detection()
