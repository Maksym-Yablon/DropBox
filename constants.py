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
# М'які кольори фігур для темної теми (приглушені, без різкості)
PIECE_YELLOW = (218, 195, 120)    # М'який золотистий
PIECE_GREEN = (144, 184, 144)     # М'який зелений
PIECE_RED = (192, 120, 120)       # М'який червоний
PIECE_BLUE = (120, 150, 192)      # М'який синій
PIECE_ORANGE = (210, 160, 120)    # М'який помаранчевий
PIECE_PINK = (192, 144, 168)      # М'який рожевий
PIECE_CYAN = (120, 180, 180)      # М'який бірюзовий

# Контури блоків
PIECE_OUTLINE_COLOR = (80, 80, 80)  # Темно-сірий контур

# ===== КОЛЬОРИ СІТКИ =====
# Темна сітка з м'якими золотистими акцентами
GRID_BACKGROUND_COLOR = (45, 50, 55)       # Темний сіро-синій фон сітки
GRID_LINE_COLOR = (120, 100, 70)           # Приглушений золотистий для ліній
EMPTY_CELL_COLOR = (40, 45, 50)            # Темний для порожніх клітинок
GRID_BORDER_COLOR = (90, 75, 50)           # Темніший золотистий для рамки

# ===== КОЛЬОРИ ІНТЕРФЕЙСУ =====
# М'яка темна тема
BACKGROUND_COLOR = (28, 32, 36)        # Темний сіро-синій фон
TEXT_COLOR = (220, 220, 215)           # М'який світлий текст

# Кольори кнопок
BUTTON_COLOR = (55, 65, 75)            # Темно-сірий
BUTTON_HOVER_COLOR = (75, 85, 95)      # Світліше при наведенні

# Кольори контейнера для фігур
PIECE_BOX_BORDER_COLOR = (70, 60, 45)  # Темний коричневий
PIECE_BOX_FILL_COLOR = (50, 55, 60)    # Темно-сірий фон

# ===== КОЛЬОРИ КОНКРЕТНИХ UI ЕЛЕМЕНТІВ =====
# Магазин
UI_SHOP_TITLE_COLOR = (220, 220, 215)      # Заголовок магазину
UI_SHOP_BALANCE_COLOR = (200, 170, 100)    # Баланс catcoin (приглушене золото)
UI_SHOP_ITEM_AVAILABLE_COLOR = (200, 200, 195)  # Доступний товар
UI_SHOP_ITEM_SELECTED_COLOR = (120, 180, 120)   # Вибраний товар
UI_SHOP_ITEM_UNAVAILABLE_COLOR = (140, 140, 135) # Недоступний товар
UI_SHOP_BACKGROUND_COLOR = (60, 70, 80, 60)      # Фон магазину з прозорістю
UI_SHOP_BORDER_COLOR = (90, 100, 110)            # Контур магазину

# Підказки та повідомлення
UI_HINT_COLOR = (160, 160, 155)            # Звичайні підказки
UI_ROTATION_HINT_COLOR = (255, 255, 0)     # Підказка про обертання (жовта)
UI_ROTATION_HIGHLIGHT_COLOR = (255, 255, 0) # Підсвічування при обертанні

# HUD (очки, рекорди)
UI_HUD_SCORE_COLOR = TEXT_COLOR             # Колір очок
UI_HUD_RECORD_COLOR = TEXT_COLOR            # Колір рекорду

# ===== КОЛЬОРИ ЕФЕКТІВ =====
# М'які кольори попереднього перегляду
PREVIEW_VALID_COLOR = (120, 180, 120, 100)    # М'який зелений з прозорістю
PREVIEW_INVALID_COLOR = (180, 100, 100, 100)  # М'який червоний з прозорістю

# Кольори для очищення ліній
CLEAR_EFFECT_COLOR = (200, 200, 200, 150)     # М'який білий з прозорістю

