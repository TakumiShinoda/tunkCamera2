import RPi.GPIO as GPIO
import mixier as mx
import time

turn_time = 1
alertPin = 21
forwardPinR = 27
forwardPinL = 23
backPinR = 17
backPinL = 24

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(alertPin, GPIO.OUT)
    GPIO.setup(forwardPinR, GPIO.OUT)
    GPIO.setup(forwardPinL, GPIO.OUT)
    GPIO.setup(backPinR, GPIO.OUT)
    GPIO.setup(backPinL, GPIO.OUT)
    init_alert()

def releaseGPIO():
    GPIO.output(alertPin, False)
    GPIO.output(forwardPinR, False)
    GPIO.output(backPinL, False)
    GPIO.output(forwardPinL, False)
    GPIO.output(backPinR, False)
    
def init_alert():
    GPIO.output(alertPin, True)
    
def goLeft():
    GPIO.output(forwardPinR, True)
    GPIO.output(backPinL, True)
    time.sleep(turn_time)
    GPIO.output(forwardPinR, False)
    GPIO.output(backPinL, False)
    mx.playMusic()

def goRight():
    GPIO.output(forwardPinL, True)
    GPIO.output(backPinR, True)
    time.sleep(turn_time)
    GPIO.output(forwardPinL, False)
    GPIO.output(backPinR, False)
    mx.playMusic()
