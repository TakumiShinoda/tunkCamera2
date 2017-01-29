import cv2
import numpy as np
import controller as ctr
import atexit

frame_degree = 4
smooth_degree = 5
accuracy = 4
lower = np.array([0,50,50])
upper = np.array([15,255,255])

def done_all():
    ctr.releaseGPIO()

def display(frame):
    cv2.imshow("frame",frame)

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
    min_pixels = pixels / accuracy
    
    frame_hsv = cv2.cvtColor(frame,cv2.cv.CV_BGR2HSV)
    frame_thres = cv2.inRange(frame_hsv,lower,upper)
    
    for content in frame_thres:
        count += np.count_nonzero(content)

    if count > min_pixels: 
        return count
    else:
        return 0


ctr.setupGPIO()
while True:
    left = 0
    right = 0
    ret,frame = frame_init()
         
    h = frame.shape[0]
    w = frame.shape[1]
    frame_left = frame[0:h,w / 2:w]
    frame_right = frame[0:h,0:w / 2]

    left = detection(frame_left)
    right = detection(frame_right)
    
    if left > right:
        print("left")
        ctr.goLeft()
    elif left < right:
        print("right")
        ctr.goRight()

    cv2.waitKey(1)
