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
        """Малює меню з кнопками"""
        self.screen.fill(CARROT)  
        font = pygame.font.Font(None, 50)
        
        # Кнопка "Грати"
        play_button = pygame.Rect(self.screen_width // 2 - 75, self.screen_height // 2 + 100, 150, 60)
        pygame.draw.rect(self.screen, KARATOVY, play_button)
        play_text = font.render("Грати", True, BLACK)
        play_text_rect = play_text.get_rect(center=play_button.center)
        self.screen.blit(play_text, play_text_rect)
        
        # Кнопка "Рекорди"
        records_button = pygame.Rect(self.screen_width // 2 - 75, self.screen_height // 2 + 180, 150, 60)
        pygame.draw.rect(self.screen, LIGHTBLUE, records_button)
        records_text = font.render("Рекорди", True, BLACK)
        records_text_rect = records_text.get_rect(center=records_button.center)
        self.screen.blit(records_text, records_text_rect)

        return play_button, records_button

    def main_menu(self):
        """Основний цикл меню"""
        while True:
            play_button, records_button = self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        return  # Вихід із меню, початок гри
                    elif records_button.collidepoint(event.pos):
                        self.show_records_screen()  # Показуємо рекорди

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

    def show_records_screen(self):
        """Показує екран з рекордами"""
        from records import records_manager  # Імпортуємо тут, щоб уникнути циклічного імпорту
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Повертаємося до головного меню
            
            # Малюємо фон
            self.screen.fill(CARROT)
            
            # Заголовок
            title_font = pygame.font.SysFont("Arial", 48, bold=True)
            title_text = title_font.render("🏆 ТАБЛИЦЯ РЕКОРДІВ", True, BLACK)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Отримуємо рекорди
            records = records_manager.get_top_records(10)
            
            if records:
                # Малюємо рекорди
                record_font = pygame.font.SysFont("Arial", 32, bold=True)
                y_offset = 200
                
                for i, record in enumerate(records, 1):
                    # Номер та очки
                    record_text = f"{i}. {record['score']} очок"
                    
                    # Різні кольори для топ-3
                    if i == 1:
                        color = (255, 215, 0)  # Золото
                    elif i == 2:
                        color = (192, 192, 192)  # Срібло
                    elif i == 3:
                        color = (205, 127, 50)  # Бронза
                    else:
                        color = BLACK
                    
                    text_surface = record_font.render(record_text, True, color)
                    self.screen.blit(text_surface, (200, y_offset))
                    
                    # Дата
                    date_font = pygame.font.SysFont("Arial", 20)
                    date_text = date_font.render(record['date'], True, (100, 100, 100))
                    self.screen.blit(date_text, (500, y_offset + 5))
                    
                    y_offset += 45
            else:
                # Немає рекордів
                no_records_font = pygame.font.SysFont("Arial", 36)
                no_records_text = no_records_font.render("Рекордів поки немає", True, BLACK)
                no_records_rect = no_records_text.get_rect(center=(self.screen_width // 2, 300))
                self.screen.blit(no_records_text, no_records_rect)
            
            # Інструкція
            instruction_font = pygame.font.SysFont("Arial", 24)
            instruction_text = instruction_font.render("Натисніть ESC для повернення", True, (100, 100, 100))
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
            self.screen.blit(instruction_text, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(60)
