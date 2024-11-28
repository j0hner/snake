from Constants import *
import pygame as pyg

def addLists(list1: list[int], list2: list[int]) -> list:
    ret = []
    for i, j in zip(list1, list2):
        ret.append(i + j)
    return ret

def DrawFont(text:str, font:pyg.font.Font, color:tuple[int] | list[int], pos: tuple[int], surface:pyg.Surface = WIN, areCoordsCenter: bool = False, xOffset: int = 0, yOffset:int = 0):
        textSurface = font.render(text, True, color)
        if len(color) > 3: textSurface.set_alpha(color[3])
        width = textSurface.get_size()[0]
        height = textSurface.get_size()[1]
        
        surface.blit(textSurface, addLists(pos, [xOffset, yOffset]) if not areCoordsCenter else addLists([GAME_WIDTH//2 - width//2, GAME_HEIGHT//2 - height//2], [xOffset, yOffset]))
        
def MakeOveraly(text:str, alpha: int = 128, backgroundColor:tuple[int] = CLR_GRAY, font: pyg.font.Font = BIG_FONT, xTextOffset:int = 0, yTextOffset: int = 0):
    overlay:pyg.Surface = pyg.Surface((GAME_WIDTH, GAME_HEIGHT), pyg.SRCALPHA)
    overlay.fill(pyg.Color(*backgroundColor, alpha))
    DrawFont(text, font, CLR_WHITE, (GAME_WIDTH // 2, GAME_HEIGHT // 2), surface = overlay, areCoordsCenter = True, xOffset=xTextOffset, yOffset=yTextOffset)
    
    return overlay