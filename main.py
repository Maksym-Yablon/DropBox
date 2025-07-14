import pygame
from sys import exit

# імпорт модулів гри
import game
import grid
import piece
import ui
#-------------------


# Константи
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Розміри екрану
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("image/icon.png"),(SCREEN_WIDTH, SCREEN_HEIGHT)) #картинка фону, з маштабуванням під розмір екрану


# Ініціалізація Pygame
pygame.display.set_caption("Drop Box")
pygame.display.set_icon(pygame.image.load("image/icon.png"))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

screen.blit(BACKGROUND_IMAGE, (0, 0))

# Основний цикл гри
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        #game code


        pygame.display.update()
        clock.tick(60)