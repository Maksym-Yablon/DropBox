import pygame
from sys import exit
import time  # Імпорт модуля для роботи з часом

# імпорт модулів
import game
import menu
import grid

# Константи
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Розміри екрану
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("image/icon.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))  # картинка фону, з маштабуванням під розмір екрану

# Ініціалізація Pygame
pygame.display.set_caption("Drop Box")
pygame.display.set_icon(pygame.image.load("image/icon.png"))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def draw_menu():
    screen.fill(BLUE)  # Змінюємо фон меню на синій
    font = pygame.font.Font(None, 50)
    play_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 150, 150, 60)  # Розміщуємо кнопку трохи нижче
    pygame.draw.rect(screen, GREEN, play_button)

    # Центруємо текст всередині кнопки
    text = font.render("Грати", True, BLACK)
    text_rect = text.get_rect(center=play_button.center)  # Центруємо текст відносно кнопки
    screen.blit(text, text_rect)

    return play_button

def main_menu():
    while True:
        play_button = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return  # Вихід із меню, початок гри

        pygame.display.update()
        clock.tick(60)

# Заставка перед меню
screen.fill(WHITE)
screen.blit(BACKGROUND_IMAGE, (0, 0))
pygame.display.update()

time.sleep(10)  # Очікування 10 секунд

# Очищення екрану після заставки
screen.fill(WHITE)
pygame.display.update()

# Основний цикл гри
main_menu()  # Виклик меню після заставки

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # game code

    pygame.display.update()
    clock.tick(60)