import pygame
import random
from constants import *


class Grid:
    """Клас для управління ігровою сіткою 8x8"""
    
    def __init__(self, size=8, generate_initial=True):
        self.size = size
        self.cells = [[None for _ in range(size)] for _ in range(size)]  # Ігрова сітка
        self.score = 0  # Поточний рахунок
        self.combo_multiplier = 1  # Множник комбо
        self.last_clear_success = False
        
        # Генеруємо початкові фігури, якщо потрібно
        if generate_initial:
            self.generate_simple_initial_setup()

    def generate_simple_initial_setup(self):
        """Проста генерація початкових фігур на сітці"""
        from piece import generate_random_piece
        
        # Випадкова кількість фігур від 2 до 6
        num_pieces = random.randint(2, 6)
        placed_pieces = 0
        max_attempts = 30  # Максимум спроб
        
        print(f"🎲 Генерація {num_pieces} початкових фігур...")
        
        for attempt in range(max_attempts):
            if placed_pieces >= num_pieces:
                break
                
            # Генеруємо випадкову фігуру
            piece = generate_random_piece()
            
            # Випадкова позиція на сітці
            grid_x = random.randint(0, self.size - 3)  # Залишаємо місце для фігури
            grid_y = random.randint(0, self.size - 3)
            
            # Перевіряємо, чи можна розмістити фігуру
            if self.can_place_piece(piece, grid_x, grid_y):
                # Розміщуємо фігуру
                for row in range(len(piece.shape)):
                    for col in range(len(piece.shape[row])):
                        if piece.shape[row][col] == 1:
                            target_row = grid_y + row
                            target_col = grid_x + col
                            if (0 <= target_row < self.size and 0 <= target_col < self.size):
                                self.cells[target_row][target_col] = piece.color
                
                placed_pieces += 1
                print(f"  ✓ Фігура {placed_pieces}/{num_pieces} розміщена в позиції ({grid_x}, {grid_y})")
        
        if placed_pieces < num_pieces:
            print(f"  ⚠️ Розміщено {placed_pieces} з {num_pieces} фігур")
        else:
            print(f"  🎉 Успішно розміщено всі {num_pieces} фігури!")
        
        # Скидаємо очки після початкового розміщення
        self.score = 0

    def draw(self, surface, cell_size=GRID_CELL_SIZE):
        """Малює ігрову сітку на екрані"""
        offset_x = (SCREEN_WIDTH - self.size * cell_size) // 2
        offset_y = (SCREEN_HEIGHT - self.size * cell_size) // 2
        
        # Малюємо сітку
        for row in range(self.size):
            for col in range(self.size):
                rect = pygame.Rect(
                    offset_x + col * cell_size,
                    offset_y + row * cell_size,
                    cell_size, cell_size
                )
                
                if self.cells[row][col] is None:
                    color = EMPTY_CELL_COLOR  # Порожня клітинка
                else:
                    color = self.cells[row][col]  # Колір фігури
                    
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, GRID_LINE_COLOR, rect, 1)  # Рамка

    def is_row_full(self, row):
        """Перевіряє, чи рядок заповнений"""
        return all(self.cells[row][col] is not None for col in range(self.size))

    def is_col_full(self, col):
        """Перевіряє, чи стовпець заповнений"""
        return all(self.cells[row][col] is not None for row in range(self.size))

    def clear_full_rows(self):
        """Очищає заповнені рядки"""
        cleared = 0
        for row in range(self.size):
            if self.is_row_full(row):
                for col in range(self.size):
                    self.cells[row][col] = None  # Очищаємо клітинки до None
                cleared += 1
        return cleared
    
    def clear_full_cols(self):
        # очищаємо заповнені стовпці
        cleared = 0
        for col in range(self.size):
            if self.is_col_full(col):
                for row in range(self.size):
                    self.cells[row][col] = None  # очищаємо клітинки до None
                cleared += 1
        return cleared
    
    # ГОЛОВНА ФУНКЦІЯ ОЧИЩЕННЯ
    def clear_lines(self):
        """Очищає всі повні лінії (рядки + стовпці) і нараховує бали"""
        # Спочатку знаходимо всі повні рядки та стовпці
        full_rows = []
        full_cols = []
        
        # Знаходимо всі повні рядки
        for row in range(self.size):
            if self.is_row_full(row):
                full_rows.append(row)
        
        # Знаходимо всі повні стовпці
        for col in range(self.size):
            if self.is_col_full(col):
                full_cols.append(col)
        
        # Очищаємо всі знайдені рядки та стовпці одночасно
        for row in full_rows:
            for col in range(self.size):
                self.cells[row][col] = None
        
        for col in full_cols:
            for row in range(self.size):
                self.cells[row][col] = None
        
        total_cleared = len(full_rows) + len(full_cols)
        points = total_cleared * 10

        # Бонуси за кілька ліній одночасно
        bonus = 0
        if total_cleared >= 2:
            if total_cleared == 2:
                bonus = 10
            elif total_cleared == 3:
                bonus = 20
            else:
                bonus = 30

        # --- Комбо-множник ---
        if total_cleared > 0:
            if self.last_clear_success:
                self.combo_multiplier += 1  # Збільшуємо множник
            else:
                self.combo_multiplier = 1  # Скидаємо множник
            self.last_clear_success = True
        else:
            self.combo_multiplier = 1
            self.last_clear_success = False

        self.score += (points + bonus) * self.combo_multiplier

        if total_cleared > 0:
            # Показуємо тільки важливу інформацію про очки та комбо
            if len(full_rows) > 0 and len(full_cols) > 0:
                print(f"🎯 Очищено {len(full_rows)} рядків + {len(full_cols)} стовпців! +{(points + bonus) * self.combo_multiplier} очок")
            elif len(full_rows) > 0:
                print(f"🎯 Очищено {len(full_rows)} рядків! +{(points + bonus) * self.combo_multiplier} очок")
            elif len(full_cols) > 0:
                print(f"🎯 Очищено {len(full_cols)} стовпців! +{(points + bonus) * self.combo_multiplier} очок")
            
            if bonus > 0:
                print(f"🎁 Бонус за кілька ліній: +{bonus}")
            if self.combo_multiplier > 1:
                print(f"🔥 КОМБО x{self.combo_multiplier}!")
        
        return total_cleared
    
        # ТЕСТОВА ФУНКЦІЯ (для перевірки)
    def fill_test_line(self):
        """Заповнює перший рядок для тестування"""
        for col in range(self.size):
            self.cells[0][col] = PIECE_RED  # Червоний колір для тесту
            
    # ВАЛІДАЦІЯ РОЗМІЩЕННЯ ФІГУР
    def mouse_to_grid(self, mouse_x, mouse_y, cell_size=GRID_CELL_SIZE):
        """Конвертує координати миші у координати сітки"""
        offset_x = (SCREEN_WIDTH - self.size * cell_size) // 2
        offset_y = (SCREEN_HEIGHT - self.size * cell_size) // 2
        
        grid_x = (mouse_x - offset_x) // cell_size
        grid_y = (mouse_y - offset_y) // cell_size
        
        return grid_x, grid_y
    
    def can_place_piece(self, piece, grid_x, grid_y):
        """Перевіряє, чи можна розмістити фігуру на позиції (grid_x, grid_y)"""
        # Перевіряємо кожну клітинку фігури
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col] == 1:  # Якщо є блок у фігурі
                    # Розраховуємо позицію на сітці
                    target_row = grid_y + row
                    target_col = grid_x + col
                    
                    # Перевіряємо межі сітки
                    if (target_row < 0 or target_row >= self.size or 
                        target_col < 0 or target_col >= self.size):
                        return False
                    
                    # Перевіряємо, чи клітинка вільна
                    if self.cells[target_row][target_col] is not None:
                        return False
        
        return True
    
    def place_piece(self, piece, grid_x, grid_y):
        """Розміщує фігуру на сітці"""
        if not self.can_place_piece(piece, grid_x, grid_y):
            return False
        
        # Розміщуємо фігуру
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col] == 1:
                    target_row = grid_y + row
                    target_col = grid_x + col
                    self.cells[target_row][target_col] = piece.color  # Зберігаємо колір фігури
        
        self.score += 1
        return True
    
    def highlight_position(self, surface, grid_x, grid_y, piece, cell_size=GRID_CELL_SIZE, valid=True):
        """Підсвічує позицію для розміщення фігури"""
        offset_x = (SCREEN_WIDTH - self.size * cell_size) // 2
        offset_y = (SCREEN_HEIGHT - self.size * cell_size) // 2
        
        # Колір підсвічування
        color = PREVIEW_VALID_COLOR if valid else PREVIEW_INVALID_COLOR  # Зелений або червоний
        
        # Створюємо поверхню з прозорістю
        highlight_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col] == 1:
                    target_row = grid_y + row
                    target_col = grid_x + col
                    
                    # Перевіряємо, чи в межах екрану
                    if (0 <= target_row < self.size and 0 <= target_col < self.size):
                        rect = pygame.Rect(
                            offset_x + target_col * cell_size,
                            offset_y + target_row * cell_size,
                            cell_size, cell_size
                        )
                        # Малюємо підсвічування
                        pygame.draw.rect(highlight_surface, color, (0, 0, cell_size, cell_size))
                        surface.blit(highlight_surface, rect.topleft)
    
    def print_grid_state(self, title="Стан сітки"):
        """Друкує поточний стан сітки для налагодження"""
        print(f"=== {title} ===")
        for row in range(self.size):
            row_str = ""
            for col in range(self.size):
                if self.cells[row][col] is None:
                    row_str += "⬜ "
                else:
                    row_str += "🟩 "
            print(f"Рядок {row}: {row_str}")
        print()
    
    def test_clearing_logic(self):
        """Тестує логіку очищення ліній"""
        print("=== ТЕСТ ЛОГІКИ ОЧИЩЕННЯ ===")
        
        # Очищаємо сітку
        for row in range(self.size):
            for col in range(self.size):
                self.cells[row][col] = None
        
        # Створюємо тестовий сценарій: заповнюємо стовпець 0, але залишаємо одну порожню клітинку
        for row in range(self.size):
            if row != 3:  # Залишаємо рядок 3 порожнім
                self.cells[row][0] = PIECE_RED  # Червоний колір
        
        # Заповнюємо стовпець 1 повністю
        for row in range(self.size):
            self.cells[row][1] = PIECE_GREEN  # Зелений колір
        
        print("Створений тестовий сценарій:")
        print("Стовпець 0: з одною порожньою клітинкою в рядку 3")
        print("Стовпець 1: повністю заповнений")
        
        self.print_grid_state("Тестовий стан")
        
        # Тестуємо перевірку стовпців
        print("Перевірка стовпців:")
        for col in range(2):
            is_full = self.is_col_full(col)
            print(f"Стовпець {col}: {'ПОВНИЙ' if is_full else 'НЕ ПОВНИЙ'}")
        
        # Очищаємо лінії
        self.clear_lines()