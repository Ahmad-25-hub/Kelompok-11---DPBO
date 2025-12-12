import pygame

# --- KONFIGURASI UMUM ---
SCALE = 0.7 
FPS = 120

# --- UKURAN ---
TABLE_WIDTH = int(1200 * SCALE)
TABLE_HEIGHT = int(678 * SCALE)
MARGIN_X = int(150 * SCALE)
MARGIN_Y = int(140 * SCALE)
BOTTOM_PANEL = int(40 * SCALE)
SCREEN_WIDTH = TABLE_WIDTH + (MARGIN_X * 2)
SCREEN_HEIGHT = TABLE_HEIGHT + MARGIN_Y + BOTTOM_PANEL

# --- UKURAN BOLA & POCKET ---
DIA = int(36 * SCALE)
POCKET_DIA = int(66 * SCALE)

# --- WARNA ---
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

# --- FONT (Diinisialisasi nanti di main agar aman) ---
font = None
large_font = None
title_font = None
small_font = None

def init_fonts():
    global font, large_font, title_font, small_font
    font = pygame.font.SysFont("Lato", int(26 * SCALE))
    large_font = pygame.font.SysFont("Lato", int(40 * SCALE), bold=True)
    title_font = pygame.font.SysFont("Lato", int(80 * SCALE), bold=True)
    small_font = pygame.font.SysFont("Lato", int(20 * SCALE))