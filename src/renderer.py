import pygame
from config import *
from objects.objek_game import Button

# Load images
try:
    menu_bg_orig = pygame.image.load("assets/background_main_menu.png").convert()
    menu_bg = pygame.transform.scale(menu_bg_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    menu_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu_bg.fill(BG)

ball_images = []
for i in range(1, 17):
    ball_img_orig = pygame.image.load(f"assets/images/ball_{i}.png").convert_alpha()
    ball_img_scaled = pygame.transform.scale(ball_img_orig, (int(36 * SCALE), int(36 * SCALE)))
    ball_images.append(ball_img_scaled)

# Tombol Menu
button_width = 300 * SCALE
button_height = 70 * SCALE
center_x = (SCREEN_WIDTH // 2) - (button_width // 2)
start_y = (SCREEN_HEIGHT // 2) + (20 * SCALE)

start_button = Button(center_x, start_y, button_width, button_height, "START GAME", large_font)
exit_button = Button(center_x, start_y + button_height + (20 * SCALE), button_width, button_height, "EXIT", large_font)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_centered_text(text, font, text_col, y_offset=0):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
    screen.blit(img, rect)

def draw_main_menu(game_state_callback, exit_callback):
    screen.blit(menu_bg, (0, 0))
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))

    title_text = "BILLIARD MASTER"
    title_surf = title_font.render(title_text, True, WHITE)
    shadow_surf = title_font.render(title_text, True, BLACK)
    
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - (120 * SCALE)))
    screen.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
    screen.blit(title_surf, title_rect)

    if start_button.draw(screen):
        game_state_callback()
    
    if exit_button.draw(screen):
        exit_callback()

    draw_centered_text("Press SPACE to Quick Start", small_font, GREY, y_offset=(250 * SCALE))