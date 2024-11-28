from Constants import *
from utilFuncs import *
import pygame as pyg

class Button:
    def __init__(self, func, rect:pyg.Rect, label: str, font: pyg.font.Font, bgColor: pyg.Color, outlineColor: pyg.Color) -> None:
        self.func = func
        self.rect = rect
        self.label = label
        self.font = font
        self.bgColor = bgColor
        self.outlineColor = outlineColor
        self.isActive = False
        
    def Draw(self):
        if not self.isActive: return
        from Variables import mouseCoords # this has to be lazy imported to avoid a circular import
        self.bgColor = self.bgColor.hsla
        if self.rect.collidepoint(mouseCoords):
            self.bgColor[2] += 10
        pyg.draw.rect(WIN, self.bgColor, self.rect)
        pyg.draw.rect(WIN, self.outlineColor, self.rect, 1)
        DrawFont(self.label, self.font, self.outlineColor, self.rect.center, areCoordsCenter= True)
        
    def TryClick(self):
        from Variables import mouseCoords
        if self.rect.collidepoint(mouseCoords):
            self.func()