# ===== КОЛЬОРИ МЕНЮ ТА РЕКОРДІВ =====
# М'які медалі в таблиці рекордів
MEDAL_GOLD = (200, 170, 100)       # Приглушене золото
MEDAL_SILVER = (150, 150, 150)     # Приглушене срібло  
MEDAL_BRONZE = (160, 120, 90)      # Приглушена бронза

# Кольори тексту в меню
MENU_TEXT_COLOR = (220, 220, 215)  # М'який світлий текст
MENU_TITLE_COLOR = (240, 235, 230) # Трохи світліший для заголовків

# ===== БАЗОВІ КОЛЬОРИ =====
WHITE = (255, 255, 255)  # Використовується в UI
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (173, 216, 230)
KARATOVY = (255, 120, 18)
CARROT = (255, 160, 48)

# ===== ШРИФТИ =====
# Базові розміри шрифтів
FONT_SIZE = 36
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# Спеціальні шрифти для різних елементів UI
UI_FONT_PAUSE_BUTTON = 24           # Шрифт кнопки паузи
UI_FONT_PAUSE_TITLE = 48            # Заголовок меню паузи
UI_FONT_PAUSE_BUTTONS = 24          # Кнопки в меню паузи
UI_FONT_CONTROL_PANEL = 20          # Панель керування
UI_FONT_SHOP_TITLE = 28             # Заголовок магазину
UI_FONT_SHOP_ITEMS = 28             # Товари в магазині
UI_FONT_ROTATION_HINT = 32          # Підказка про обертання
UI_FONT_HUD_SCORE = int(FONT_SIZE * 0.9)    # Шрифт очок (32)
UI_FONT_HUD_RECORD = int(FONT_SIZE_SMALL * 0.8)  # Шрифт рекорду (19)
UI_FONT_HINTS = 18                  # Підказки

# Налаштування шрифтів (ім'я та стиль)
UI_FONT_FAMILY_DEFAULT = None       # None = системний шрифт Pygame
UI_FONT_FAMILY_ARIAL = "Arial"      # Arial для HUD
UI_USE_BOLD_FONTS = True            # Використовувати жирні шрифти

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

# Кольори панелі керування для темної теми
CONTROL_PANEL_BG = (35, 40, 45, 200)     # Темний сіро-синій з прозорістю
CONTROL_PANEL_BORDER = (70, 80, 90)      # М'який сірий для рамки
CONTROL_BUTTON_COLOR = (55, 65, 75)      # М'який темно-сірий
CONTROL_BUTTON_HOVER = (75, 85, 95)      # Світліше при наведенні
CONTROL_BUTTON_TEXT = (220, 220, 215)    # М'який світлий текст

# ===== КНОПКА ПАУЗИ =====
# М'яка кнопка паузи для темної теми
PAUSE_BUTTON_SIZE = 50
PAUSE_BUTTON_X = 20
PAUSE_BUTTON_Y = SCREEN_HEIGHT - PAUSE_BUTTON_SIZE - 20
PAUSE_BUTTON_COLOR = (50, 55, 65, 200)   # М'який темно-сірий з прозорістю
PAUSE_BUTTON_HOVER = (70, 75, 85, 220)   # Світліше при наведенні
PAUSE_BUTTON_BORDER = (90, 95, 105)      # М'який сірий контур

# ===== ШЛЯХИ ДО ЗОБРАЖЕНЬ =====
# Іконки та фонові зображення
UI_ICON_PATH = "image/icon.png"             # Іконка гри
UI_BACKGROUND_IMAGE_PATH = "image/icon.png" # Фонове зображення (поки використовуємо іконку)

