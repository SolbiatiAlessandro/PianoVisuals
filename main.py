import cv2 as cv
import numpy as np
from Line import Line, Point, RotatingLine
import constants
from constants import WIDTH, HEIGHT, HORIZON
import utils
from random import random


######################
# GENERATE FIXED IMAGE

BACKGROUND_COLOR = 170
fixedImage = np.full((HEIGHT,WIDTH,3), (BACKGROUND_COLOR,BACKGROUND_COLOR,BACKGROUND_COLOR), dtype='uint8')
horizon_color = 100

# horizon
horizon = Line(Point(0, HORIZON), Point(WIDTH, HORIZON))
horizon.draw(fixedImage, color=(horizon_color,horizon_color,horizon_color), thickness=2)
for i in range(horizon_color, BACKGROUND_COLOR ):
    gradient = int((i - horizon_color) / 2)
    _horizon = Line(Point(0, HORIZON + gradient), 
            Point(WIDTH, HORIZON + gradient))
    _horizon.draw(fixedImage, color=(i,i,i), thickness=1)

# 3 left to right fixedImage lines

keyboardClose = Line(Point(400, HEIGHT), Point(865, HORIZON))
keyboardFar = Line(Point(510, HEIGHT), Point(875, HORIZON))

keyboardClose.draw(fixedImage, color = (128, 128, 128), thickness = 2)
#keyboardClose._debug(fixedImage)
keyboardFar.draw(fixedImage, color = (128, 128, 128), thickness = 2)
#keyboardFar._debug(fixedImage)

center = keyboardClose.intersect(keyboardFar)
#center.draw(fixedImage)

k2 = Line(Point(550, HEIGHT), center)
k2.drawBelowHorizon(fixedImage)

pts =np.array([
    keyboardClose.startPoint.toList(),
    k2.startPoint.toList(),
    k2.intersect(horizon).toList(),
    keyboardClose.endPoint.toList()])
cv.fillPoly(fixedImage, pts=np.int32([pts]), color=(248,244,236))

##############
# PROCESS AUDIO

import Audio
splitsPerSecond = 8
audioSplits=Audio.rmsSplits("mozart17jan.wav", splitsPerSecond)
audioLengthSecond = len(audioSplits) / splitsPerSecond  

#mapping line thickness 6 -> max intensity, 1 -> min intensity (avg)
maxRMS = max(audioSplits)
minRMS = (sum(audioSplits) / len(audioSplits)) 
maxThickness = 7
def rmsToThicnkess(rms):
    return max(1, int((rms / (maxRMS - minRMS)) * (maxThickness)))
    

##############
# GENERATE MOVIE

fourcc = cv.VideoWriter_fourcc(*'MP4V')
video = cv.VideoWriter('./AlexMozartBackground.mp4', fourcc, float(constants.FPS), (constants.WIDTH, constants.HEIGHT))

movieLenghtSeconds = audioLengthSecond


rotatingLines, flyingLines = [], []
for i, rms in enumerate(audioSplits):
    if rms > minRMS:
        r = RotatingLine(
            550, 
            i / splitsPerSecond, 
            center, 
            thickness=rmsToThicnkess(rms),
            rms=rms)
        rotatingLines.append(r)
        print(r)
    else:
        print("skipping "+str(rms))
print(len(rotatingLines))
print(len(audioSplits))


for ts in range(int(constants.FPS * movieLenghtSeconds)):
    frameImage = np.copy(fixedImage)
    for r in rotatingLines:
        ts_seconds = ts / constants.FPS
        r.draw(frameImage, ts_seconds)
        if (r.rotation >= WIDTH):
            f = r.generateFlyingLine()
            if f: flyingLines.append(f)
    for f in flyingLines:
        f.draw(frameImage, ts)

    video.write(frameImage)

video.release()

"""
cv.imshow('image', fixedImage)
cv.waitKey(0)
"""
