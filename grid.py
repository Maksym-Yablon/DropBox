import pygame
from main import SCREEN_WIDTH, SCREEN_HEIGHT
class Grid:
    def __init__(self, size=8):
        self.size = size
        self.cells = [[0 for _ in range(size)] for _ in range(size)]  # ігрова сітка
    
    def draw(self, surface, cell_size=60,):
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

    def is_row_full(self, row):
        # перевіряємо, чи рядок заповнений
        return all(self.cells[row][col] != 0 for col in range(self.size))
    
    def clear_full_rows (self):
        # очищаємо заповнені рядки
        cleared = 0
        for row in range(self.size):
            if self.is_row_full(row):
                for col in range(self.size):
                    self.cells[row][col] = 0  # очищаємо клітинки
                cleared += 1
        return cleared
