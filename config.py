import pygame
import os
from audio import *

pygame.init()

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREY = 90, 90, 90
BLUE1 = "#2339FF"


TILE_SIZE = 32


SIZE = (WIDTH, HEIGHT) = ( 1280, 720 )
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Deep Sea Cleaner")

FPS = 60

EIGHT_BIT_WONDER = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), 50)
COMPASS_PRO = pygame.font.Font(os.path.join("font", "CompassPro.ttf"), 70)
EQUIPMENT_PRO = pygame.font.Font(os.path.join("font", "EquipmentPro.ttf"), 30)
EXPRESSION_PRO = pygame.font.Font(os.path.join("font", "ExpressionPro.ttf"), 35)
FUTILE_PRO = pygame.font.Font(os.path.join("font", "FutilePro.ttf"), 70)
MATCHUP_PRO =  pygame.font.Font(os.path.join("font", "MatchupPro.ttf"), 50)
MONOGRAM_EXTENDED = pygame.font.Font(os.path.join("font", "monogram-extended.ttf"), 70)
QUIXEL = pygame.font.Font(os.path.join("font", "Quixel.ttf"), 40)
THALEAH_FAT = pygame.font.Font(os.path.join("font", "ThaleahFat.ttf"), 85)

MUSIC = Music()
SFX = SoundEffects()