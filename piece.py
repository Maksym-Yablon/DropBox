from builtins import range
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
        # Кешуємо розміри фігури для оптимізації
        self._cached_dimensions = None
        # Додаємо можливість обертання
        self.rotation_angle = 0  # 0, 90, 180, 270 градусів

    def get_dimensions(self, cell_size):
        """Отримує розміри фігури з кешуванням"""
        if self._cached_dimensions is None or self._cached_dimensions[0] != cell_size:
            rows = len(self.shape)
            cols = len(self.shape[0]) if rows > 0 else 0
            width = cols * cell_size
            height = rows * cell_size
            self._cached_dimensions = (cell_size, width, height)
            return width, height
        return self._cached_dimensions[1], self._cached_dimensions[2]

    def rotate_90_clockwise(self):
        """Повертає фігуру на 90 градусів за годинниковою стрілкою"""
        if not self.shape:
            return
        
        rows = len(self.shape)
        cols = len(self.shape[0])
        
        # Створюємо нову матрицю повернену на 90 градусів
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = self.shape[i][j]
        
        self.shape = rotated
        self.rotation_angle = (self.rotation_angle + 90) % 360
        # Очищаємо кеш розмірів після обертання
        self._cached_dimensions = None

    def rotate_90_counterclockwise(self):
        """Повертає фігуру на 90 градусів проти годинникової стрілки"""
        # Поворот на 90 градусів проти годинникової = 3 повороти за годинниковою
        for _ in range(3):
            self.rotate_90_clockwise()

    def can_rotate(self):
        """Перевіряє, чи можна повернути фігуру (деякі фігури симетричні)"""
        # Квадрати та одиночні блоки не потрібно повертати
        if isinstance(self, (SingleBlock, Square, Square3x3)):
            return False
        return True

    def draw(self, surface, start_x, start_y, cell_size=GRID_CELL_SIZE, alpha=255):
        """Малює фігуру на екрані використовуючи спрайти або кольори"""
        from constants import get_block_sprite
        
        # Кешування позицій блоків для оптимізації
        cache_key = (id(self.shape), cell_size)
        if not hasattr(self, '_block_positions') or self._last_cache_key != cache_key:
            self._block_positions = []
            for row in range(len(self.shape)):
                for col in range(len(self.shape[row])):
                    if self.shape[row][col] == 1:
                        self._block_positions.append((row, col))
            self._last_cache_key = cache_key
        
        # Розрахунок розміру спрайту з кращими відступами
        sprite_margin = max(2, PIECE_MARGIN )  # Більший відступ для спрайтів
        sprite_size = cell_size - sprite_margin

        # Отримуємо спрайт для цього кольору
        sprite = get_block_sprite(self.color, sprite_size)
        
        # Оптимізація: створюємо поверхню тільки один раз для всієї фігури з прозорістю
        if alpha < 255:
            # Розраховуємо загальний розмір фігури
            width, height = self.get_dimensions(cell_size)
            if width > 0 and height > 0:
                # Створюємо одну поверхню для всієї фігури
                figure_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                
                for row, col in self._block_positions:
                    # Центруємо спрайт у клітинці
                    block_x = col * cell_size + (cell_size - sprite_size) // 2
                    block_y = row * cell_size + (cell_size - sprite_size) // 2
                    
                    if sprite:
                        # Використовуємо спрайт з прозорістю
                        sprite_with_alpha = sprite.copy()
                        sprite_with_alpha.set_alpha(alpha)
                        figure_surface.blit(sprite_with_alpha, (block_x, block_y))
                    else:
                        # Fallback до кольорових прямокутників
                        margin = PIECE_MARGIN
                        rect = pygame.Rect(
                            col * cell_size + margin,
                            row * cell_size + margin,
                            cell_size - 2 * margin, 
                            cell_size - 2 * margin
                        )
                        color_with_alpha = (*self.color, alpha)
                        pygame.draw.rect(figure_surface, color_with_alpha, rect)
                        outline_with_alpha = (*PIECE_OUTLINE_COLOR, alpha)
                        pygame.draw.rect(figure_surface, outline_with_alpha, rect, 1)
                
                surface.blit(figure_surface, (start_x, start_y))
        else:
            # Звичайне малювання без прозорості
            for row, col in self._block_positions:
                # Центруємо спрайт у клітинці
                block_x = start_x + col * cell_size + (cell_size - sprite_size) // 2
                block_y = start_y + row * cell_size + (cell_size - sprite_size) // 2
                
                if sprite:
                    # Використовуємо спрайт
                    surface.blit(sprite, (block_x, block_y))
                else:
                    # Fallback до кольорових прямокутників
                    margin = PIECE_MARGIN
                    rect = pygame.Rect(
                        start_x + col * cell_size + margin,
                        start_y + row * cell_size + margin,
                        cell_size - 2 * margin, 
                        cell_size - 2 * margin
                    )
                    pygame.draw.rect(surface, self.color, rect)
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


