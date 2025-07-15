import pygame
import math
import time
from sys import exit
from constants import *

class UIEffects:
    """Клас для візуальних ефектів інтерфейсу"""
    
    def __init__(self):
        self.blink_start_time = 0
        self.blink_duration = 1.2  # Повільніше миготіння - 1.2 секунди на цикл
        self.is_blinking = False
        
    def start_blinking(self):
        """Запускає ефект мигання"""
        self.blink_start_time = time.time()
        self.is_blinking = True
    
    def stop_blinking(self):
        """Зупиняє ефект мигання"""
        self.is_blinking = False
    
    def get_blink_alpha(self):
        """Повертає прозорість для ефекту мигання (від 80 до 160 для кращої видимості)"""
        if not self.is_blinking:
            return 160
        
        current_time = time.time()
        elapsed = current_time - self.blink_start_time
        
        # Синусоїдальна функція для плавного мигання
        blink_cycle = math.sin(elapsed * (2 * math.pi / self.blink_duration))
        # Перетворюємо з діапазону [-1, 1] в [80, 160] для м'якшого ефекту
        alpha = int(120 + blink_cycle * 40)
        return max(80, min(160, alpha))
    
    def draw_piece_preview(self, surface, grid, piece, grid_x, grid_y, cell_size=GRID_CELL_SIZE, valid=True):
        """Малює попередній перегляд фігури з підсвічуванням"""
        offset_x = (SCREEN_WIDTH - grid.size * cell_size) // 2
        offset_y = (SCREEN_HEIGHT - grid.size * cell_size) // 2
        
        # Колір підсвічування залежно від валідності
        if valid:
            base_color = (144, 238, 144)  # Світло-салатовий (Light Green)
        else:
            base_color = (255, 160, 160)  # Світло-червоний для помилок
        
        # Отримуємо прозорість для мигання
        alpha = self.get_blink_alpha() if valid else 120
        
        # Створюємо поверхню з прозорістю
        preview_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col] == 1:
                    target_row = grid_y + row
                    target_col = grid_x + col
                    
                    # Перевіряємо, чи в межах сітки
                    if (0 <= target_row < grid.size and 0 <= target_col < grid.size):
                        rect = pygame.Rect(
                            offset_x + target_col * cell_size,
                            offset_y + target_row * cell_size,
                            cell_size, cell_size
                        )
                        
                        # Малюємо підсвічування з мигающою прозорістю
                        color_with_alpha = (*base_color, alpha)
                        pygame.draw.rect(preview_surface, color_with_alpha, (0, 0, cell_size, cell_size))
                        surface.blit(preview_surface, rect.topleft)
                        
                        # Додаємо тонку рамку для кращої видимості
                        frame_color = (min(255, base_color[0] + 40), min(255, base_color[1] + 40), min(255, base_color[2] + 40))
                        pygame.draw.rect(surface, frame_color, rect, 2)
    
    def get_lines_to_clear_preview(self, grid, piece, grid_x, grid_y):
        """Повертає списки рядків та стовпців, які будуть очищені після розміщення фігури"""
        if not grid.can_place_piece(piece, grid_x, grid_y):
            return [], []
        
        # Створюємо копію сітки для симуляції
        temp_cells = [row[:] for row in grid.cells]
        
        # Тимчасово розміщуємо фігуру
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col] == 1:
                    target_row = grid_y + row
                    target_col = grid_x + col
                    if (0 <= target_row < grid.size and 0 <= target_col < grid.size):
                        temp_cells[target_row][target_col] = piece.color
        
        # Перевіряємо, які лінії будуть повними
        full_rows = []
        full_cols = []
        
        # Перевіряємо рядки
        for row in range(grid.size):
            if all(temp_cells[row][col] is not None for col in range(grid.size)):
                full_rows.append(row)
        
        # Перевіряємо стовпці
        for col in range(grid.size):
            if all(temp_cells[row][col] is not None for row in range(grid.size)):
                full_cols.append(col)
        
        return full_rows, full_cols
    
    def draw_clearing_preview(self, surface, grid, full_rows, full_cols, cell_size=GRID_CELL_SIZE):
        """Малює мигаючий попередній перегляд очищення ліній"""
        if not full_rows and not full_cols:
            return
        
        offset_x = (SCREEN_WIDTH - grid.size * cell_size) // 2
        offset_y = (SCREEN_HEIGHT - grid.size * cell_size) // 2
        
        # Отримуємо прозорість для мигання
        alpha = self.get_blink_alpha()
        
        # Колір для мигання очищення (світло-жовтий/персиковий)
        clear_color = (255, 218, 185, alpha)  # Персиковий з прозорістю
        
        # Створюємо поверхню для ефекту
        effect_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        
        # Підсвічуємо рядки, що будуть очищені
        for row in full_rows:
            for col in range(grid.size):
                rect = pygame.Rect(
                    offset_x + col * cell_size,
                    offset_y + row * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(effect_surface, clear_color, (0, 0, cell_size, cell_size))
                surface.blit(effect_surface, rect.topleft)
                
                # Додаємо м'яку рамку
                pygame.draw.rect(surface, (255, 200, 150), rect, 2)
        
        # Підсвічуємо стовпці, що будуть очищені
        for col in full_cols:
            for row in range(grid.size):
                rect = pygame.Rect(
                    offset_x + col * cell_size,
                    offset_y + row * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(effect_surface, clear_color, (0, 0, cell_size, cell_size))
                surface.blit(effect_surface, rect.topleft)
                
                # Додаємо м'яку рамку
                pygame.draw.rect(surface, (255, 200, 150), rect, 2)
    
    def draw_enhanced_preview(self, surface, grid, piece, grid_x, grid_y, cell_size=GRID_CELL_SIZE):
        """Комплексний попередній перегляд з підсвічуванням фігури та майбутнього очищення"""
        valid = grid.can_place_piece(piece, grid_x, grid_y)
        
        if valid:
            # Запускаємо мигання, якщо ще не запущено
            if not self.is_blinking:
                self.start_blinking()
            
            # Отримуємо лінії для очищення
            full_rows, full_cols = self.get_lines_to_clear_preview(grid, piece, grid_x, grid_y)
            
            # Спочатку малюємо попередній перегляд очищення
            if full_rows or full_cols:
                self.draw_clearing_preview(surface, grid, full_rows, full_cols, cell_size)
            
            # Потім малюємо попередній перегляд фігури
            self.draw_piece_preview(surface, grid, piece, grid_x, grid_y, cell_size, valid)
        else:
            # Зупиняємо мигання для невалідних позицій
            self.stop_blinking()
            # Малюємо червоний попередній перегляд
            self.draw_piece_preview(surface, grid, piece, grid_x, grid_y, cell_size, valid)

    def draw_simple_piece_box(self, surface, piece_box):
        """Малює просту мінімалістичну коробку для фігур з прозорістю"""
        box_rect = pygame.Rect(piece_box.start_x, piece_box.start_y, piece_box.width, piece_box.height)
        
        # Створюємо поверхню з прозорістю для заливки
        box_surface = pygame.Surface((piece_box.width, piece_box.height), pygame.SRCALPHA)
        
        # Заливка з прозорістю (коричневий колір схожий на сітку)
        fill_color = (*PIECE_BOX_FILL_COLOR, 40)  # Коричневий з прозорістю 40/255
        pygame.draw.rect(box_surface, fill_color, (0, 0, piece_box.width, piece_box.height), border_radius=10)
        
        # Малюємо заливку на екрані
        surface.blit(box_surface, (piece_box.start_x, piece_box.start_y))
        
        # Обводка (коричневий колір як сітка)
        pygame.draw.rect(surface, PIECE_BOX_BORDER_COLOR, box_rect, width=2, border_radius=10)


# Створюємо глобальні екземпляри для використання в грі
ui_effects = UIEffects()
game_over_screen = None  # Ініціалізується в main.py
game_ui = None          # Ініціалізується в main.py 
menu_system = None      # Ініціалізується в main.py

class GameOverScreen:
    """Клас для екрану завершення гри"""
    
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
    
    def show(self, final_score, records_manager):
        """Показує екран завершення гри з результатами"""
        # Додаємо рекорд
        is_new_record = records_manager.add_record(final_score)
        
        # Повідомляємо гравця в консоль
        if is_new_record:
            print(f"🎉 НОВИЙ РЕКОРД! Очки: {final_score}")
            position = records_manager.get_player_position(final_score)
            if position:
                print(f"Ваша позиція: {position} місце")
        else:
            print(f"Гра завершена! Очки: {final_score}")
            best_score = records_manager.get_best_score()
            print(f"Найкращий результат: {best_score}")
        
        # Екран результатів
        while True:
            # Ініціалізуємо кнопки
            try_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 350, BUTTON_WIDTH_LARGE, BUTTON_HEIGHT)
            menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 430, BUTTON_WIDTH_MEDIUM, BUTTON_HEIGHT)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Перевіряємо натискання кнопок
                    if try_again_button.collidepoint(event.pos):
                        return "restart"
                    elif menu_button.collidepoint(event.pos):
                        return "menu"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "restart"
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"
            
            # Малюємо екран результатів
            self.screen.fill(BACKGROUND_COLOR)
            
            # Заголовок
            title_font = pygame.font.SysFont("Arial", FONT_SIZE_LARGE, bold=True)
            if is_new_record:
                title_text = title_font.render("🎉 НОВИЙ РЕКОРД!", True, PIECE_RED)
            else:
                title_text = title_font.render("ГРА ЗАВЕРШЕНА", True, TEXT_COLOR)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)
            
            # Очки
            score_display_font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
            score_display_text = score_display_font.render(f"Ваш результат: {final_score} очок", True, TEXT_COLOR)
            score_display_rect = score_display_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
            self.screen.blit(score_display_text, score_display_rect)
            
            # Найкращий результат
            best_score = records_manager.get_best_score()
            record_font = pygame.font.SysFont("Arial", FONT_SIZE_SMALL, bold=True)
            best_score_text = record_font.render(f"Найкращий результат: {best_score}", True, TEXT_COLOR)
            best_score_rect = best_score_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
            self.screen.blit(best_score_text, best_score_rect)
            
            # Кнопки
            button_font = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM, bold=True)
            
            # Малюємо кнопку "Спробувати ще раз"
            pygame.draw.rect(self.screen, BUTTON_COLOR, try_again_button)
            try_again_text = button_font.render("Спробувати ще раз", True, TEXT_COLOR)
            try_again_text_rect = try_again_text.get_rect(center=try_again_button.center)
            self.screen.blit(try_again_text, try_again_text_rect)
            
            # Малюємо кнопку "Головне меню"
            pygame.draw.rect(self.screen, BUTTON_COLOR, menu_button)
            menu_text = button_font.render("Головне меню", True, TEXT_COLOR)
            menu_text_rect = menu_text.get_rect(center=menu_button.center)
            self.screen.blit(menu_text, menu_text_rect)
            
            # Інструкції
            instruction_font = pygame.font.SysFont("Arial", 20)
            instruction1 = instruction_font.render("ПРОБІЛ - грати знову, ESC - меню", True, TEXT_COLOR)
            instruction1_rect = instruction1.get_rect(center=(SCREEN_WIDTH // 2, 550))
            self.screen.blit(instruction1, instruction1_rect)
            
            pygame.display.flip()
            self.clock.tick(60)


class GameUI:
    """Клас для основного ігрового інтерфейсу"""
    
    def __init__(self, screen):
        self.screen = screen
        self.score_font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
        self.record_font = pygame.font.SysFont("Arial", FONT_SIZE_SMALL, bold=True)
    
    def draw_hud(self, score, best_score):
        """Малює HUD (очки та рекорд)"""
        # Відображаємо очки у верхньому лівому куті
        score_text = self.score_font.render(f"Очки: {score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (30, 30))
        
        # Відображаємо найкращий рекорд
        record_text = self.record_font.render(f"Рекорд: {best_score}", True, TEXT_COLOR)
        self.screen.blit(record_text, (30, 80))


class MenuSystem:
    """Клас для системи меню"""
    
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
    
    def draw_menu_buttons(self):
        """Малює кнопки головного меню"""
        self.screen.fill(BACKGROUND_COLOR)  
        font = pygame.font.Font(None, 50)
        
        # Кнопка "Грати"
        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 100, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, BUTTON_COLOR, play_button)
        play_text = font.render("Грати", True, TEXT_COLOR)
        play_text_rect = play_text.get_rect(center=play_button.center)
        self.screen.blit(play_text, play_text_rect)
        
        # Кнопка "Рекорди"
        records_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 180, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, BUTTON_COLOR, records_button)
        records_text = font.render("Рекорди", True, TEXT_COLOR)
        records_text_rect = records_text.get_rect(center=records_button.center)
        self.screen.blit(records_text, records_text_rect)

        return play_button, records_button
    
    def show_records_screen(self, records_manager):
        """Показує екран з рекордами"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Повертаємося до головного меню
            
            # Малюємо фон
            self.screen.fill(BACKGROUND_COLOR)
            
            # Заголовок
            title_font = pygame.font.SysFont("Arial", FONT_SIZE_LARGE, bold=True)
            title_text = title_font.render("🏆 ТАБЛИЦЯ РЕКОРДІВ", True, MENU_TITLE_COLOR)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Отримуємо рекорди
            records = records_manager.get_top_records(10)
            
            if records:
                # Малюємо рекорди
                record_font = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM, bold=True)
                y_offset = 200
                
                for i, record in enumerate(records, 1):
                    # Номер та очки
                    record_text = f"{i}. {record['score']} очок"
                    
                    # Різні кольори для топ-3
                    if i == 1:
                        color = MEDAL_GOLD
                    elif i == 2:
                        color = MEDAL_SILVER
                    elif i == 3:
                        color = MEDAL_BRONZE
                    else:
                        color = MENU_TEXT_COLOR
                    
                    text_surface = record_font.render(record_text, True, color)
                    self.screen.blit(text_surface, (200, y_offset))
                    
                    # Дата
                    date_font = pygame.font.SysFont("Arial", 20)
                    date_text = date_font.render(record['date'], True, MENU_TEXT_COLOR)
                    self.screen.blit(date_text, (500, y_offset + 5))
                    
                    y_offset += 45
            else:
                # Немає рекордів
                no_records_font = pygame.font.SysFont("Arial", FONT_SIZE)
                no_records_text = no_records_font.render("Рекордів поки немає", True, MENU_TEXT_COLOR)
                no_records_rect = no_records_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
                self.screen.blit(no_records_text, no_records_rect)
            
            # Інструкція
            instruction_font = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            instruction_text = instruction_font.render("Натисніть ESC для повернення", True, MENU_TEXT_COLOR)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(instruction_text, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def show_splash_screen(self, background_image):
        """Показує заставку перед меню"""
        self.screen.fill(WHITE)
        self.screen.blit(background_image, (0, 0))
        pygame.display.update()
        
        # Очищення екрану після заставки
        self.screen.fill(WHITE)
        pygame.display.update()
    
    def main_menu_loop(self, records_manager, background_image):
        """Основний цикл меню"""
        # Показуємо заставку
        self.show_splash_screen(background_image)
        
        while True:
            play_button, records_button = self.draw_menu_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        return  # Вихід із меню, початок гри
                    elif records_button.collidepoint(event.pos):
                        self.show_records_screen(records_manager)  # Показуємо рекорди

            pygame.display.update()
            self.clock.tick(60)
