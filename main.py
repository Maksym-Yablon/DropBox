import pygame
from sys import exit
import time  # Імпорт модуля для роботи з часом

# імпорт модулів гри з папки DROPBOX
import game
import grid
import piece
import ui
from menu import Menu
#-------------------


# Константи
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
KARATOVY = (255, 120, 18)
CARROT = (255, 160, 48)
# Розміри екрану
SCREEN_WIDTH = 800 # ширина екрану
SCREEN_HEIGHT = 950 # висота екрану

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("image/icon.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))  # картинка фону, з маштабуванням під розмір екрану

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Drop Box")
pygame.display.set_icon(pygame.image.load("image/icon.png"))

# Створюємо об'єкти
grid = grid.Grid() # ігрове поле
menu = Menu(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE)

# Показуємо заставку та меню
menu.show_splash_screen()
menu.main_menu()  # Запускаємо меню і чекаємо натискання "Грати"

# Основний цикл гри (запускається після натискання "Грати")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # код гри
    screen.fill(CARROT)
    grid.draw(screen)  # малюємо ігрове поле
    pygame.display.flip() # Оновлюємо екран
    clock.tick(60)
pygame.quit()
exit()    