import pygame

# ===== РОЗМІРИ ТА ПОЗИЦІЇ =====
# Розміри екрану
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700

# Розміри клітинок
GRID_CELL_SIZE = 50  # Розмір клітинки сітки
PIECE_CELL_SIZE = 50  # Розмір клітинки для фігур
PIECE_CONTAINER_CELL_SIZE = 40  # Менший розмір для фігур у контейнері

# Параметри сітки
GRID_SIZE = 8  # Розмір сітки 8x8
GRID_COLS = GRID_SIZE
GRID_ROWS = GRID_SIZE

# Позиція сітки на екрані (центрована)
GRID_X = (SCREEN_WIDTH - GRID_SIZE * GRID_CELL_SIZE) // 2
GRID_Y = (SCREEN_HEIGHT - GRID_SIZE * GRID_CELL_SIZE) // 2

# Контейнер для фігур
PIECE_CONTAINER_WIDTH = 250
PIECE_CONTAINER_HEIGHT = 550  # Збільшено на 10% (500 * 1.1)

# Відступи та поля
PIECE_MARGIN = 1  # Відступ між блоками фігури

# Розміри кнопок
BUTTON_WIDTH_LARGE = 300
BUTTON_WIDTH_MEDIUM = 200
BUTTON_WIDTH_SMALL = 150
BUTTON_HEIGHT = 60

# ===== КОЛЬОРИ БЛОКІВ ФІГУР =====
# Основні кольори фігур
PIECE_YELLOW = (255, 255, 0)
PIECE_GREEN = (0, 255, 0)
PIECE_RED = (255, 0, 0)
PIECE_BLUE = (0, 0, 255)
PIECE_ORANGE = (255, 165, 0)
PIECE_PINK = (255, 192, 203)
PIECE_CYAN = (0, 255, 255)

# Контури блоків
PIECE_OUTLINE_COLOR = (128, 128, 128)

# ===== КОЛЬОРИ СІТКИ =====
# Сітка
GRID_LINE_COLOR = (48, 48, 96)
EMPTY_CELL_COLOR = (139, 69, 19)  # Коричневий для порожніх клітинок

# ===== КОЛЬОРИ ІНТЕРФЕЙСУ =====
# Базові кольори
BACKGROUND_COLOR = (32, 32, 64)
TEXT_COLOR = (255, 255, 255)
TEXT_COLOR_BLACK = (0, 0, 0)

# Кольори кнопок
BUTTON_COLOR = (64, 128, 192)
BUTTON_HOVER_COLOR = (96, 160, 224)

# Кольори контейнера для фігур
PIECE_BOX_BORDER_COLOR = (139, 69, 19)  # Коричневий як у сітки
PIECE_BOX_FILL_COLOR = (205, 133, 63)   # Світло-коричневий

# ===== КОЛЬОРИ ЕФЕКТІВ =====
# Кольори попереднього перегляду (зелені відтінки)
PREVIEW_VALID_COLOR = (0, 255, 0, 80)      # Зелений з прозорістю
PREVIEW_INVALID_COLOR = (255, 0, 0, 80)    # Червоний з прозорістю

# Кольори для очищення ліній
CLEAR_EFFECT_COLOR = (255, 255, 255, 200)  # Білий з прозорістю

# ===== КОЛЬОРИ МЕНЮ ТА РЕКОРДІВ =====
# Медалі в таблиці рекордів
MEDAL_GOLD = (255, 215, 0)     # Золото
MEDAL_SILVER = (192, 192, 192) # Срібло  
MEDAL_BRONZE = (205, 127, 50)  # Бронза

# Кольори тексту в меню
MENU_TEXT_COLOR = (255, 255, 255)
MENU_TITLE_COLOR = (255, 255, 255)

# ===== ЗАСТАРІЛІ КОЛЬОРИ (для сумісності) =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (173, 216, 230)
KARATOVY = (255, 120, 18)
CARROT = (255, 160, 48)

# ===== ШРИФТИ =====
FONT_SIZE = 36
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# ===== ШАНСИ ПОЯВИ ФІГУР (0-100%) =====
# Налаштування шансів появи кожної фігури від 0% до 100%
# 0% = фігура ніколи не з'являється
# 100% = фігура з'являється дуже часто
PIECE_SPAWN_CHANCES = {
    'SingleBlock': 20,    # 20% - часто (основна фігура)
    'Square': 15,         # 15% - досить часто
    'Square3x3': 3,       # 3% - рідко (велика фігура)
    'Line': 18,           # 18% - часто
    'Line2x1': 18,        # 18% - часто  
    'Line3x1': 8,         # 8% - середньо (довга фігура)
    'LShape': 12,         # 12% - середньо
    'TShape': 10,         # 10% - середньо
    'ZShape': 8,          # 8% - середньо
    'Cross': 6,           # 6% - рідше (складна форма)
    'Corner': 14,         # 14% - досить часто
    'Line3': 16,          # 16% - часто
    'SmallT': 12          # 12% - середньо
}

