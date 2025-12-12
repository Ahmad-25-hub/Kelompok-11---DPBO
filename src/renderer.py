import pygame
from config import *

def draw_text(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

def draw_centered_text(surface, text, font, text_col, y_offset=0):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
    surface.blit(img, rect)

class Button():
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        # Warna default
        top_color = PANEL_BG
        text_col = WHITE
        border_col = WHITE
        shadow_offset = 5

        # Cek Hover
        if self.rect.collidepoint(pos):
            top_color = (60, 65, 70) 
            border_col = ACTIVE_BORDER 
            text_col = ACTIVE_BORDER
            
            # Cek Klik
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Gambar Bayangan (Shadow)
        shadow_rect = pygame.Rect(self.rect.x + shadow_offset, self.rect.y + shadow_offset, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (20, 20, 20), shadow_rect, border_radius=15)

        # Gambar Kotak Utama
        pygame.draw.rect(surface, top_color, self.rect, border_radius=15)
        
        # Gambar Border
        pygame.draw.rect(surface, border_col, self.rect, 3, border_radius=15)

        # Gambar Teks
        text_img = self.font.render(self.text, True, text_col)
        text_rect = text_img.get_rect(center=self.rect.center)
        surface.blit(text_img, text_rect)

        return action