# Спрайти котиків
SPRITE_PATH_WHITE = "assets/sprites/cats/white_block_cat.png"
SPRITE_PATH_MINT = "assets/sprites/cats/mind_block_cat.png"
SPRITE_PATH_RED = "assets/sprites/cats/red_block_cat.png"
SPRITE_PATH_BLUE = "assets/sprites/cats/blue_block_cat.png"
SPRITE_PATH_ORANGE = "assets/sprites/cats/orange_block_cat.png"
SPRITE_PATH_PINK = "assets/sprites/cats/pink_block_cat.png"
SPRITE_PATH_PURPLE = "assets/sprites/cats/purple_block_cat.png"
SPRITE_PATH_YELLOW = "assets/sprites/cats/yelow_block_cat.png"

# Налаштування спрайтів
SPRITE_ORIGINAL_SIZE = 2048         # Оригінальний розмір спрайтів
SPRITE_USE_SMOOTH_SCALING = False   # False = швидше, True = краща якість
SPRITE_CACHE_SIZE = 50              # Максимум спрайтів у кеші

# ===== СПРАЙТИ БЛОКІВ =====
# Увімкнути/вимкнути використання спрайтів (True = спрайти, False = кольорові блоки)
USE_SPRITES = True

# Відповідність кольорів до файлів спрайтів (використовуємо нові константи)
COLOR_TO_SPRITE = {
    PIECE_YELLOW: SPRITE_PATH_WHITE,      # Жовтий -> білий кіт
    PIECE_GREEN: SPRITE_PATH_MINT,        # Зелений -> м'ятний кіт  
    PIECE_RED: SPRITE_PATH_RED,           # Червоний -> червоний кіт
    PIECE_BLUE: SPRITE_PATH_BLUE,         # Синій -> синій кіт
    PIECE_ORANGE: SPRITE_PATH_ORANGE,     # Помаранчевий -> помаранчевий кіт
    PIECE_PINK: SPRITE_PATH_PINK,         # Рожевий -> рожевий кіт
    PIECE_CYAN: SPRITE_PATH_PURPLE,       # Блакитний -> фіолетовий кіт
}

# Кеш завантажених спрайтів з обмеженням розміру (використовуємо нові константи)
_sprite_cache = {}
_max_cache_size = SPRITE_CACHE_SIZE  # Використовуємо константу замість магічного числа
_original_sprites = {}  # Кеш оригінальних спрайтів

def get_block_sprite(color, size):
    """Оптимізована версія з контролем пам'яті"""
    # Якщо спрайти вимкнені, повертаємо None
    if not USE_SPRITES:
        return None
        
    if color not in COLOR_TO_SPRITE:
        return None
        
    sprite_path = COLOR_TO_SPRITE[color]
    cache_key = (sprite_path, size)
    
    # Перевіряємо кеш масштабованих спрайтів
    if cache_key in _sprite_cache:
        return _sprite_cache[cache_key]
    
    try:
        # Завантажуємо оригінальний спрайт лише один раз
        if sprite_path not in _original_sprites:
            _original_sprites[sprite_path] = pygame.image.load(sprite_path)
        
        original_sprite = _original_sprites[sprite_path]
        
        # Масштабуємо спрайт
        if size > 0:
            # Використовуємо scale замість smoothscale для швидкості
            scaled_sprite = pygame.transform.scale(original_sprite, (size, size))
        else:
            scaled_sprite = original_sprite
        
        # Контролюємо розмір кешу
        if len(_sprite_cache) >= _max_cache_size:
            # Видаляємо найстарший елемент (простий FIFO)
            oldest_key = next(iter(_sprite_cache))
            del _sprite_cache[oldest_key]
        
        _sprite_cache[cache_key] = scaled_sprite
        return scaled_sprite
        
    except pygame.error as e:
        print(f"Помилка завантаження спрайту {sprite_path}: {e}")
        return None

# ===== ФУНКЦІЇ =====
def get_background_image():
    """Повертає фонове зображення з масштабуванням під розмір екрану"""
    return pygame.transform.scale(
        pygame.image.load(UI_BACKGROUND_IMAGE_PATH), 
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
