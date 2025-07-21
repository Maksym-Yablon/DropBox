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
        """Обчислює центровані позиції для кожної фігури з горизонтальним розташуванням (адаптовано під мобільний)"""
        self.piece_slots = []
        
        if not self.pieces:
            return
        
        # Створюємо список фігур для розрахунку позицій
        # Якщо фігуру перетягують, замінюємо її на next_piece для розрахунків
        pieces_for_calculation = []
        for i, piece in enumerate(self.pieces):
            if i == self.dragging_index:
                # Використовуємо наступну фігуру замість перетягуваної
                pieces_for_calculation.append(self.next_piece)
            else:
                pieces_for_calculation.append(piece)
        
        # Отримуємо реальні розміри всіх фігур для горизонтального розташування
        piece_widths = []
        max_height = 0
        
        for piece in pieces_for_calculation:
            width, height = self._get_piece_dimensions(piece)
            piece_widths.append(width)
            max_height = max(max_height, height)
        
        # Розраховуємо адаптивні відступи для горизонтального розташування
        total_pieces_width = sum(piece_widths)
        average_piece_width = total_pieces_width / len(piece_widths) if piece_widths else 0
        
        # Базовий відступ залежить від середнього розміру фігур по ширині
        if average_piece_width <= 40:  # Маленькі фігури (1x1, 2x2)
            base_spacing = 20
        elif average_piece_width <= 80:  # Середні фігури (лінії 3x1, T-форми)
            base_spacing = 15
        else:  # Великі фігури (довгі лінії, великі квадрати)
            base_spacing = 10
        
        # Обчислюємо коефіцієнт заповнення контейнера по ширині
        container_padding = 20
        available_width = self.width - 2 * container_padding
        fill_ratio = total_pieces_width / available_width if available_width > 0 else 1
        
        # Адаптуємо відступи залежно від заповнення
        if fill_ratio > 0.8:  # Якщо контейнер заповнений більш ніж на 80%
            adaptive_spacing = max(3, base_spacing * (1 - fill_ratio) * 2)
        elif fill_ratio < 0.5:  # Якщо контейнер заповнений менш ніж на 50%
            adaptive_spacing = min(base_spacing * 1.5, 25)  # Збільшуємо відступи, але не більше 25
        else:
            adaptive_spacing = base_spacing
        
        total_spacing = adaptive_spacing * (len(pieces_for_calculation) - 1) if len(pieces_for_calculation) > 1 else 0
        total_required = total_pieces_width + total_spacing
        
        # Якщо фігури не влазять з адаптивними відступами, зменшуємо їх пропорційно
        if total_required > available_width and available_width > total_pieces_width:
            # Розподіляємо залишок простору на відступи
            remaining_space = available_width - total_pieces_width
            if len(pieces_for_calculation) > 1:
                actual_spacing = remaining_space / (len(pieces_for_calculation) - 1)
                actual_spacing = max(3, actual_spacing)  # Мінімальний відступ 3 пікселі
            else:
                actual_spacing = 0
        else:
            actual_spacing = adaptive_spacing
        
        # Розраховуємо стартову позицію по горизонталі (центрування)
        total_width_with_spacing = total_pieces_width + actual_spacing * (len(pieces_for_calculation) - 1) if len(pieces_for_calculation) > 1 else total_pieces_width
        start_x = (self.width - total_width_with_spacing) // 2
        start_x = max(start_x, container_padding // 2)  # Мінімальний відступ зліва
        
        # Додаткова перевірка: якщо все не влазить, починаємо зліва з мінімальним відступом
        if start_x + total_width_with_spacing > self.width - container_padding // 2:
            start_x = container_padding // 2
        
        # Розраховуємо позиції для кожної фігури (горизонтально)
        current_x = start_x
        
        for i, piece in enumerate(pieces_for_calculation):
            piece_width, piece_height = self._get_piece_dimensions(piece)
            
            # Центруємо фігуру вертикально в контейнері
            center_y = (self.height - piece_height) // 2
            
            # Позиція по горизонталі - використовуємо поточну позицію
            center_x = current_x
            
            # Зберігаємо позицію слота
            self.piece_slots.append((center_x, center_y, piece_width, piece_height))
            
            # Переходимо до наступної позиції (горизонтально)
            current_x += piece_width + (actual_spacing if i < len(pieces_for_calculation) - 1 else 0)
        
        # Зберігаємо максимальну висоту для використання в draw() (змінено з max_width)
        self.max_piece_height = max_height
    
    def _get_piece_at_position(self, mouse_x, mouse_y):
        """Спільна логіка для знаходження фігури за позицією (оптимізація)"""
        # Перевіряємо, чи миша всередині контейнера
        if not (self.start_x <= mouse_x <= self.start_x + self.width and 
                self.start_y <= mouse_y <= self.start_y + self.height):
            return None, None, None, None, None
            
        # Перевіряємо кожну фігуру в її слоті
        for i, (slot_x, slot_y, slot_width, slot_height) in enumerate(self.piece_slots):
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
            block_col = int(offset_x // self.cell_size)
            block_row = int(offset_y // self.cell_size)
            
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
            block_col = int(offset_x // self.cell_size)
            block_row = int(offset_y // self.cell_size)
            
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
            # Перераховуємо позиції з урахуванням наступної фігури
            self._calculate_piece_positions()

    def stop_dragging(self, piece_placed=False):
        """Зупиняє перетягування фігури"""
        if self.dragging_index is not None:
            if piece_placed:
                # Фігуру розміщено на сітці - замінюємо на ту, що показували під час перетягування
                self.pieces[self.dragging_index] = self.next_piece
                # Генеруємо нову наступну фігуру тільки після заміни
                self.next_piece = generate_weighted_random_piece()
            
            # Скидаємо індекс перетягування
            self.dragging_index = None
            # Перераховуємо позиції після завершення перетягування
            self._calculate_piece_positions()

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
                # Зберігаємо оригінальний стан фігури на випадок проблем
                original_shape = [row[:] for row in piece.shape]  # Глибока копія
                original_angle = piece.rotation_angle
                original_dimensions = piece._cached_dimensions
                
                # Повертаємо фігуру
                piece.rotate_90_clockwise()
                
                # Перераховуємо позиції всіх фігур з урахуванням нової форми
                self._calculate_piece_positions()
                
                # Перевіряємо, чи всі фігури влазять у контейнер після перерахунку
                if self._do_all_pieces_fit():
                    # Всі фігури влазять - зберігаємо поворот
                    print(f"✅ Фігуру повернено успішно")
                    return True
                else:
                    # Не всі фігури влазять - відновлюємо оригінальний стан
                    piece.shape = original_shape
                    piece.rotation_angle = original_angle
                    piece._cached_dimensions = original_dimensions
                    # Перераховуємо позиції з оригінальною фігурою
                    self._calculate_piece_positions()
                    print(f"⚠️ Неможливо повернути фігуру - не всі фігури влазять у контейнер")
                    return False
        return False

    def _do_all_pieces_fit(self):
        """Перевіряє, чи всі фігури влазять у контейнер з поточним розміщенням"""
        for i, (slot_x, slot_y, slot_width, slot_height) in enumerate(self.piece_slots):
            piece = self.pieces[i]
            piece_width, piece_height = self._get_piece_dimensions(piece)
            
            # Перевіряємо горизонтальні границі
            if slot_x < 0 or slot_x + piece_width > self.width:
                return False
            
            # Перевіряємо вертикальні границі
            if slot_y < 0 or slot_y + piece_height > self.height:
                return False
        
        return True

    def draw(self, surface):
        """Малює всі фігури в коробці з правильним урахуванням наступної фігури"""
        for i, (slot_x, slot_y, slot_width, slot_height) in enumerate(self.piece_slots):
            
            if i == self.dragging_index:
                # Малюємо наступну фігуру замість перетягуваної з прозорістю
                abs_x = self.start_x + slot_x
                abs_y = self.start_y + slot_y
                self.next_piece.draw(surface, abs_x, abs_y, self.cell_size, alpha=128)
            else:
                # Малюємо звичайну фігуру на її розрахованій позиції
                abs_x = self.start_x + slot_x  
                abs_y = self.start_y + slot_y
                self.pieces[i].draw(surface, abs_x, abs_y, self.cell_size)
    
    def draw_box_outline(self, surface):
        """Малює рамку коробки"""
        pygame.draw.rect(surface, PIECE_OUTLINE_COLOR, 
                        (self.start_x, self.start_y, self.width, self.height), 2)

