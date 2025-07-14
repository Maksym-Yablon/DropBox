import pygame
from constants import*  # Імпорт констант

class Grid:
    def __init__(self, size=8):
        self.size = size
        self.cells = [[0 for _ in range(size)] for _ in range(size)]  # ігрова сітка
        self.score = 0  # початковий рахунок
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
                color = (255, 255, 255) if self.cells[row][col] == 0 else (100, 180, 255)
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (50, 50, 50), rect, 1)  # рамка
    # ПЕРЕВІРКА РЯДКІВ
    def is_row_full(self, row):
        # перевіряємо, чи рядок заповнений
        return all(self.cells[row][col] != 0 for col in range(self.size))
    

    def is_col_full(self, col):
        # перевіряємо, чи стовпець заповнений  
        return all(self.cells[row][col] != 0 for row in range(self.size))    
    
    def clear_full_rows (self):
        # очищаємо заповнені рядки
        cleared = 0
        for row in range(self.size):
            if self.is_row_full(row):
                for col in range(self.size):
                    self.cells[row][col] = 0  # очищаємо клітинки
                cleared += 1
        return cleared
    
    def clear_full_cols(self):
        # очищаємо заповнені стовпці
        cleared = 0
        for col in range(self.size):
            if self.is_col_full(col):
                for row in range(self.size):
                    self.cells[row][col] = 0  # очищаємо клітинки
                cleared += 1
        return cleared
    
    # ГОЛОВНА ФУНКЦІЯ ОЧИЩЕННЯ
    def clear_lines(self):
        """Очищає всі повні лінії (рядки + стовпці) і нараховує бали"""
        cleared_rows = self.clear_full_rows()
        cleared_cols = self.clear_full_cols()
        
        total_cleared = cleared_rows + cleared_cols
        if total_cleared > 0:
            # Нараховуємо бали: 10 балів за кожну лінію
            points = total_cleared * 10
            self.score += points
            print(f"Очищено {cleared_rows} рядків і {cleared_cols} стовпців. +{points} балів!")
        
        return total_cleared
    
        # ТЕСТОВА ФУНКЦІЯ (для перевірки)
    def fill_test_line(self):
        """Заповнює перший рядок для тестування"""
        for col in range(self.size):
            self.cells[0][col] = 1