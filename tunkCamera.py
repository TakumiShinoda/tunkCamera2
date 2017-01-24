import pygame.mixer
import cv2
import RPi.GPIO as GPIO
import numpy as np
import time
import os
import glob
import random

forwardPinR = 27
forwardPinL = 23
backPinR = 17
backPinL = 24

projectPath = os.path.abspath(os.path.dirname(__file__))
cascade = cv2.CascadeClassifier(projectPath + "/xml/cascade.xml")
musicFiles = glob.glob(projectPath + "/music/*")

turn_time = 3
frame_degree = 4
accuracy = 4
lower = np.array([0,50,50])
upper = np.array([15,255,255])

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(forwardPinR, GPIO.OUT)
    GPIO.setup(forwardPinL, GPIO.OUT)
    GPIO.setup(backPinR, GPIO.OUT)
    GPIO.setup(backPinL, GPIO.OUT)

def display(frame):
    cv2.imshow("frame",frame)

def playMusic():
    random.shuffle(musicFiles)
    musicPath = musicFiles[0]
    pygame.mixer.init()
    pygame.mixer.music.load(musicPath)
    pygame.mixer.music.play(1)
    time.sleep(3)
    pygame.mixer.music.stop()

def goRight():
    GPIO.output(forwardPinR, True)
    GPIO.output(backPinL, True)
    time.sleep(turn_time)
    GPIO.output(forwardPinR, False)
    GPIO.output(backPinL, False)

def goLeft():
    GPIO.output(forwardPinL, True)
    GPIO.output(backPinR, True)
    time.sleep(turn_time)
    GPIO.output(forwardPinL, False)
    GPIO.output(backPinR, False)

def frame_init():
    cap = cv2.VideoCapture(0)
    i = 0

    while i < 10:
        ret,frame = cap.read()
        i += 1

    return ret,frame
    
def detection(frame):
    count = 0
    size = (frame.shape[1] / frame_degree,frame.shape[0] / frame_degree)
    frame = cv2.resize(frame,size)
    pixels = frame.shape[0] * frame.shape[1]
    
    frameHSV = cv2.cvtColor(frame,cv2.cv.CV_BGR2HSV)
    
    frameHSV = cv2.inRange(frameHSV,lower,upper)
    min_pixels = pixels / accuracy
    
    for content in frameHSV:
        count += np.count_nonzero(content)

    if count > min_pixels: 
        return count
    else:
        return 0


setupGPIO()
while True:
    left = 0
    right = 0
    ret,frame = frame_init()
         
    h = frame.shape[0]
    w = frame.shape[1]

    if ret == True:
        frame_left = frame[0:h,w / 2:w]
        frame_right = frame[0:h,0:w / 2]

    display(cv2.inRange(cv2.cvtColor(cv2.medianBlur(cv2.resize(frame,(w / 2,h/2)),5),cv2.cv.CV_BGR2HSV),lower,upper))

    left = detection(frame_left)
    right = detection(frame_right)
    
    if left > right:
        print("left")
        goLeft()
        playMusic()
    elif left < right:
        print("right")
        goRight()
        playMusic()
        
    cv2.waitKey(1)
