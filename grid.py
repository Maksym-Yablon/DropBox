import pygame
from constants import*  # Імпорт констант

class Grid:
    def __init__(self, size=8):
        self.size = size
        self.cells = [[None for _ in range(size)] for _ in range(size)]  # ігрова сітка
        self.score = 0  # початковий рахунок
        self.combo_multiplier = 1  # множник комбо
        self.last_clear_success = False

    def draw(self, surface, cell_size=50):
        offset_x = (SCREEN_WIDTH - self.size * cell_size) // 2
        offset_y = (SCREEN_HEIGHT - self.size * cell_size) // 2
        #малюємо сітку
        for row in range(self.size):
            for col in range(self.size):
                rect = pygame.Rect(
                    offset_x + col * cell_size,
                    offset_y + row * cell_size,
                    cell_size, cell_size
                )
                
                if self.cells[row][col] is None:
                    color = (125, 78, 23)  # Порожня клітинка
                else:
                    color = self.cells[row][col]  # Колір фігури
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, CARROT, rect, 1)  # рамка
                
    # ПЕРЕВІРКА РЯДКІВ
    def is_row_full(self, row):
        # перевіряємо, чи рядок заповнений
        return all(self.cells[row][col] is not None for col in range(self.size))
    

    def is_col_full(self, col):
        # перевіряємо, чи стовпець заповнений  
        return all(self.cells[row][col] is not None for row in range(self.size))    
    
    def clear_full_rows (self):
        # очищаємо заповнені рядки
        cleared = 0
        for row in range(self.size):
            if self.is_row_full(row):
                for col in range(self.size):
                    self.cells[row][col] = None  # очищаємо клітинки до None
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
            print(f"Очищено {len(full_rows)} рядків і {len(full_cols)} стовпців. +{points} балів! Бонус: +{bonus}")
        

        return total_cleared
    
        # ТЕСТОВА ФУНКЦІЯ (для перевірки)
    def fill_test_line(self):
        """Заповнює перший рядок для тестування"""
        for col in range(self.size):
            self.cells[0][col] = (255, 0, 0)  # Червоний колір для тесту
            
    # ВАЛІДАЦІЯ РОЗМІЩЕННЯ ФІГУР
    def mouse_to_grid(self, mouse_x, mouse_y, cell_size=50):
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
    
    def highlight_position(self, surface, grid_x, grid_y, piece, cell_size=50, valid=True):
        """Підсвічує позицію для розміщення фігури"""
        offset_x = (SCREEN_WIDTH - self.size * cell_size) // 2
        offset_y = (SCREEN_HEIGHT - self.size * cell_size) // 2
        
        # Колір підсвічування
        color = (0, 255, 0, 100) if valid else (255, 0, 0, 100)  # Зелений або червоний
        
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