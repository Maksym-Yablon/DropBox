import pygame
import random
from constants import *


class Piece:
    """Базовий клас для всіх ігрових фігур"""
    
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = 0
        self.y = 0

    def draw(self, surface, start_x, start_y, cell_size=GRID_CELL_SIZE):
        """Малює фігуру на екрані з покращеним візуалом"""
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] == 1:  # Якщо є блок
                    # Відступ для візуального розділення блоків
                    margin = PIECE_MARGIN
                    rect = pygame.Rect(
                        start_x + col * cell_size + margin,
                        start_y + row * cell_size + margin,
                        cell_size - 2 * margin, 
                        cell_size - 2 * margin
                    )
                    
                    # Основний колір блоку
                    pygame.draw.rect(surface, self.color, rect)
                    
                    # Тонкий контур навколо блоку
                    pygame.draw.rect(surface, PIECE_OUTLINE_COLOR, rect, 1)


class SingleBlock(Piece):
    """Одиночний блок 1x1"""
    
    def __init__(self, color=PIECE_YELLOW):  # Жовтий колір за замовчуванням
        shape = [[1]]  # Матриця 1x1 з одним блоком
        super().__init__(shape, color)


class Square(Piece):
    """Квадрат 2x2"""
    
    def __init__(self, color=PIECE_GREEN):  # Зелений колір
        shape = [
            [1, 1],
            [1, 1]
        ]
        super().__init__(shape, color)


class Square3x3(Piece):
    """Квадрат 3x3"""
    
    def __init__(self, color=PIECE_RED):  # Червоний колір
        shape = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        super().__init__(shape, color)


class Line(Piece):
    """Пряма лінія 1x2"""
    
    def __init__(self, color=PIECE_BLUE):  # Синій колір
        shape = [
            [1, 1]
        ]
        super().__init__(shape, color)


class Line2x1(Piece):
    """Пряма лінія 2x1"""
    
    def __init__(self, color=PIECE_GREEN):  # Зелений колір
        shape = [
            [1],
            [1]
        ]
        super().__init__(shape, color)


class Line3x1(Piece):
    """Пряма лінія 1x4"""
    
    def __init__(self, color=PIECE_ORANGE):  # Помаранчевий колір
        shape = [
            [1, 1, 1, 1]
        ]
        super().__init__(shape, color)


class LShape(Piece):
    """L-подібна фігура"""
    
    def __init__(self, color=PIECE_PINK):  # Рожевий колір
        shape = [
            [1, 0],
            [1, 0],
            [1, 1]
        ]
        super().__init__(shape, color)


class TShape(Piece):
    """Т-подібна фігура"""
    
    def __init__(self, color=PIECE_CYAN):  # Блакитний колір
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
    Square3x3,
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
    def __init__(self, start_x, start_y, width=PIECE_CONTAINER_WIDTH, height=PIECE_CONTAINER_HEIGHT):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cell_size = PIECE_CELL_SIZE  # Розмір клітинки для фігур
        self.spacing = 30    # Відступ між фігурами
        
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
            return None, None, None
            
        # Перевіряємо кожну фігуру з урахуванням її реальних розмірів
        for i, (rel_x, rel_y) in enumerate(self.piece_slots):
            piece = self.pieces[i]
            piece_width, piece_height = self._get_piece_dimensions(piece)
            
            abs_x = self.start_x + rel_x
            abs_y = self.start_y + rel_y
            
            # Область кліку відповідає реальному розміру фігури
            if (abs_x <= mouse_x <= abs_x + piece_width and 
                abs_y <= mouse_y <= abs_y + piece_height):
                # Обчислюємо зміщення кліку відносно початку фігури
                offset_x = mouse_x - abs_x
                offset_y = mouse_y - abs_y
                return i, offset_x, offset_y
        
        return None, None, None
    
    def get_block_position_in_piece(self, mouse_x, mouse_y):
        """Визначає, за який блок фігури взялися (координати блоку в матриці фігури)"""
        # Перевіряємо, чи миша всередині коробки
        if not (self.start_x <= mouse_x <= self.start_x + self.width and 
                self.start_y <= mouse_y <= self.start_y + self.height):
            return None, None, None
            
        # Перевіряємо кожну фігуру
        for i, (rel_x, rel_y) in enumerate(self.piece_slots):
            piece = self.pieces[i]
            piece_width, piece_height = self._get_piece_dimensions(piece)
            
            abs_x = self.start_x + rel_x
            abs_y = self.start_y + rel_y
            
            # Перевіряємо, чи клік в межах фігури
            if (abs_x <= mouse_x <= abs_x + piece_width and 
                abs_y <= mouse_y <= abs_y + piece_height):
                
                # Обчислюємо зміщення кліку відносно початку фігури
                offset_x = mouse_x - abs_x
                offset_y = mouse_y - abs_y
                
                # Визначаємо, на який блок фігури клікнули
                block_col = offset_x // self.cell_size
                block_row = offset_y // self.cell_size
                
                # Перевіряємо, чи це дійсно блок фігури (а не порожнє місце)
                if (0 <= block_row < len(piece.shape) and 
                    0 <= block_col < len(piece.shape[0]) and
                    piece.shape[block_row][block_col] == 1):
                    
                    return i, block_col, block_row
                    
        return None, None, None

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
        pygame.draw.rect(surface, PIECE_OUTLINE_COLOR, 
                        (self.start_x, self.start_y, self.width, self.height), 2)

