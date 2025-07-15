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

class Square(Piece):
    """Квадрат 2x2"""
    def __init__(self, color=(0, 255, 0)):  # Зелений колір
        shape = [
            [1, 1],
            [1, 1]
        ]
        super().__init__(shape, color)

class square3x3(Piece):
    """Квадрат 3x3"""
    def __init__(self, color=(255, 0, 0)):  # Червоний колір
        shape = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        super().__init__(shape, color)

class Line(Piece):
    """Пряма лінія 1x2"""
    def __init__(self, color=(0, 0, 255)):  # Синій колір
        shape = [
            [1, 1]
        ]
        super().__init__(shape, color)

class Line2x1(Piece):
    """Пряма лінія 2x1"""
    def __init__(self, color=(0, 255, 0)):  # Зелений колір
        shape = [
            [1],
            [1]
        ]
        super().__init__(shape, color)

class Line3x1(Piece):
    """Пряма лінія 1x4"""
    def __init__(self, color=(255, 165, 0)):  # Помаранчевий колір
        shape = [
            [1, 1, 1, 1]
        ]
        super().__init__(shape, color)


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
            [0, 1, 0],
            [0, 1, 0]
        ]
        super().__init__(shape, color)

# Список всіх доступних фігур
PIECE_TYPES = [
    SingleBlock,
    Square,
    square3x3,
    Line,
    Line2x1,
    Line3x1,
    LShape,
    TShape
]

def generate_random_piece():
    """Генерує випадкову фігуру"""
    import random
    piece_class = random.choice(PIECE_TYPES)
    return piece_class()

def generate_three_pieces():
    """Генерує 3 фігури для вибору (як у Block Blast)"""
    return [generate_random_piece() for _ in range(3)]

class PieceBox:
    """Невидима коробка для розміщення 3 фігур"""
    def __init__(self, start_x, start_y, width=250, height=500):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cell_size = 48  # Розмір клітинки для фігур
        self.spacing = 30    # Збільшений відступ між фігурами
        
        # 3 фігури в коробці
        self.pieces = [
            generate_random_piece(),
            generate_random_piece(),
            generate_random_piece()
        ]
        
        # Обчислюємо позиції фігур з урахуванням їх розмірів
        self._calculate_piece_positions()
    
    def _get_piece_dimensions(self, piece):
        """Отримує розміри фігури в пікселях"""
        if not piece or not piece.shape:
            return 0, 0
        
        rows = len(piece.shape)
        cols = len(piece.shape[0]) if rows > 0 else 0
        
        width = cols * self.cell_size
        height = rows * self.cell_size
        
        return width, height
    
    def _calculate_piece_positions(self):
        """Обчислює центровані позиції для кожної фігури з урахуванням відступів"""
        self.piece_slots = []
        
        # Отримуємо висоти всіх фігур
        piece_heights = []
        for piece in self.pieces:
            _, height = self._get_piece_dimensions(piece)
            piece_heights.append(height)
        
        # Обчислюємо загальну висоту всіх фігур + відступи
        total_pieces_height = sum(piece_heights) + (self.spacing * (len(self.pieces) - 1))
        
        # Початкова позиція по Y (центруємо весь блок фігур)
        start_y = (self.height - total_pieces_height) // 2
        start_y = max(start_y, self.spacing)  # Мінімальний відступ зверху
        
        current_y = start_y
        
        for i, piece in enumerate(self.pieces):
            piece_width, piece_height = self._get_piece_dimensions(piece)
            
            # Центруємо фігуру по горизонталі
            center_x = (self.width - piece_width) // 2
            
            # Додаємо позицію для поточної фігури
            self.piece_slots.append((center_x, current_y))
            
            # Переміщуємося на наступну позицію (висота фігури + відступ)
            current_y += piece_height + self.spacing
    
    def get_piece_at_mouse(self, mouse_x, mouse_y):
        """Перевіряє, чи клікнули на фігуру в коробці"""
        # Перевіряємо, чи миша всередині коробки
        if not (self.start_x <= mouse_x <= self.start_x + self.width and 
                self.start_y <= mouse_y <= self.start_y + self.height):
            return None
            
        # Перевіряємо кожну фігуру з урахуванням її реальних розмірів
        for i, (rel_x, rel_y) in enumerate(self.piece_slots):
            piece = self.pieces[i]
            piece_width, piece_height = self._get_piece_dimensions(piece)
            
            abs_x = self.start_x + rel_x
            abs_y = self.start_y + rel_y
            
            # Область кліку відповідає реальному розміру фігури
            if (abs_x <= mouse_x <= abs_x + piece_width and 
                abs_y <= mouse_y <= abs_y + piece_height):
                return i
        
        return None
    
    def replace_piece(self, piece_index):
        """Замінює фігуру на нову випадкову"""
        if 0 <= piece_index < len(self.pieces):
            self.pieces[piece_index] = generate_random_piece()
            # Перераховуємо позиції після заміни фігури
            self._calculate_piece_positions()
    
    def draw(self, surface, dragging_index=None):
        """Малює всі фігури в коробці (крім тої, що перетягується)"""
        for i, (rel_x, rel_y) in enumerate(self.piece_slots):
            if i != dragging_index:  # Не малюємо фігуру, яку перетягуємо
                abs_x = self.start_x + rel_x
                abs_y = self.start_y + rel_y
                self.pieces[i].draw(surface, abs_x, abs_y, self.cell_size)
    
    def draw_box_outline(self, surface):
        """Малює рамку коробки"""
        pygame.draw.rect(surface, (100, 100, 100), 
                        (self.start_x, self.start_y, self.width, self.height), 2)

