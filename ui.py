import pygame

class UI:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw_menu(self):
        self.screen.fill((0, 0, 255))  # Змінюємо фон меню на синій
        font = pygame.font.Font(None, 50)
        play_button = pygame.Rect(self.screen_width // 2 - 75, self.screen_height // 2 + 150, 150, 60)  # Розміщуємо кнопку трохи нижче
        pygame.draw.rect(self.screen, (0, 255, 0), play_button)

        # Центруємо текст всередині кнопки
        text = font.render("Грати", True, (0, 0, 0))
        text_rect = text.get_rect(center=play_button.center)  # Центруємо текст відносно кнопки
        self.screen.blit(text, text_rect)

        return play_button