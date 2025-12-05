import pygame
from config import *

table_image_orig = pygame.image.load("assets/images/table.png").convert_alpha()
table_image = pygame.transform.scale(table_image_orig, (TABLE_WIDTH, TABLE_HEIGHT))