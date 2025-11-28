import pygame
import math

class Tongkat:
    def __init__(self, image):
        self.original_image = image
        self.angle = 0
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def update(self, angle):
        self.angle = angle

    def draw(self, surface, pos, power_dist):
        # power_dist: jarak mundur/offset (bisa >0 saat tarik, atau saat animasi)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        radi = math.radians(self.angle)

        offset_x = math.cos(radi) * power_dist
        offset_y = -math.sin(radi) * power_dist  # - karena koordinat pygame terbalik di Y

        new_x = pos[0] + offset_x
        new_y = pos[1] + offset_y

        self.rect = self.image.get_rect(center=(new_x, new_y))
        surface.blit(self.image,
                     (self.rect.centerx - self.image.get_width() / 2,
                      self.rect.centery - self.image.get_height() / 2))
