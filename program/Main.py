from typing import Literal
import pygame as pyg
import random as rng
from Constants import *
from utilFuncs import *
import Variables as vars
from Button import buttons

pyg.display.set_caption("Snake")

pyg.init()

def PlaceApple():
    choices = []
    for x in range(GAME_WIDTH//TILE_SIZE):
        for y in range(GAME_HEIGHT//TILE_SIZE):
            if not [x,y] in vars.apples and not [x,y] in vars.snake:
                choices.append([x,y])
    
    vars.apples.append(rng.choice(choices))

def Reset(toMenu:bool = False):
    vars.currentHeadCoords = START_COORDS
    vars.snake = [START_COORDS]
    vars.apples = []
    PlaceApple()
    vars.currentDirection = "0"
    vars.nextDirection = "0"
    vars.isAlive = True
    vars.isPaused = False
    vars.score = 0
    vars.gameRunning = not toMenu
    
    if toMenu:
        vars.isInMenu = True
        SetBtnGroupState("menu", True)

def Refresh():
    WIN.fill(CLR_BLACK)
    
    if vars.gameRunning: 
        if DRAW_GRID:
            for i in range(TILE_SIZE,GAME_WIDTH, TILE_SIZE):
                pyg.draw.line(WIN, CLR_GRAY, (i, 0 + TOP_OFFSET), (i, GAME_HEIGHT + TOP_OFFSET))
            
            for i in range(TOP_OFFSET, GAME_HEIGHT + TOP_OFFSET, TILE_SIZE):
                pyg.draw.line(WIN, CLR_GRAY, (0, i), (GAME_WIDTH, i))
            
        for apple in vars.apples:
            rect = pyg.Rect(apple[0] * TILE_SIZE, apple[1] * TILE_SIZE + TOP_OFFSET, TILE_SIZE, TILE_SIZE)
            pyg.draw.circle(WIN, CLR_RED, rect.center, TILE_SIZE / 2)
            
        for i, part in enumerate(vars.snake):
            rect = pyg.Rect(part[0] * TILE_SIZE, part[1] * TILE_SIZE + TOP_OFFSET, TILE_SIZE, TILE_SIZE)
            if i == 0 and len(vars.snake) > 1:# Tail
                nextPart = vars.snake[1]
                dx, dy = nextPart[0] - part[0], nextPart[1] - part[1]
                
                if dx == 1:  # Tail is pointing right
                    pyg.draw.rect(WIN, CLR_GREEN, rect, border_top_left_radius=10, border_bottom_left_radius=10)
                elif dx == -1:  # Tail is pointing left
                    pyg.draw.rect(WIN, CLR_GREEN, rect, border_top_right_radius=10, border_bottom_right_radius=10)
                elif dy == 1:  # Tail is pointing down
                    pyg.draw.rect(WIN, CLR_GREEN, rect, border_top_left_radius=10, border_top_right_radius=10)
                elif dy == -1:  # Tail is pointing up
                    pyg.draw.rect(WIN, CLR_GREEN, rect, border_bottom_left_radius=10, border_bottom_right_radius=10)
            elif i == len(vars.snake) - 1: # Head
                
                
                headRadii = {
                    "d": {"border_bottom_left_radius": 10, "border_bottom_right_radius": 10},
                    "u": {"border_top_left_radius": 10, "border_top_right_radius": 10},
                    "l": {"border_top_left_radius": 10, "border_bottom_left_radius": 10},
                    "r": {"border_top_right_radius": 10, "border_bottom_right_radius": 10},
                    "0": {"border_top_right_radius": 10, "border_top_left_radius": 10, "border_bottom_right_radius": 10, "border_bottom_left_radius": 10},
                }
                if len(vars.snake) > 1: pyg.draw.rect(WIN, CLR_GREEN, rect, **headRadii.get(vars.currentDirection, {}))
                else: pyg.draw.rect(WIN, CLR_GREEN, rect, **headRadii.get("0", {}))
                
                # Add eyes
                eyeRadius = TILE_SIZE // 8
                eyeOffset = TILE_SIZE // 4
                if vars.currentDirection == "u":
                    leftEye = (part[0] * TILE_SIZE + eyeOffset, part[1] * TILE_SIZE + eyeOffset + TOP_OFFSET)
                    rightEye = (part[0] * TILE_SIZE + TILE_SIZE - eyeOffset, part[1] * TILE_SIZE + eyeOffset + TOP_OFFSET)
                elif vars.currentDirection == "d":
                    leftEye = (part[0] * TILE_SIZE + eyeOffset, part[1] * TILE_SIZE + TILE_SIZE - eyeOffset + TOP_OFFSET)
                    rightEye = (part[0] * TILE_SIZE + TILE_SIZE - eyeOffset, part[1] * TILE_SIZE + TILE_SIZE - eyeOffset + TOP_OFFSET)
                elif vars.currentDirection == "r":
                    leftEye = (part[0] * TILE_SIZE + TILE_SIZE - eyeOffset, part[1] * TILE_SIZE + eyeOffset + TOP_OFFSET)
                    rightEye = (part[0] * TILE_SIZE + TILE_SIZE - eyeOffset, part[1] * TILE_SIZE + TILE_SIZE - eyeOffset + TOP_OFFSET)
                elif vars.currentDirection == "l":
                    leftEye = (part[0] * TILE_SIZE + eyeOffset, part[1] * TILE_SIZE + eyeOffset + TOP_OFFSET)
                    rightEye = (part[0] * TILE_SIZE + eyeOffset, part[1] * TILE_SIZE + TILE_SIZE - eyeOffset + TOP_OFFSET)

                # Draw eyes
                if not vars.currentDirection == "0": 
                    pyg.draw.circle(WIN, (255, 255, 255), leftEye, eyeRadius)
                    pyg.draw.circle(WIN, (255, 255, 255), rightEye, eyeRadius)
            else: # Body segments
                    
                    prevPart = vars.snake[i - 1]
                    nextPart = vars.snake[i + 1]
                    
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
        
        if vars.isPaused:
            WIN.blit(MakeOveraly("Paused", 130), (0,TOP_OFFSET))
    
        if not vars.isAlive:
            WIN.blit(MakeOveraly("Game Over", 255, CLR_RED), (0,TOP_OFFSET))
            DrawFont(f"[space] continue", SMALL_FONT, CLR_WHITE, WIN_CENTER, areCoordsCenter=True, offset=(0,15 + TOP_OFFSET))
            DrawFont(f"[esc] menu", SMALL_FONT, CLR_WHITE, WIN_CENTER, areCoordsCenter=True, offset=(0,30 + TOP_OFFSET))
        
        # cover top offset 
        pyg.draw.rect(WIN, CLR_BLACK, pyg.Rect((0,0),(WIN_WIDTH, TOP_OFFSET)))
        pyg.draw.line(WIN, CLR_WHITE, (0, TOP_OFFSET), (WIN_WIDTH, TOP_OFFSET), 1)
        DrawFont(f"score: {vars.score}", MEDIUM_FONT, CLR_WHITE, (3,5))

    if vars.isInMenu:
        DrawFont("S N A K E", BIG_FONT, CLR_WHITE, WIN_CENTER, offset=(0,-200), areCoordsCenter= True)
    
    for btn in buttons:
        if not btn.isActive: continue
        btn.Draw()
    
    if vars.showDbgInfo:
        clr = (*CLR_WHITE, 90)
        DrawFont(f"vars.snake: {vars.snake}", SMALL_FONT, clr, (0,1 + TOP_OFFSET))
        DrawFont(f"apples: {vars.apples}", SMALL_FONT, clr, (0,14 + TOP_OFFSET))
        DrawFont(f"FPS: {CLOCK.get_fps() :.4f}", SMALL_FONT, clr, (0,28 + TOP_OFFSET))
        DrawFont(f"Head: {vars.currentHeadCoords}", SMALL_FONT, clr, (0,42 + TOP_OFFSET))
        DrawFont(f"Current direction: {vars.currentDirection}", SMALL_FONT, clr, (0,56 + TOP_OFFSET))
        DrawFont(f"Next direction: {vars.nextDirection}", SMALL_FONT, clr, (0,70 + TOP_OFFSET))
        DrawFont(f"isControlsWASD: {vars.isControlsWASD}", SMALL_FONT, clr, (0,84 + TOP_OFFSET))
        DrawFont(f"gameRunning: {vars.gameRunning}", SMALL_FONT, clr, (0,98 + TOP_OFFSET))

    pyg.display.update()

def Main():
    PlaceApple()
    run = True
    while run:        
        if vars.gameRunning and vars.isAlive and not vars.isPaused:
            if (vars.currentDirection == "u" and vars.nextDirection != "d") or \
            (vars.currentDirection == "d" and vars.nextDirection != "u") or \
            (vars.currentDirection == "l" and vars.nextDirection != "r") or \
            (vars.currentDirection == "r" and vars.nextDirection != "l") or \
            (vars.currentDirection == "0" and vars.nextDirection != "0"): vars.currentDirection = vars.nextDirection
            
            vars.currentHeadCoords = vars.snake[len(vars.snake) - 1]
            match vars.currentDirection:
                case "d": 
                    vars.snake.append([vars.currentHeadCoords[0], vars.currentHeadCoords[1] + 1])
                case "u": 
                    vars.snake.append([vars.currentHeadCoords[0], vars.currentHeadCoords[1] - 1])
                case "l": 
                    vars.snake.append([vars.currentHeadCoords[0] - 1, vars.currentHeadCoords[1]])
                case "r": 
                    vars.snake.append([vars.currentHeadCoords[0] + 1, vars.currentHeadCoords[1]])
                case "0": ...
            
            if not vars.currentHeadCoords in vars.apples and not len(vars.snake) <= DEFAULT_SNAKE_LEN and not vars.currentDirection == "0":
                vars.snake.pop(0)
                
            if vars.snake.count(vars.currentHeadCoords) > 1 or GAME_WIDTH//TILE_SIZE <= vars.currentHeadCoords[0] or vars.currentHeadCoords[0] < 0 or GAME_HEIGHT//TILE_SIZE <= vars.currentHeadCoords[1] or vars.currentHeadCoords[1] < 0:
                vars.isAlive = False
            
            if vars.currentHeadCoords in vars.apples: 
                vars.apples.remove(vars.currentHeadCoords)
                vars.score += 1
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
                    global keyMap
                    
                    keyMap = [pyg.K_w, pyg.K_s, pyg.K_a, pyg.K_d] if vars.isControlsWASD else [pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT]
                    
                    #region controls
                    if event.key == keyMap[0]:
                        if not vars.isPaused:
                            vars.nextDirection = "u"
                    elif event.key == keyMap[1]:
                        if not vars.isPaused:
                            vars.nextDirection = "d"
                    elif event.key == keyMap[2]:
                        if not vars.isPaused:
                            vars.nextDirection = "l"
                    elif event.key == keyMap[3]:
                        if not vars.isPaused:
                            vars.nextDirection = "r"
                            if not vars.isPaused: vars.nextDirection = "r"
                    #endregion
                    
                    elif event.key == pyg.K_ESCAPE:
                            if vars.isAlive: vars.isPaused = not vars.isPaused
                            else: Reset(True)
                    elif event.key == pyg.K_INSERT:
                            vars.insertPressCount += 1
                            if vars.insertPressCount >= 3:
                                vars.insertPressCount = 0
                                vars.showDbgInfo = not vars.showDbgInfo
                                SetBtnGroupState("dbg", vars.showDbgInfo)
                    elif event.key == pyg.K_SPACE:
                            if not vars.isAlive: 
                                Reset()
                                
                case pyg.MOUSEBUTTONUP:
                    for button in buttons:
                        if not button.isActive: continue
                        button.TryClick(globals())
                            
if __name__ == "__main__":
    Main()