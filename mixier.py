import pygame.mixer as pm
import time
import os
import glob
import random

projectPath = os.path.abspath(os.path.dirname(__file__))
musicFiles = glob.glob(projectPath + "/music/*")

def playMusic():
    random.shuffle(musicFiles)
    musicPath = musicFiles[0]
    pm.init()
    pm.music.load(musicPath)
    pm.music.play(1)
    time.sleep(3)
    pm.music.stop()
