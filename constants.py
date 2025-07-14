import pygame
# Константи
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
KARATOVY = (255, 120, 18)
CARROT = (255, 160, 48)
# Розміри екрану
SCREEN_WIDTH = 1300 # ширина екрану
SCREEN_HEIGHT = 700 # висота екрану

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("image/icon.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))  # картинка фону, з маштабуванням під розмір екрану
