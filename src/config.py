import pygame

pygame.init()

# --- FAKTOR SKALA ---
SCALE = 0.7 

# --- UKURAN MEJA & LAYAR ---
TABLE_WIDTH = int(1200 * SCALE)
TABLE_HEIGHT = int(678 * SCALE)
MARGIN_X = int(150 * SCALE)
MARGIN_Y = int(140 * SCALE)
BOTTOM_PANEL = int(40 * SCALE)
SCREEN_WIDTH = TABLE_WIDTH + (MARGIN_X * 2)
SCREEN_HEIGHT = TABLE_HEIGHT + MARGIN_Y + BOTTOM_PANEL

# Colours
BG = (50, 50, 50)
UI_BG = (30, 30, 30)
PANEL_BG = (40, 45, 50)
ACTIVE_BORDER = (255, 215, 0) # Gold
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (50, 150, 255)
GREEN = (0, 255, 0)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("Lato", int(26 * SCALE))
large_font = pygame.font.SysFont("Lato", int(40 * SCALE), bold=True)
title_font = pygame.font.SysFont("Lato", int(80 * SCALE), bold=True)
small_font = pygame.font.SysFont("Lato", int(20 * SCALE))

# Screen Setup (Dibuat di sini agar bisa diimport renderer)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pool Game - 2 Players (Improved UI)")
clock = pygame.time.Clock()
FPS = 120