# ===== ПАНЕЛЬ КЕРУВАННЯ =====
# Розміри панелі керування
CONTROL_PANEL_WIDTH = 200
CONTROL_PANEL_HEIGHT = 300
CONTROL_PANEL_X = 50  # Ліва сторона екрану
CONTROL_PANEL_Y = 150

# Розміри кнопок панелі
CONTROL_BUTTON_WIDTH = 150
CONTROL_BUTTON_HEIGHT = 40
CONTROL_BUTTON_MARGIN = 15

# Кольори панелі керування
CONTROL_PANEL_BG = (45, 45, 75, 180)    # Темно-синій з прозорістю
CONTROL_PANEL_BORDER = (100, 100, 150)   # Світло-синій для рамки
CONTROL_BUTTON_COLOR = (70, 130, 180)    # Сталево-синій
CONTROL_BUTTON_HOVER = (100, 149, 237)   # Корнфлавер синій
CONTROL_BUTTON_TEXT = (255, 255, 255)    # Білий текст

# ===== КНОПКА ПАУЗИ =====
# Кнопка паузи в нижньому лівому куті
PAUSE_BUTTON_SIZE = 50
PAUSE_BUTTON_X = 20
PAUSE_BUTTON_Y = SCREEN_HEIGHT - PAUSE_BUTTON_SIZE - 20
PAUSE_BUTTON_COLOR = (60, 60, 100, 180)  # Темний з прозорістю
PAUSE_BUTTON_HOVER = (80, 80, 120, 200)
PAUSE_BUTTON_BORDER = (120, 120, 160)

# ===== СПРАЙТИ БЛОКІВ =====
# Увімкнути/вимкнути використання спрайтів (True = спрайти, False = кольорові блоки)
USE_SPRITES = True

# Відповідність кольорів до файлів спрайтів
COLOR_TO_SPRITE = {
    PIECE_YELLOW: "assets/sprites/cats/white_block_cat.png",      # Жовтий -> білий кіт
    PIECE_GREEN: "assets/sprites/cats/mind_block_cat.png",        # Зелений -> м'ятний кіт  
    PIECE_RED: "assets/sprites/cats/red_block_cat.png",           # Червоний -> червоний кіт
    PIECE_BLUE: "assets/sprites/cats/blue_block_cat.png",         # Синій -> синій кіт
    PIECE_ORANGE: "assets/sprites/cats/orange_block_cat.png",     # Помаранчевий -> помаранчевий кіт
    PIECE_PINK: "assets/sprites/cats/pink_block_cat.png",         # Рожевий -> рожевий кіт
    PIECE_CYAN: "assets/sprites/cats/purple_block_cat.png",       # Блакитний -> фіолетовий кіт
}

# Кеш завантажених спрайтів
_sprite_cache = {}

def get_block_sprite(color, size):
    """Повертає спрайт блоку для заданого кольору та розміру з якісним масштабуванням"""
    # Якщо спрайти вимкнені, повертаємо None
    if not USE_SPRITES:
        return None
        
    if color not in COLOR_TO_SPRITE:
        return None
        
    sprite_path = COLOR_TO_SPRITE[color]
    cache_key = (sprite_path, size)
    
    if cache_key not in _sprite_cache:
        try:
            # Завантажуємо оригінальний спрайт (2048x2048)
            original_sprite = pygame.image.load(sprite_path)
            
            # Використовуємо smoothscale для якісного масштабування великих зображень
            # Це краще ніж звичайний scale для високорозширених зображень
            if size > 0:
                scaled_sprite = pygame.transform.smoothscale(original_sprite, (size, size))
            else:
                scaled_sprite = original_sprite
                
            _sprite_cache[cache_key] = scaled_sprite
            
        except pygame.error as e:
            # Якщо не вдалося завантажити спрайт, повертаємо None
            print(f"Помилка завантаження спрайту {sprite_path}: {e}")
            return None
    
    return _sprite_cache[cache_key]

# ===== ФУНКЦІЇ =====
def get_background_image():
    """Повертає фонове зображення з масштабуванням під розмір екрану"""
    return pygame.transform.scale(
        pygame.image.load("image/icon.png"), 
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
