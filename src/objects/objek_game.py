import pygame
from config import SCALE, DIA

def load_ball_images():
    ball_images = []
    for i in range(1, 17):
        try:
            ball_img_orig = pygame.image.load(f"assets/images/ball_{i}.png").convert_alpha()
            ball_img_scaled = pygame.transform.scale(ball_img_orig, (DIA, DIA))
            ball_images.append(ball_img_scaled)
        except:
            # Fallback jika gambar tidak ditemukan
            surf = pygame.Surface((DIA, DIA))
            surf.fill((255, 255, 255))
            ball_images.append(surf)
    return ball_images