import pygame
from constants import*


class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = 0
        self.y = 0

    def draw(self, surface, start_x, start_y, cell_size=50):
    # малює фігуру на екрані
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] == 1:  # Якщо є блок
                    rect = pygame.Rect(
                        start_x + col * cell_size,
                        start_y + row * cell_size,
                        cell_size, cell_size
                    )
                    pygame.draw.rect(surface, self.color, rect)
                    pygame.draw.rect(surface, (0, 0, 0), rect, 2)
        

class SingleBlock(Piece):
    #Одиночний блок 1x1
        def __init__(self, color=(255, 255, 0)):  # Жовтий колір за замовчуванням
            shape = [[1]]  # Матриця 1x1 з одним блоком
            super().__init__(shape, color)


class LShape(Piece):
    """L-подібна фігура"""
    pass

class Square(Piece):
    """Квадратна фігура 2x2, 3x3"""
    pass

class LShape(Piece):
    """L-подібна фігура"""
    def __init__(self, color=(255, 192, 203)):  # Рожевий колір
        shape = [
            [1, 0],
            [1, 0],
            [1, 1]
        ]
        super().__init__(shape, color)

class TShape(Piece):
    """Т-подібна фігура"""
    def __init__(self, color=(0, 255, 255)):  # Блакитний колір
        shape = [
            [1, 1, 1],
            [0, 1, 0]
        ]
        super().__init__(shape, color)

