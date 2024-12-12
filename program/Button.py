from Constants import *
import Variables as vars
from utilFuncs import *
import pygame as pyg

class Button:
    def __init__(self, func, rect:pyg.Rect, label: str, font: pyg.font.Font, bgColor: pyg.Color, outlineColor: pyg.Color, group:str, isActive:bool = True,  offset:tuple[int, int] = [0,0]) -> None:
        self.func = func
        self.rect = rect
        self.label = label
        self.font = font
        self.defaultBgColor = bgColor
        self.bgColor = self.defaultBgColor
        self.outlineColor = outlineColor
        self.isActive = isActive
        self.offset = offset
        self.group = group
        
        self.rect.topleft = addLists(self.rect.topleft, self.offset)
        
    def Draw(self):
        if not self.isActive: return
        if self.rect.collidepoint(pyg.mouse.get_pos()):
            self.bgColor = CLR_GRAY
        else: 
            self.bgColor = self.defaultBgColor
        pyg.draw.rect(WIN, self.bgColor, self.rect)
        pyg.draw.rect(WIN, self.outlineColor, self.rect, 1)
        DrawFont(self.label, self.font, self.outlineColor, self.rect.center, areCoordsCenter= True, )
        
    def TryClick(self, context:dict):
        if self.rect.collidepoint(pyg.mouse.get_pos()):
            try:
                self.func()
            except:
                # print(context)
                exec(self.func, {**context, "self":self})

def BtnPlay():
    vars.isInMenu = False
    vars.gameRunning = True
    SetBtnGroupState("menu", False)

def BtnControls():
    vars.isControlsWASD = not vars.isControlsWASD
    buttons[1].label = f"Controls: {"WASD" if vars.isControlsWASD else "arrows"}"
    
def BtnCredits():
    vars.isInMenu = False
    SetBtnGroupState("menu", False)
    vars.creditsShown = True
    SetBtnGroupState("credits", True)

def BtnUnstuck():
    vars.currentHeadCoords = START_COORDS
    vars.snake = [START_COORDS]
    vars.apples = []
    vars.currentDirection = "0"
    vars.nextDirection = "0"
    vars.isAlive = True
    vars.isPaused = False
    vars.score = 0
    vars.gameRunning = False
    
    SetBtnGroupState("*", False)
    SetBtnGroupState("menu", True)
    SetBtnGroupState("dbg", True)

def BtnCreditsBack():
    vars.isInMenu = True
    SetBtnGroupState("menu", True)
    vars.creditsShown = False
    SetBtnGroupState("credits", False)

buttons: list[Button] = [Button(BtnPlay, pyg.Rect((WIN_CENTER[0] - 100, WIN_CENTER[1] - 25),(200,50)), "Play", SMALL_FONT, CLR_BLACK, CLR_WHITE, "menu", offset=[0,-55]),
                         Button(BtnControls, pyg.Rect((WIN_CENTER[0] - 100, WIN_CENTER[1] - 25),(200,50)), f"Controls: {"WASD" if vars.isControlsWASD else "arrows"}", SMALL_FONT, CLR_BLACK, CLR_WHITE, "menu"),
                         Button(BtnCredits, pyg.Rect((WIN_CENTER[0] - 100, WIN_CENTER[1] - 25),(200,50)), "Credits", SMALL_FONT, CLR_BLACK, CLR_WHITE, "menu", offset=[0,55]),
                         Button(BtnUnstuck, pyg.Rect((0,0),(100,20)), "unstuck", SMALL_FONT, CLR_BLACK, CLR_WHITE, "dbg", False),
                         Button(BtnCredits, pyg.Rect((WIN_CENTER[0] - 100, WIN_CENTER[1] - 25),(200,50)), "Credits", SMALL_FONT, CLR_BLACK, CLR_WHITE, "menu", offset=[0,55]),
                         Button(BtnCreditsBack, pyg.Rect((WIN_CENTER[0] - 100, WIN_CENTER[1] - 25),(200,50)), "Back", SMALL_FONT, CLR_BLACK, CLR_WHITE, "credits", offset=[0,55], isActive=False)

]