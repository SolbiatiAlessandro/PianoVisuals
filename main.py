import cv2 as cv
import numpy as np
from Line import Line, Point, RotatingLine
import constants
from constants import WIDTH, HEIGHT, HORIZON
import utils
from random import random

fourcc = cv.VideoWriter_fourcc(*'MP4V')
video = cv.VideoWriter('./AlexMozartBackground.mp4', fourcc, float(constants.FPS), (constants.WIDTH, constants.HEIGHT))

fixedImage = np.full((HEIGHT,WIDTH,3), (172,170,164), dtype='uint8')

# horizon
horizon = Line(Point(0, HORIZON), Point(WIDTH, HORIZON))
horizon.draw(fixedImage, color=(0,0,0), thickness=2)
# 3 left to right fixedImage lines

keyboardClose = Line(Point(400, HEIGHT), Point(865, HORIZON))
keyboardFar = Line(Point(510, HEIGHT), Point(875, HORIZON))

keyboardClose.draw(fixedImage, color = (128, 128, 128), thickness = 2)
#keyboardClose._debug(fixedImage)
keyboardFar.draw(fixedImage, color = (128, 128, 128), thickness = 2)
#keyboardFar._debug(fixedImage)

center = keyboardClose.intersect(keyboardFar)
center.draw(fixedImage)

k2 = Line(Point(550, HEIGHT), center)
k2.drawBelowHorizon(fixedImage)

pts =np.array([
    keyboardClose.startPoint.toList(),
    k2.startPoint.toList(),
    k2.intersect(horizon).toList(),
    keyboardClose.endPoint.toList()])
cv.fillPoly(fixedImage, pts=np.int32([pts]), color=(248,244,236))

movieLenghtSeconds = 30
linesPerSec = 10
rotatingLines = [RotatingLine(550, i / linesPerSec, center) 
        for i in range(movieLenghtSeconds * linesPerSec) if random() > 0.5]
for r in rotatingLines: print(r)

for ts in range(constants.FPS * movieLenghtSeconds):
    frameImage = np.copy(fixedImage)
    for r in rotatingLines:
        ts_seconds = ts / constants.FPS
        r.draw(frameImage, ts_seconds)
    video.write(frameImage)

video.release()

"""
cv.imshow('image', fixedImage)
cv.waitKey(0)
"""
