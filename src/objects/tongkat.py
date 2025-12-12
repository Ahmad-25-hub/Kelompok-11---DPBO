import pygame
import math

class Cue():
    def __init__(self, pos, image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, angle):
        self.angle = angle

    def draw(self, surface, pos, power_dist):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        radi = math.radians(self.angle)
        offset_x = math.cos(radi) * power_dist
        offset_y = math.sin(radi) * -power_dist
        new_x = pos[0] + offset_x
        new_y = pos[1] + offset_y
        self.rect = self.image.get_rect()
        self.rect.center = (new_x, new_y)
        surface.blit(self.image,
            (self.rect.centerx - self.image.get_width() / 2,
             self.rect.centery - self.image.get_height() / 2)
        )