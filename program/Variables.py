from Constants import *

showDbgInfo: bool = False
isAlive: bool = True
isPaused: bool = False
gameRunning: bool = False
isControlsWASD:bool = False
creditsShown:bool = False
isInMenu = True

currentHeadCoords: list[int] = START_COORDS
snake: list[list[int]] = [START_COORDS]
apples: list[list[2,int]] = []

mouseCoords: tuple[int]

currentDirection: DIR = "0"
nextDirection: DIR = "0"

insertPressCount:int = 0
score:int = 0
