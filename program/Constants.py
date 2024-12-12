from typing import Literal
import pygame as pyg

CLR_BLACK = (0,0,0)
CLR_WHITE = (255, 255, 255)
CLR_GREEN = (0, 255, 0)
CLR_RED = (255, 0, 0)
CLR_GRAY = (20, 20, 20)

pyg.init()

BIG_FONT = pyg.font.Font("GameFont.ttf", 24)
MEDIUM_FONT = pyg.font.Font("GameFont.ttf", 18)
SMALL_FONT = pyg.font.Font("GameFont.ttf", 12)

TILE_SIZE = 20
CLOCK = pyg.time.Clock()


GAME_WIDTH = 31 * TILE_SIZE
GAME_HEIGHT = 31 * TILE_SIZE
TOP_OFFSET = 30
WIN_WIDTH = GAME_WIDTH
WIN_HEIGHT = GAME_HEIGHT + TOP_OFFSET
WIN_CENTER = (WIN_WIDTH//2, WIN_HEIGHT//2)

WIN = pyg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

START_COORDS = [15,15]
DEFAULT_SNAKE_LEN = 5

DRAW_GRID = True

DIR = Literal["u","d","l","r","0"]
