import cv2 as cv
import numpy as np
from Line import Line, Point
from constants import WIDTH, HEIGHT, HORIZON
import utils


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

for i in [600, 700, 800, 900, 1000, WIDTH]:
    k3 = Line(Point(i, HEIGHT), center)
    k3.drawBelowHorizon(fixedImage, color = utils.randomColor(), thickness=1)






cv.imshow('image', fixedImage)
cv.waitKey(0)