class ZShape(Piece):
    """Z-подібна фігура"""
    
    def __init__(self, color=PIECE_RED):  # Червоний колір
        shape = [
            [1, 1, 0],
            [0, 1, 1]
        ]
        super().__init__(shape, color)


class Cross(Piece):
    """Хрест (плюс)"""
    
    def __init__(self, color=PIECE_GREEN):  # Зелений колір
        shape = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]
        super().__init__(shape, color)


class Corner(Piece):
    """Кутова фігура"""
    
    def __init__(self, color=PIECE_BLUE):  # Синій колір
        shape = [
            [1, 1],
            [1, 0]
        ]
        super().__init__(shape, color)


class Line3(Piece):
    """Лінія з 3 блоків"""
    
    def __init__(self, color=PIECE_ORANGE):  # Помаранчевий колір
        shape = [
            [1, 1, 1]
        ]
        super().__init__(shape, color)


class SmallT(Piece):
    """Маленький T"""
    
    def __init__(self, color=PIECE_PINK):  # Рожевий колір
        shape = [
            [1, 1, 1],
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
    TShape,
    ZShape,
    Cross,
    Corner,
    Line3,
    SmallT
]


def generate_weighted_random_piece():
    """Генерує випадкову фігуру з урахуванням шансів появи з constants.py"""
    # Отримуємо всі фігури з їх шансами
    available_pieces = []
    weights = []
    
    # Створюємо словник відповідності класу та його назви
    piece_name_map = {
        SingleBlock: 'SingleBlock',
        Square: 'Square', 
        Square3x3: 'Square3x3',
        Line: 'Line',
        Line2x1: 'Line2x1',
        Line3x1: 'Line3x1',
        LShape: 'LShape',
        TShape: 'TShape',
        ZShape: 'ZShape',
        Cross: 'Cross',
        Corner: 'Corner',
        Line3: 'Line3',
        SmallT: 'SmallT'
    }
    
    # Збираємо доступні фігури та їх ваги
    for piece_class in PIECE_TYPES:
        piece_name = piece_name_map.get(piece_class)
        if piece_name and piece_name in PIECE_SPAWN_CHANCES:
            chance = PIECE_SPAWN_CHANCES[piece_name]
            if chance > 0:  # Додаємо тільки фігури з шансом > 0%
                available_pieces.append(piece_class)
                weights.append(chance)
    
    # Якщо немає доступних фігур (всі шанси 0%), використовуємо SingleBlock
    if not available_pieces:
        return SingleBlock()
    
    # Використовуємо weighted random choice
    total_weight = sum(weights)
    if total_weight == 0:
        return SingleBlock()
    
    # Генеруємо випадкове число від 0 до загальної ваги
    random_value = random.randint(1, total_weight)
    
    # Знаходимо відповідну фігуру
    current_weight = 0
    for i, weight in enumerate(weights):
        current_weight += weight
        if random_value <= current_weight:
            return available_pieces[i]()
    
    # Fallback (не повинно статися)
    return available_pieces[-1]()


def generate_three_pieces():
    """Генерує 3 фігури для вибору з урахуванням шансів появи"""
    return [generate_weighted_random_piece() for _ in range(3)]


