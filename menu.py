import pygame
from sys import exit
import time
from constants import*  # Імпорт констант

class Menu:
    def __init__(self, screen, clock, screen_width, screen_height, background_image):
        self.screen = screen
        self.clock = clock
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_image = background_image

    def draw_menu(self):
        """Малює меню з кнопкою Грати"""
        self.screen.fill(CARROT)  
        font = pygame.font.Font(None, 50)
        play_button = pygame.Rect(self.screen_width // 2 - 75, self.screen_height // 2 + 150, 150, 60)
        pygame.draw.rect(self.screen, KARATOVY, play_button)

        # Центруємо текст всередині кнопки
        text = font.render("Грати", True, BLACK)
        text_rect = text.get_rect(center=play_button.center)
        self.screen.blit(text, text_rect)

        return play_button

    def main_menu(self):
        """Основний цикл меню"""
        while True:
            play_button = self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        return  # Вихід із меню, початок гри

            pygame.display.update()
            self.clock.tick(60)

    def show_splash_screen(self):
        """Показує заставку перед меню"""
        self.screen.fill(WHITE)
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.update()
        #time.sleep(5)  # Очікування 5 секунд

        # Очищення екрану після заставки
        self.screen.fill(WHITE)
        pygame.display.update()
