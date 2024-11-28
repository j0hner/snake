from typing import Literal
import pygame as pyg
import random as rng
from Constants import *
from utilFuncs import *
from Variables import *

pyg.display.set_caption("Snake")

pyg.init()

def PlaceApple():
    choices = []
    for x in range(GAME_WIDTH//TILE_SIZE):
        for y in range(GAME_HEIGHT//TILE_SIZE):
            if not [x,y] in apples and not [x,y] in snake:
                choices.append([x,y])
    
    apples.append(rng.choice(choices))

def Reset():
    global currentHeadCoords, snake, apples, currentDirection, nextDirection, gameRunning, isAlive, score, isPaused
    
    currentHeadCoords = START_COORDS
    snake = [START_COORDS]
    apples = []
    PlaceApple()
    currentDirection = "0"
    nextDirection = "0"
    isAlive = True
    gameRunning = True # TODO: chabge when implementing menu
    isPaused = False
    score = 0

def Refresh():
    global currentHeadCoords
    WIN.fill(CLR_BLACK)
    
    if gameRunning: 
        if DRAW_GRID:
            for i in range(TILE_SIZE,GAME_WIDTH, TILE_SIZE):
                pyg.draw.line(WIN, CLR_GRAY, (i, 0 + TOP_OFFSET), (i, GAME_HEIGHT + TOP_OFFSET))
            
            for i in range(TOP_OFFSET, GAME_HEIGHT + TOP_OFFSET, TILE_SIZE):
                pyg.draw.line(WIN, CLR_GRAY, (0, i), (GAME_WIDTH, i))
            
        for apple in apples:
            rect = pyg.Rect(apple[0] * TILE_SIZE, apple[1] * TILE_SIZE + TOP_OFFSET, TILE_SIZE, TILE_SIZE)
            pyg.draw.circle(WIN, CLR_RED, rect.center, TILE_SIZE / 2)
            
        for i, part in enumerate(snake):
            rect = pyg.Rect(part[0] * TILE_SIZE, part[1] * TILE_SIZE + TOP_OFFSET, TILE_SIZE, TILE_SIZE)
            if i == 0 and len(snake) > 1:# Tail
                nextPart = snake[1]
                dx, dy = nextPart[0] - part[0], nextPart[1] - part[1]
                
                if dx == 1:  # Tail is pointing right
                    pyg.draw.rect(WIN, CLR_GREEN, rect, border_top_left_radius=10, border_bottom_left_radius=10)
                elif dx == -1:  # Tail is pointing left
                    pyg.draw.rect(WIN, CLR_GREEN, rect, border_top_right_radius=10, border_bottom_right_radius=10)
                elif dy == 1:  # Tail is pointing down
                    pyg.draw.rect(WIN, CLR_GREEN, rect, border_top_left_radius=10, border_top_right_radius=10)
                elif dy == -1:  # Tail is pointing up
                    pyg.draw.rect(WIN, CLR_GREEN, rect, border_bottom_left_radius=10, border_bottom_right_radius=10)
            elif i == len(snake) - 1: # Head
                
                
                headRadii = {
                    "d": {"border_bottom_left_radius": 10, "border_bottom_right_radius": 10},
                    "u": {"border_top_left_radius": 10, "border_top_right_radius": 10},
                    "l": {"border_top_left_radius": 10, "border_bottom_left_radius": 10},
                    "r": {"border_top_right_radius": 10, "border_bottom_right_radius": 10},
                    "0": {"border_top_right_radius": 10, "border_top_left_radius": 10, "border_bottom_right_radius": 10, "border_bottom_left_radius": 10},
                }
                if len(snake) > 1: pyg.draw.rect(WIN, CLR_GREEN, rect, **headRadii.get(currentDirection, {}))
                else: pyg.draw.rect(WIN, CLR_GREEN, rect, **headRadii.get("0", {}))
                
                # Add eyes
                eyeRadius = TILE_SIZE // 8
                eyeOffset = TILE_SIZE // 4
                if currentDirection == "u":
                    leftEye = (part[0] * TILE_SIZE + eyeOffset, part[1] * TILE_SIZE + eyeOffset + TOP_OFFSET)
                    rightEye = (part[0] * TILE_SIZE + TILE_SIZE - eyeOffset, part[1] * TILE_SIZE + eyeOffset + TOP_OFFSET)
                elif currentDirection == "d":
                    leftEye = (part[0] * TILE_SIZE + eyeOffset, part[1] * TILE_SIZE + TILE_SIZE - eyeOffset + TOP_OFFSET)
                    rightEye = (part[0] * TILE_SIZE + TILE_SIZE - eyeOffset, part[1] * TILE_SIZE + TILE_SIZE - eyeOffset + TOP_OFFSET)
                elif currentDirection == "r":
                    leftEye = (part[0] * TILE_SIZE + TILE_SIZE - eyeOffset, part[1] * TILE_SIZE + eyeOffset + TOP_OFFSET)
                    rightEye = (part[0] * TILE_SIZE + TILE_SIZE - eyeOffset, part[1] * TILE_SIZE + TILE_SIZE - eyeOffset + TOP_OFFSET)
                elif currentDirection == "l":
                    leftEye = (part[0] * TILE_SIZE + eyeOffset, part[1] * TILE_SIZE + eyeOffset + TOP_OFFSET)
                    rightEye = (part[0] * TILE_SIZE + eyeOffset, part[1] * TILE_SIZE + TILE_SIZE - eyeOffset + TOP_OFFSET)

                # Draw eyes
                if not currentDirection == "0": 
                    pyg.draw.circle(WIN, (255, 255, 255), leftEye, eyeRadius)
                    pyg.draw.circle(WIN, (255, 255, 255), rightEye, eyeRadius)
            else: # Body segments
                    
                    prevPart = snake[i - 1]
                    nextPart = snake[i + 1]
                    
                    # Determine if turning
                    if prevPart[0] != nextPart[0] and prevPart[1] != nextPart[1]:
                        if (prevPart[0] < part[0] and nextPart[1] > part[1]) or (nextPart[0] < part[0] and prevPart[1] > part[1]):  # Bottom-left turn
                            pyg.draw.rect(WIN, CLR_GREEN, rect, border_top_right_radius=10)
                        elif (prevPart[0] > part[0] and nextPart[1] > part[1]) or (nextPart[0] > part[0] and prevPart[1] > part[1]):  # Bottom-right turn
                            pyg.draw.rect(WIN, CLR_GREEN, rect, border_top_left_radius=10)
                        elif (prevPart[0] < part[0] and nextPart[1] < part[1]) or (nextPart[0] < part[0] and prevPart[1] < part[1]):  # Top-left turn
                            pyg.draw.rect(WIN, CLR_GREEN, rect, border_bottom_right_radius=10)
                        elif (prevPart[0] > part[0] and nextPart[1] < part[1]) or (nextPart[0] > part[0] and prevPart[1] < part[1]):  # Top-right turn
                            pyg.draw.rect(WIN, CLR_GREEN, rect, border_bottom_left_radius=10)
                    else:
                        pyg.draw.rect(WIN, CLR_GREEN, rect)
        
        if isPaused:
            WIN.blit(MakeOveraly("Paused", 130), (0,TOP_OFFSET))
    
    if not isAlive:
        WIN.blit(MakeOveraly("Game Over", 255, CLR_RED), (0,TOP_OFFSET))
        DrawFont(f"[space]", SMALL_FONT, CLR_WHITE, (GAME_WIDTH//2, GAME_HEIGHT//2), areCoordsCenter=True, yOffset = 20 + TOP_OFFSET)
    
    if gameRunning:
        # cover top offset 
        pyg.draw.rect(WIN, CLR_BLACK, pyg.Rect((0,0),(WIN_WIDTH, TOP_OFFSET)))
        pyg.draw.line(WIN, CLR_WHITE, (0, TOP_OFFSET), (WIN_WIDTH, TOP_OFFSET), 1)
        DrawFont(f"score: {score}", MEDIUM_FONT, CLR_WHITE, (3,5))
    
    if showDbgInfo:
        clr = (*CLR_WHITE, 90)
        DrawFont(f"Snake: {snake}", SMALL_FONT, clr, (0,1 + TOP_OFFSET))
        DrawFont(f"Apples: {apples}", SMALL_FONT, clr, (0,14 + TOP_OFFSET))
        DrawFont(f"FPS: {CLOCK.get_fps() :.4f}", SMALL_FONT, clr, (0,28 + TOP_OFFSET))
        DrawFont(f"Head: {currentHeadCoords}", SMALL_FONT, clr, (0,42 + TOP_OFFSET))
        DrawFont(f"Current direction: {currentDirection}", SMALL_FONT, clr, (0,56 + TOP_OFFSET))
        DrawFont(f"Next direction: {nextDirection}", SMALL_FONT, clr, (0,70 + TOP_OFFSET))

    pyg.display.update()

def Main():
    global currentDirection, currentHeadCoords, gameRunning, nextDirection, isAlive, score, mouseCoords, isPaused
    PlaceApple()
    run = True
    while run:
        mouseCoords = pyg.mouse.get_pos()
        
        if gameRunning and isAlive and not isPaused:
            if (currentDirection == "u" and nextDirection != "d") or \
            (currentDirection == "d" and nextDirection != "u") or \
            (currentDirection == "l" and nextDirection != "r") or \
            (currentDirection == "r" and nextDirection != "l") or \
            (currentDirection == "0" and nextDirection != "0"): currentDirection = nextDirection
            
            currentHeadCoords = snake[len(snake) - 1]
            match currentDirection:
                case "d": 
                    snake.append([currentHeadCoords[0], currentHeadCoords[1] + 1])
                case "u": 
                    snake.append([currentHeadCoords[0], currentHeadCoords[1] - 1])
                case "l": 
                    snake.append([currentHeadCoords[0] - 1, currentHeadCoords[1]])
                case "r": 
                    snake.append([currentHeadCoords[0] + 1, currentHeadCoords[1]])
                case "0": ...
            
            if not currentHeadCoords in apples and not len(snake) <= DEFAULT_SNAKE_LEN and not currentDirection == "0":
                snake.pop(0)
                
            if snake.count(currentHeadCoords) > 1 or GAME_WIDTH//TILE_SIZE <= currentHeadCoords[0] or currentHeadCoords[0] < 0 or GAME_HEIGHT//TILE_SIZE <= currentHeadCoords[1] or currentHeadCoords[1] < 0:
                isAlive = False
            
            if currentHeadCoords in apples: 
                apples.remove(currentHeadCoords)
                score += 1
                PlaceApple()
            
            pyg.time.delay(80)            
        
        Refresh()
        CLOCK.tick(60)
        
        # event handling
        for event in pyg.event.get():
            match event.type:
                case pyg.QUIT:
                    run = False
                case pyg.KEYDOWN:
                    # Buffer the next direction
                    match event.key:
                        case pyg.K_UP:
                            if not isPaused: nextDirection = "u"
                        case pyg.K_DOWN:
                            if not isPaused: nextDirection = "d"
                        case pyg.K_LEFT:
                            if not isPaused: nextDirection = "l"
                        case pyg.K_RIGHT:
                            if not isPaused: nextDirection = "r"
                        case pyg.K_ESCAPE:
                            if isAlive: isPaused = not isPaused
                        case pyg.K_INSERT:
                            global insertPressCount, showDbgInfo
                            insertPressCount += 1
                            if insertPressCount >= 3:
                                insertPressCount = 0
                                showDbgInfo = not showDbgInfo
                        case pyg.K_SPACE:
                            if not isAlive: 
                                Reset()
                                
                case pyg.MOUSEBUTTONUP:
                    for button in buttons:
                        if not button.isActive: continue
                        button.TryClick()
                            

if __name__ == "__main__":
    Main()