class PieceBox:
    def __init__(self, start_x, start_y, width=PIECE_CONTAINER_WIDTH, height=PIECE_CONTAINER_HEIGHT):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cell_size = PIECE_CONTAINER_CELL_SIZE  # Менший розмір для контейнера
        self.spacing = 40    # Збільшили відступ між фігурами
        
        # 3 фігури в коробці (з урахуванням шансів)
        self.pieces = [
            generate_weighted_random_piece(),
            generate_weighted_random_piece(),
            generate_weighted_random_piece()
        ]
        
        # Наступна фігура (одна для всіх слотів)
        self.next_piece = generate_weighted_random_piece()
        
        # Індекс фігури, яку зараз перетягують (для показу preview)
        self.dragging_index = None
        
        # Обчислюємо позиції фігур з урахуванням їх розмірів
        self._calculate_piece_positions()
    
    def _get_piece_dimensions(self, piece):
        """Отримує розміри фігури в пікселях (використовує кешований метод)"""
        if not piece or not piece.shape:
            return 0, 0
        return piece.get_dimensions(self.cell_size)
    
    def _calculate_piece_positions(self):
        """Обчислює центровані позиції для кожної фігури з оптимізованим вирівнюванням"""
        self.piece_slots = []
        
        # Знаходимо максимальні розміри серед всіх фігур (включаючи наступну)
        max_width = 0
        max_height = 0
        
        # Перевіряємо всі поточні фігури
        for piece in self.pieces:
            width, height = self._get_piece_dimensions(piece)
            max_width = max(max_width, width)
            max_height = max(max_height, height)
        
        # Також перевіряємо наступну фігуру
        if self.next_piece:
            width, height = self._get_piece_dimensions(self.next_piece)
            max_width = max(max_width, width)
            max_height = max(max_height, height)
        
        # Розраховуємо розмір унітарного слоту з більшими відступами
        slot_width = max_width + 25   # Збільшили відступ
        slot_height = max_height + 35 # Збільшили вертикальний відступ для запобігання перекриттю
        
        # Загальна висота всіх слотів + відступи між ними
        total_height = len(self.pieces) * slot_height + (len(self.pieces) - 1) * self.spacing
        
        # Центруємо весь блок слотів у контейнері
        start_y = (self.height - total_height) // 2
        start_y = max(start_y, 15)  # Мінімальний відступ зверху
        
        # Розраховуємо позиції для кожного слоту
        current_y = start_y
        
        for i, piece in enumerate(self.pieces):
            piece_width, piece_height = self._get_piece_dimensions(piece)
            
            # Центруємо фігуру горизонтально в контейнері
            center_x = (self.width - piece_width) // 2
            
            # Центруємо фігуру вертикально у її слоті
            center_y = current_y + (slot_height - piece_height) // 2
            
            # Зберігаємо позицію та розмір слоту
            self.piece_slots.append((center_x, center_y))
            
            # Переходимо до наступного слоту
            current_y += slot_height + self.spacing
        
        # Зберігаємо розміри слоту для використання в draw()
        self.slot_width = slot_width
        self.slot_height = slot_height
    
    def _get_piece_at_position(self, mouse_x, mouse_y):
        """Спільна логіка для знаходження фігури за позицією (оптимізація)"""
        # Перевіряємо, чи миша всередині контейнера
        if not (self.start_x <= mouse_x <= self.start_x + self.width and 
                self.start_y <= mouse_y <= self.start_y + self.height):
            return None, None, None, None, None
            
        # Перевіряємо кожну фігуру в її слоті
        for i, (slot_x, slot_y) in enumerate(self.piece_slots):
            piece = self.pieces[i]
            piece_width, piece_height = self._get_piece_dimensions(piece)
            
            # Абсолютні координати фігури
            abs_x = self.start_x + slot_x
            abs_y = self.start_y + slot_y
            
            # Перевіряємо, чи клік потрапив у фігуру
            if (abs_x <= mouse_x <= abs_x + piece_width and 
                abs_y <= mouse_y <= abs_y + piece_height):
                
                # Розраховуємо зміщення кліку відносно початку фігури
                offset_x = mouse_x - abs_x
                offset_y = mouse_y - abs_y
                return i, piece, abs_x, abs_y, (offset_x, offset_y)
        
        return None, None, None, None, None

    def get_piece_at_mouse(self, mouse_x, mouse_y):
        """Перевіряє, чи клікнули на фігуру в коробці з урахуванням слотів"""
        piece_index, piece, abs_x, abs_y, offset = self._get_piece_at_position(mouse_x, mouse_y)
        if piece_index is not None:
            offset_x, offset_y = offset
            
            # ВИПРАВЛЕННЯ: Перевіряємо, чи клік потрапив саме на блок фігури (зі значенням 1)
            block_col = offset_x // self.cell_size
            block_row = offset_y // self.cell_size
            
            # Якщо клік потрапив на порожнє місце (0), то не беремо фігуру
            if (0 <= block_row < len(piece.shape) and 
                0 <= block_col < len(piece.shape[0]) and
                piece.shape[block_row][block_col] == 1):
                
                return piece_index, offset_x, offset_y
            else:
                # Клік потрапив на порожнє місце - не беремо фігуру
                return None, None, None
        return None, None, None

    def get_block_position_in_piece(self, mouse_x, mouse_y):
        """Визначає, за який блок фігури взялися з урахуванням слотів"""
        piece_index, piece, abs_x, abs_y, offset = self._get_piece_at_position(mouse_x, mouse_y)
        if piece_index is not None:
            offset_x, offset_y = offset
            
            # Визначаємо блок фігури
            block_col = offset_x // self.cell_size
            block_row = offset_y // self.cell_size
            
            # ВИПРАВЛЕННЯ: Перевіряємо, чи це дійсно блок фігури (зі значенням 1)
            if (0 <= block_row < len(piece.shape) and 
                0 <= block_col < len(piece.shape[0]) and
                piece.shape[block_row][block_col] == 1):
                
                return piece_index, block_col, block_row
                    
        return None, None, None

    def start_dragging(self, piece_index):
        """Починає перетягування фігури"""
        if 0 <= piece_index < len(self.pieces):
            self.dragging_index = piece_index

    def stop_dragging(self, piece_placed=False):
        """Зупиняє перетягування фігури"""
        if self.dragging_index is not None:
            if piece_placed:
                # Фігуру розміщено на сітці - замінюємо на ту, що показували під час перетягування
                self.pieces[self.dragging_index] = self.next_piece
                # Генеруємо нову наступну фігуру тільки після заміни
                self.next_piece = generate_weighted_random_piece()
                self._calculate_piece_positions()
            # Якщо фігуру не розміщено, вона просто повертається на місце
            self.dragging_index = None

    def replace_piece(self, piece_index):
        """Замінює фігуру на наступну (для сумісності - краще використовувати stop_dragging)"""
        if 0 <= piece_index < len(self.pieces):
            self.pieces[piece_index] = self.next_piece
            self.next_piece = generate_weighted_random_piece()
            # Перераховуємо позиції після заміни фігури
            self._calculate_piece_positions()

    def rotate_piece(self, piece_index):
        """Повертає фігуру в контейнері на 90 градусів за годинниковою стрілкою"""
        if 0 <= piece_index < len(self.pieces):
            piece = self.pieces[piece_index]
            if piece.can_rotate():
                piece.rotate_90_clockwise()
                # Перераховуємо позиції після обертання
                self._calculate_piece_positions()
                return True
        return False

    def draw(self, surface):
        """Малює всі фігури в коробці з правильним вирівнюванням наступної фігури"""
        for i, (slot_x, slot_y) in enumerate(self.piece_slots):
            
            if i == self.dragging_index:
                # Малюємо наступну фігуру замість перетягуваної
                next_piece_width, next_piece_height = self._get_piece_dimensions(self.next_piece)
                
                # Центруємо наступну фігуру горизонтально в контейнері
                preview_x = self.start_x + (self.width - next_piece_width) // 2
                
                # ВИПРАВЛЕННЯ: Центруємо відносно верхньої та нижньої фігур
                if i == 0:  # Верхня позиція
                    # Центруємо між верхом контейнера та наступною фігурою
                    if len(self.piece_slots) > 1:
                        next_slot_y = self.piece_slots[1][1]
                        available_space = (self.start_y + next_slot_y) - self.start_y
                        preview_y = self.start_y + (available_space - next_piece_height) // 2
                    else:
                        preview_y = self.start_y + (self.height - next_piece_height) // 2
                elif i == len(self.piece_slots) - 1:  # Нижня позиція
                    # Центруємо між попередньою фігурою та низом контейнера
                    prev_slot_y = self.piece_slots[i-1][1]
                    prev_piece_height = self._get_piece_dimensions(self.pieces[i-1])[1]
                    prev_bottom = self.start_y + prev_slot_y + prev_piece_height
                    container_bottom = self.start_y + self.height
                    available_space = container_bottom - prev_bottom
                    preview_y = prev_bottom + (available_space - next_piece_height) // 2
                else:  # Середня позиція
                    # Центруємо між попередньою та наступною фігурами
                    prev_slot_y = self.piece_slots[i-1][1]
                    next_slot_y = self.piece_slots[i+1][1]
                    prev_piece_height = self._get_piece_dimensions(self.pieces[i-1])[1]
                    
                    prev_bottom = self.start_y + prev_slot_y + prev_piece_height
                    next_top = self.start_y + next_slot_y
                    available_space = next_top - prev_bottom
                    preview_y = prev_bottom + (available_space - next_piece_height) // 2
                
                # Малюємо тільки наступну фігуру з прозорістю (з меншим розміром контейнера)
                self.next_piece.draw(surface, preview_x, preview_y, self.cell_size, alpha=128)
                
            else:  # Звичайні фігури (не перетягувані)
                # Малюємо фігуру на її розрахованій позиції (з меншим розміром контейнера)
                abs_x = self.start_x + slot_x  
                abs_y = self.start_y + slot_y
                self.pieces[i].draw(surface, abs_x, abs_y, self.cell_size)
    
    def draw_box_outline(self, surface):
        """Малює рамку коробки"""
        pygame.draw.rect(surface, PIECE_OUTLINE_COLOR, 
                        (self.start_x, self.start_y, self.width, self.height), 2)

