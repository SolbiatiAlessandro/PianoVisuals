from random import randint, random

def randomColor(): return (randint(0, 255), randint(0, 255), randint(0, 255))
def randomThickness(): return int(random() * 5) + 1
