from __future__ import annotations
import cv2 as cv
from constants import WIDTH, HEIGHT, HORIZON
import utils

class Point:
    def __init__(self, x, y):
        self.x  = x
        self.y  = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def draw(self, image, radius = 3, color = (255, 255, 255)):
        cv.circle(image, (int(self.x), int(self.y)), radius, color)

    def toList(self):
        return [int(self.x), int(self.y)]

class Line:
    def __init__(self, startPoint: Point, endPoint : Point = None, m: int = None):
        self.startPoint = startPoint
        if endPoint:
            self.endPoint = endPoint
        
            # y = mx + q
            self.m = (startPoint.y - endPoint.y)/(startPoint.x - endPoint.x)
            self.q = startPoint.y - self.m * startPoint.x
        elif m:
            self.m = m
            self.q = startPoint.y - self.m * startPoint.x

            # on right border of image
            self.endPoint = Point(WIDTH, self._y(WIDTH))
        else:
            raise "You need either a endPoint or a m to initialise a line"


    def _y(self,x):
        return self.m * x + self.q

    def _x(self, y):
        return (y - self.q) / self.m

    def _debug(self, image):
        cv.line(image, 
                (int(self._x(HEIGHT)), HEIGHT), 
                (WIDTH, int(self._y(WIDTH))), 
                (255, 0, 0), 
                thickness = 1)

    def draw(self, image, color = (100, 100, 100), thickness = 1):
        cv.line(image, 
                (int(self.startPoint.x), int(self.startPoint.y)), 
                (int(self.endPoint.x), int(self.endPoint.y)), 
                color, 
                thickness = thickness)

    def drawBelowHorizon(self, image, color = (100, 100, 100), thickness = 1):
        cv.line(image, 
                (int(self.startPoint.x), int(self.startPoint.y)), 
                (int(self._x(HORIZON)), HORIZON), 
                color, 
                thickness = thickness)


    def intersect(self, otherLine: Line) -> Point:
        x = (otherLine.q - self.q)/(self.m - otherLine.m)
        y = x * self.m + self.q
        return Point(x, y)

class RotatingLine():

    def __init__(self, startRotation, startTime, center, maxRotation = WIDTH):
        self.rotation = startRotation
        self.startTime = startTime
        self.center = center
        self.color = utils.randomColor()
        #self.thickness = utils.randomThickness()
        self.thickness = 1

    def __str__(self):
        return "RotatingLine: startTime {}".format(self.startTime)

    def draw(self, frameImage, ts):
        if ts >= self.startTime and self.rotation < WIDTH:
            self.rotation += 10
            line = Line(Point(self.rotation, HEIGHT), self.center)
            line.drawBelowHorizon(frameImage, color = self.color, thickness=self.thickness)

