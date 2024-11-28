from Constants import *
from Button import Button

currentHeadCoords: list[int] = START_COORDS
snake: list[list[int]] = [START_COORDS]
apples: list[list[2,int]] = []
buttons: list[Button]
mouseCoords: tuple[int]

currentDirection: DIR = "0"
nextDirection: DIR = "0"

insertPressCount:int = 0
score:int = 0

showDbgInfo: bool = False
isAlive: bool = True
isPaused: bool = False
gameRunning: bool = True