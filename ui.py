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


class PauseButton:
    """Проста кнопка паузи в нижньому лівому куті"""
    
    def __init__(self):
        self.rect = pygame.Rect(PAUSE_BUTTON_X, PAUSE_BUTTON_Y, PAUSE_BUTTON_SIZE, PAUSE_BUTTON_SIZE)
        self.hovered = False
        self.font = pygame.font.Font(None, 24)
    
    def handle_mouse_motion(self, mouse_pos):
        """Обробляє рух миші для ховер ефекту"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_click(self, mouse_pos):
        """Обробляє клік по кнопці"""
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def draw(self, screen):
        """Малює кнопку паузи"""
        # Вибираємо колір залежно від ховера
        color = PAUSE_BUTTON_HOVER if self.hovered else PAUSE_BUTTON_COLOR
        
        # Малюємо кнопку з заокругленими кутами
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, PAUSE_BUTTON_BORDER, self.rect, 2, border_radius=8)
        
        # Малюємо іконку паузи
        pause_text = self.font.render("II", True, WHITE)
        text_rect = pause_text.get_rect(center=self.rect.center)
        screen.blit(pause_text, text_rect)


class ControlPanel:
    """Клас для панелі керування в грі"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.is_visible = True
        self.hover_button = None  # Кнопка під мишею
        
        # Визначаємо кнопки панелі
        self.buttons = {
            'pause': self._create_button(0, "⏸ Пауза"),
            'restart': self._create_button(1, "🔄 Нова гра"), 
            'settings': self._create_button(2, "⚙ Налаштування"),
            'help': self._create_button(3, "❓ Допомога"),
            'menu': self._create_button(4, "🏠 Меню")
        }
    
    def _create_button(self, index, text):
        """Створює кнопку на панелі"""
        y_pos = CONTROL_PANEL_Y + 50 + index * (CONTROL_BUTTON_HEIGHT + CONTROL_BUTTON_MARGIN)
        return {
            'rect': pygame.Rect(
                CONTROL_PANEL_X + 25, 
                y_pos,
                CONTROL_BUTTON_WIDTH, 
                CONTROL_BUTTON_HEIGHT
            ),
            'text': text,
            'enabled': True
        }
    
    def handle_mouse_motion(self, mouse_pos):
        """Обробляє рух миші для ефекту hover"""
        self.hover_button = None
        if self.is_visible:
            for button_name, button in self.buttons.items():
                if button['rect'].collidepoint(mouse_pos):
                    self.hover_button = button_name
                    break
    
    def handle_click(self, mouse_pos):
        """Обробляє клік по кнопках панелі"""
        if not self.is_visible:
            return None
            
        for button_name, button in self.buttons.items():
            if button['rect'].collidepoint(mouse_pos) and button['enabled']:
                return button_name
        return None
    
    def toggle_visibility(self):
        """Перемикає видимість панелі"""
        self.is_visible = not self.is_visible
    
    def draw(self):
        """Малює панель керування"""
        if not self.is_visible:
            return
            
        # Малюємо фон панелі з прозорістю
        panel_surface = pygame.Surface((CONTROL_PANEL_WIDTH, CONTROL_PANEL_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, CONTROL_PANEL_BG, 
                        (0, 0, CONTROL_PANEL_WIDTH, CONTROL_PANEL_HEIGHT), border_radius=15)
        self.screen.blit(panel_surface, (CONTROL_PANEL_X, CONTROL_PANEL_Y))
        
        # Рамка панелі
        pygame.draw.rect(self.screen, CONTROL_PANEL_BORDER,
                        (CONTROL_PANEL_X, CONTROL_PANEL_Y, CONTROL_PANEL_WIDTH, CONTROL_PANEL_HEIGHT),
                        width=2, border_radius=15)
        
        # Заголовок панелі
        title_text = self.font.render("Керування", True, CONTROL_BUTTON_TEXT)
        title_rect = title_text.get_rect(center=(CONTROL_PANEL_X + CONTROL_PANEL_WIDTH//2, CONTROL_PANEL_Y + 25))
        self.screen.blit(title_text, title_rect)
        
        # Малюємо кнопки
        for button_name, button in self.buttons.items():
            # Колір кнопки залежить від hover стану
            if button_name == self.hover_button:
                color = CONTROL_BUTTON_HOVER
            else:
                color = CONTROL_BUTTON_COLOR
            
            # Малюємо кнопку
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(self.screen, CONTROL_PANEL_BORDER, button['rect'], width=1, border_radius=8)
            
            # Текст кнопки
            text_surface = self.font.render(button['text'], True, CONTROL_BUTTON_TEXT)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)


class PauseMenu:
    """Меню паузи з напівпрозорим оверлеєм"""
    
    def __init__(self):
        self.is_paused = False
        self.overlay_alpha = 128
        self.buttons = []
        self._create_buttons()
    
    def _create_buttons(self):
        """Створює кнопки меню паузи"""
        button_width = 200
        button_height = 50
        button_spacing = 60
        
        # Центруємо кнопки
        start_x = (SCREEN_WIDTH - button_width) // 2
        start_y = (SCREEN_HEIGHT - (5 * button_height + 4 * button_spacing)) // 2
        
        buttons_data = [
            ('resume', 'Продовжити'),
            ('restart', 'Перезапустити'),
            ('settings', 'Налаштування'),
            ('help', 'Допомога'),
            ('menu', 'Головне меню')
        ]
        
        for i, (action, text) in enumerate(buttons_data):
            y = start_y + i * (button_height + button_spacing)
            button = {
                'action': action,
                'rect': pygame.Rect(start_x, y, button_width, button_height),
                'text': text,
                'hovered': False
            }
            self.buttons.append(button)
    
    def toggle_pause(self):
        """Перемикає стан паузи"""
        self.is_paused = not self.is_paused
        return self.is_paused
    
    def handle_click(self, mouse_pos):
        """Обробляє кліки по кнопках меню паузи"""
        if not self.is_paused:
            return None
            
        for button in self.buttons:
            if button['rect'].collidepoint(mouse_pos):
                return button['action']
        return None
    
    def handle_mouse_motion(self, mouse_pos):
        """Обробляє рух миші для ховер ефектів"""
        if not self.is_paused:
            return
            
        for button in self.buttons:
            button['hovered'] = button['rect'].collidepoint(mouse_pos)
    
    def draw(self, screen):
        """Малює меню паузи з оверлеєм"""
        if not self.is_paused:
            return
        
        # Створюємо напівпрозорий оверлей
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(self.overlay_alpha)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Малюємо заголовок
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("ПАУЗА", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Малюємо кнопки
        for button in self.buttons:
            # Кольори залежно від ховера
            if button['hovered']:
                button_color = CONTROL_BUTTON_HOVER
                text_color = WHITE
            else:
                button_color = CONTROL_BUTTON_COLOR
                text_color = CONTROL_BUTTON_TEXT
            
            # Малюємо кнопку
            pygame.draw.rect(screen, button_color, button['rect'], border_radius=8)
            pygame.draw.rect(screen, WHITE, button['rect'], 2, border_radius=8)
            
            # Малюємо текст
            font = pygame.font.Font(None, 24)
            text_surface = font.render(button['text'], True, text_color)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
        
    def show_pause_screen(self):
        """Показує екран паузи"""
        # Напівпрозорий фон
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 150), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(overlay, (0, 0))
        
        # Головний контейнер паузи
        pause_width, pause_height = 400, 300
        pause_x = (SCREEN_WIDTH - pause_width) // 2
        pause_y = (SCREEN_HEIGHT - pause_height) // 2
        
        # Фон меню паузи
        menu_surface = pygame.Surface((pause_width, pause_height), pygame.SRCALPHA)
        pygame.draw.rect(menu_surface, (30, 30, 60, 220), (0, 0, pause_width, pause_height), border_radius=20)
        self.screen.blit(menu_surface, (pause_x, pause_y))
        
        # Рамка
        pygame.draw.rect(self.screen, (100, 100, 150), 
                        (pause_x, pause_y, pause_width, pause_height), width=3, border_radius=20)
        
        # Заголовок "ПАУЗА"
        title_text = self.font_large.render("ПАУЗА", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, pause_y + 60))
        self.screen.blit(title_text, title_rect)
        
        # Інструкції
        instructions = [
            "ПРОБІЛ - продовжити гру",
            "ESC - головне меню", 
            "R - нова гра"
        ]
        
        y_offset = pause_y + 120
        for instruction in instructions:
            text = self.font_medium.render(instruction, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40


class SettingsMenu:
    """Клас для меню налаштувань"""
    
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font_large = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 24, bold=True)
        
        # Налаштування (поки що заглушки)
        self.settings = {
            'sound_enabled': True,
            'music_enabled': True,
            'show_grid_lines': True,
            'auto_save': True
        }
    
    def show_settings_screen(self):
        """Показує екран налаштувань"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Перевіряємо, що натиснута саме ліва кнопка миші
                    if event.button != 1:
                        continue  # Ігноруємо всі інші кнопки миші
                    # Тут буде логіка кліку по налаштуваннях
                    pass
                elif event.type == pygame.MOUSEWHEEL:
                    # Ігноруємо прокручування колеса миші
                    continue
            
            # Фон
            self.screen.fill(BACKGROUND_COLOR)
            
            # Заголовок
            title_text = self.font_large.render("НАЛАШТУВАННЯ", True, TEXT_COLOR)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Налаштування (поки що текстом)
            y_offset = 200
            settings_display = [
                f"Звук: {'Увімкнено' if self.settings['sound_enabled'] else 'Вимкнено'}",
                f"Музика: {'Увімкнена' if self.settings['music_enabled'] else 'Вимкнена'}",
                f"Лінії сітки: {'Показувати' if self.settings['show_grid_lines'] else 'Приховати'}",
                f"Автозбереження: {'Увімкнено' if self.settings['auto_save'] else 'Вимкнено'}"
            ]
            
            for setting in settings_display:
                text = self.font_medium.render(setting, True, TEXT_COLOR)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 50
            
            # Інструкція
            instruction = self.font_medium.render("ESC - повернутися", True, (180, 180, 180))
            instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(instruction, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(60)


# Створюємо глобальні екземпляри для використання в грі
ui_effects = UIEffects()
control_panel = None    # Ініціалізується в main.py
pause_menu = None       # Ініціалізується в main.py
settings_menu = None    # Ініціалізується в main.py
game_over_screen = None # Ініціалізується в main.py
game_ui = None         # Ініціалізується в main.py 
menu_system = None     # Ініціалізується в main.py

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
            print(f"НОВИЙ РЕКОРД! Очки: {final_score}")
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
                    # Перевіряємо, що натиснута саме ліва кнопка миші
                    if event.button != 1:
                        continue  # Ігноруємо всі інші кнопки миші
                    # Перевіряємо натискання кнопок
                    if try_again_button.collidepoint(event.pos):
                        return "restart"
                    elif menu_button.collidepoint(event.pos):
                        return "menu"
                elif event.type == pygame.MOUSEWHEEL:
                    # Ігноруємо прокручування колеса миші
                    continue
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
                title_text = title_font.render("НОВИЙ РЕКОРД!", True, PIECE_RED)
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
        self.score_font = pygame.font.SysFont("Arial",  int(FONT_SIZE * 0.9), bold=True)
        # Зменшуємо шрифт рекорда на 20% (24 * 0.8 = 19.2 ≈ 19)
        self.record_font = pygame.font.SysFont("Arial", int(FONT_SIZE_SMALL * 0.8), bold=True)
    
    def draw_hud(self, score, best_score):
        """Малює HUD (очки та рекорд)"""
        # Обчислюємо зміщення: 2% від розмірів екрану
        offset_x = int(SCREEN_WIDTH * 0.02)  # 2% вліво
        offset_y = int(SCREEN_HEIGHT * 0.02)  # 2% вгору
        
        # Відображаємо рекорд у верхньому лівому куті (перша позиція)
        record_text = self.record_font.render(f"Рекорд: {best_score}", True, TEXT_COLOR)
        self.screen.blit(record_text, (35 - offset_x, offset_y))
        
        # Відображаємо очки нижче рекорда (друга позиція) зі зміщенням
        score_text = self.score_font.render(f"Очки: {score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,  offset_y))

        # Показуємо просту підказку
        hints_font = pygame.font.SysFont("Arial", 18)
        hint_text = hints_font.render("N - Нова гра", True, (180, 180, 180))
        hint_rect = hint_text.get_rect()
        hint_rect.topright = (SCREEN_WIDTH - 30, 30)
        self.screen.blit(hint_text, hint_rect)


class MenuSystem:
    """Клас для системи меню"""
    
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.hovered_button = None  # Кнопка під мишею для ховер ефекту
    
    def draw_menu_buttons(self, has_saved_game=False):
        """Малює кнопки головного меню"""
        self.screen.fill(BACKGROUND_COLOR)  
        font = pygame.font.Font(None, 36)  # Трохи більший шрифт
        
        # Визначаємо кількість кнопок залежно від наявності збереження
        if has_saved_game:
            buttons_count = 5
            buttons_data = [
                ('continue', 'Продовжити', 0),
                ('play', 'Нова гра', 1),
                ('records', 'Рекорди', 2),
                ('settings', 'Налаштування', 3),
                ('exit', 'Вихід', 4)
            ]
        else:
            buttons_count = 4
            buttons_data = [
                ('play', 'Грати', 0),
                ('records', 'Рекорди', 1),
                ('settings', 'Налаштування', 2),
                ('exit', 'Вихід', 3)
            ]
        
        # Розраховуємо центральне розташування кнопок
        button_spacing = 70  # Трохи менша відстань між кнопками
        total_height = buttons_count * BUTTON_HEIGHT + (buttons_count - 1) * button_spacing
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        button_objects = []
        
        for button_id, text, index in buttons_data:
            y_pos = start_y + index * (BUTTON_HEIGHT + button_spacing)
            
            # Створюємо кнопку
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, y_pos, 200, BUTTON_HEIGHT)
            
            # Визначаємо кольори залежно від ховера
            is_hovered = self.hovered_button == button_id
            if is_hovered:
                button_color = CONTROL_BUTTON_HOVER
                text_color = WHITE
            else:
                button_color = CONTROL_BUTTON_COLOR
                text_color = CONTROL_BUTTON_TEXT
            
            # Малюємо кнопку з заокругленими кутами та рамкою як в меню паузи
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2, border_radius=8)
            
            # Малюємо текст
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
            
            button_objects.append((button_id, button_rect))
        
        return button_objects
    
    def handle_menu_hover(self, mouse_pos, has_saved_game=False):
        """Обробляє ховер ефекти для кнопок меню"""
        # Визначаємо кількість кнопок залежно від наявності збереження
        if has_saved_game:
            buttons_count = 5
            buttons_data = [
                ('continue', 0),
                ('play', 1),
                ('records', 2),
                ('settings', 3),
                ('exit', 4)
            ]
        else:
            buttons_count = 4
            buttons_data = [
                ('play', 0),
                ('records', 1),
                ('settings', 2),
                ('exit', 3)
            ]
        
        button_spacing = 70
        total_height = buttons_count * BUTTON_HEIGHT + (buttons_count - 1) * button_spacing
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        self.hovered_button = None
        for button_id, index in buttons_data:
            y_pos = start_y + index * (BUTTON_HEIGHT + button_spacing)
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, y_pos, 200, BUTTON_HEIGHT)
            if button_rect.collidepoint(mouse_pos):
                self.hovered_button = button_id
                break
    
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Перевіряємо, що натиснута саме ліва кнопка миші
                    if event.button != 1:
                        continue  # Ігноруємо всі інші кнопки миші
                elif event.type == pygame.MOUSEWHEEL:
                    # Ігноруємо прокручування колеса миші
                    continue
            
            # Малюємо фон
            self.screen.fill(BACKGROUND_COLOR)
            
            # Заголовок
            title_font = pygame.font.SysFont("Arial", FONT_SIZE_LARGE, bold=True)
            title_text = title_font.render("ТАБЛИЦЯ РЕКОРДІВ", True, MENU_TITLE_COLOR)
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
    
    def main_menu_loop(self, records_manager, background_image, save_manager=None):
        """Основний цикл меню"""
        # Показуємо заставку
        self.show_splash_screen(background_image)
        
        # Створюємо об'єкт налаштувань для меню
        settings_menu = SettingsMenu(self.screen, self.clock)
        
        while True:
            # Перевіряємо наявність збереженої гри
            has_saved_game = save_manager.has_saved_game() if save_manager else False
            
            # Обробляємо ховер ефекти
            mouse_pos = pygame.mouse.get_pos()
            self.handle_menu_hover(mouse_pos, has_saved_game)
            
            buttons = self.draw_menu_buttons(has_saved_game)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Перевіряємо, що натиснута саме ліва кнопка миші
                    if event.button != 1:
                        continue
                    
                    # Обробляємо кліки по кнопках
                    for button_id, button_rect in buttons:
                        if button_rect.collidepoint(event.pos):
                            if button_id == 'continue':
                                return 'continue'  # Продовжити збережену гру
                            elif button_id == 'play':
                                return 'new_game'  # Нова гра
                            elif button_id == 'records':
                                self.show_records_screen(records_manager)
                                break
                            elif button_id == 'settings':
                                result = settings_menu.show_settings_screen()
                                if result == "quit":
                                    pygame.quit()
                                    exit()
                                break
                            elif button_id == 'exit':
                                pygame.quit()
                                exit()
                            break
                elif event.type == pygame.MOUSEWHEEL:
                    continue

            pygame.display.update()
            self.clock.tick(60)
