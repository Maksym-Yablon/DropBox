import pygame
import random

# ===== РОЗМІРИ ТА ПОЗИЦІЇ =====
# Налаштування для тестування на комп'ютері (встановіть TEST_MODE = True для тестування)
TEST_MODE = True  # Змініть на False для справжніх мобільних розмірів

if TEST_MODE:
    # Розміри для тестування на комп'ютері (вертикальна орієнтація, але менша)
    SCREEN_WIDTH = 540   # Половина від мобільної ширини
    SCREEN_HEIGHT = 960  # Приблизно половина від мобільної висоти
else:
    # Розміри екрану для мобільного пристрою (вертикальна орієнтація)
    SCREEN_WIDTH = 1080  # Ширина екрану мобільного пристрою  
    SCREEN_HEIGHT = 2412  # Висота екрану мобільного пристрою

# Мобільні відступи
MOBILE_SIDE_MARGIN = 40  # Відступи по боках від краю екрану

# Розміри клітинок (адаптовані під мобільний)
available_width = SCREEN_WIDTH - (2 * MOBILE_SIDE_MARGIN)  # Доступна ширина з урахуванням відступів
GRID_CELL_SIZE = available_width // 8 - 2  # Розмір клітинки сітки (8 клітинок + відступи)
PIECE_CELL_SIZE = GRID_CELL_SIZE  # Розмір клітинки для фігур
PIECE_CONTAINER_CELL_SIZE = GRID_CELL_SIZE - 10  # Менший розмір для фігур у контейнері
GRID_CELL_BORDER_RADIUS = 8  # Радіус закруглення для комірок сітки

# Параметри сітки
GRID_SIZE = 8  # Розмір сітки 8x8
GRID_COLS = GRID_SIZE
GRID_ROWS = GRID_SIZE

# Мобільні UI елементи (адаптивні під розмір екрана)
MOBILE_TOP_BAR_HEIGHT = 80  # Висота верхньої панелі
MOBILE_BUTTON_SIZE = 60  # Розмір кнопок у верхній панелі
MOBILE_SCORE_AREA_HEIGHT = 120  # Висота області з очками

# Контейнер для фігур (адаптований під мобільний та TEST_MODE)
PIECE_CONTAINER_WIDTH = SCREEN_WIDTH - (2 * MOBILE_SIDE_MARGIN)  # На всю ширину з відступами
# PIECE_CONTAINER_HEIGHT встановлюється в логіці адаптивного позиціонування вище

# Магазин (адаптований під мобільний та TEST_MODE)
SHOP_CONTAINER_WIDTH = SCREEN_WIDTH - (2 * MOBILE_SIDE_MARGIN)  # На всю ширину з відступами
SHOP_BUTTON_SIZE = 60  # Фіксований розмір для стабільності
# SHOP_CONTAINER_HEIGHT встановлюється в логіці адаптивного позиціонування вище

# Рекламний блок (адаптований під мобільний та TEST_MODE)
AD_CONTAINER_WIDTH = SCREEN_WIDTH - (2 * MOBILE_SIDE_MARGIN)
AD_CONTAINER_VISIBLE = True  # Тепер видимий
# AD_CONTAINER_HEIGHT встановлюється в логіці адаптивного позиціонування вище

# ===== АДАПТИВНЕ ПОЗИЦІОНУВАННЯ КОНТЕЙНЕРІВ =====
# Рівномірний розподіл висоти екрану з адаптивними відступами

# Верхня панель (header)
MOBILE_HEADER_HEIGHT = MOBILE_TOP_BAR_HEIGHT + MOBILE_SCORE_AREA_HEIGHT  # 80 + 120 = 200px

# Доступна висота для ігрових елементів
AVAILABLE_HEIGHT = SCREEN_HEIGHT - MOBILE_HEADER_HEIGHT  # 960 - 200 = 760px

# Адаптивний розподіл доступної висоти (у відсотках)
GRID_HEIGHT_PERCENT = 0.55      # 55% для ігрового поля (трохи зменшено)
PIECES_HEIGHT_PERCENT = 0.18    # 18% для контейнера фігур (збільшено)
SHOP_HEIGHT_PERCENT = 0.10      # 10% для магазину
AD_HEIGHT_PERCENT = 0.07        # 7% для реклами
SPACING_HEIGHT_PERCENT = 0.10   # 10% для всіх відступів разом

# Розрахунок реальних розмірів
GRID_HEIGHT = int(AVAILABLE_HEIGHT * GRID_HEIGHT_PERCENT)      # ~418px
PIECE_CONTAINER_HEIGHT = int(AVAILABLE_HEIGHT * PIECES_HEIGHT_PERCENT)  # ~136px
SHOP_CONTAINER_HEIGHT = int(AVAILABLE_HEIGHT * SHOP_HEIGHT_PERCENT)     # ~76px
AD_CONTAINER_HEIGHT = int(AVAILABLE_HEIGHT * AD_HEIGHT_PERCENT)         # ~53px

# Розрахунок відступів (рівномірно розподіляємо 10% на 5 відступів)
TOTAL_SPACING = int(AVAILABLE_HEIGHT * SPACING_HEIGHT_PERCENT)  # ~76px
CONTAINER_SPACING = TOTAL_SPACING // 5  # ~15px на кожен відступ

# Позиціонування контейнерів з рівними відступами
GRID_Y = MOBILE_HEADER_HEIGHT + CONTAINER_SPACING
GRID_X = (SCREEN_WIDTH - (GRID_SIZE * GRID_CELL_SIZE)) // 2  # Центрування
GRID_BOTTOM = GRID_Y + GRID_HEIGHT

PIECE_CONTAINER_Y = GRID_BOTTOM + CONTAINER_SPACING
SHOP_CONTAINER_Y = PIECE_CONTAINER_Y + PIECE_CONTAINER_HEIGHT + CONTAINER_SPACING
AD_CONTAINER_Y = SHOP_CONTAINER_Y + SHOP_CONTAINER_HEIGHT + CONTAINER_SPACING

# Нижній відступ (до кінця екрану)
BOTTOM_MARGIN = CONTAINER_SPACING

# Діагностика розподілу
TOTAL_USED_HEIGHT = AD_CONTAINER_Y + AD_CONTAINER_HEIGHT + BOTTOM_MARGIN
REMAINING_HEIGHT = SCREEN_HEIGHT - TOTAL_USED_HEIGHT

print(f"🎯 АДАПТИВНИЙ РОЗПОДІЛ для {SCREEN_WIDTH}x{SCREEN_HEIGHT}:")
print(f"📏 Header: {MOBILE_HEADER_HEIGHT}px ({MOBILE_HEADER_HEIGHT/SCREEN_HEIGHT*100:.1f}%)")
print(f"📏 Grid: {GRID_HEIGHT}px ({GRID_HEIGHT_PERCENT*100:.0f}%)")
print(f"📏 Pieces: {PIECE_CONTAINER_HEIGHT}px ({PIECES_HEIGHT_PERCENT*100:.0f}%)")  
print(f"📏 Shop: {SHOP_CONTAINER_HEIGHT}px ({SHOP_HEIGHT_PERCENT*100:.0f}%)")
print(f"📏 Ads: {AD_CONTAINER_HEIGHT}px ({AD_HEIGHT_PERCENT*100:.0f}%)")
print(f"📏 Відступи: {CONTAINER_SPACING}px кожен ({SPACING_HEIGHT_PERCENT*100:.0f}% загалом)")
print(f"📏 Використано: {TOTAL_USED_HEIGHT}px, Залишилося: {REMAINING_HEIGHT}px")

# Автокорекція якщо є невелике переповнення/недовикористання
if abs(REMAINING_HEIGHT) > 20:
    print(f"⚙️ Автокорекція: коригуємо відступи на {REMAINING_HEIGHT}px")
    CONTAINER_SPACING += REMAINING_HEIGHT // 5
    
    # Перерахунок з новими відступами
    GRID_Y = MOBILE_HEADER_HEIGHT + CONTAINER_SPACING
    GRID_BOTTOM = GRID_Y + GRID_HEIGHT
    PIECE_CONTAINER_Y = GRID_BOTTOM + CONTAINER_SPACING
    SHOP_CONTAINER_Y = PIECE_CONTAINER_Y + PIECE_CONTAINER_HEIGHT + CONTAINER_SPACING
    AD_CONTAINER_Y = SHOP_CONTAINER_Y + SHOP_CONTAINER_HEIGHT + CONTAINER_SPACING
    BOTTOM_MARGIN = CONTAINER_SPACING
    
    print(f"📏 Новий відступ: {CONTAINER_SPACING}px")

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
BUTTON_BORDER_COLOR = (90, 100, 110)   # Сірий колір для рамки кнопок

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
    'SingleBlock': 10,    # 10% - часто (основна фігура)
    'Square': 12,         # 12% - досить часто
    'Square3x3': 5,       # 5% - рідко (велика фігура)
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

# ===== МОБІЛЬНІ КОНСТАНТИ =====
# Кнопки header'а
MOBILE_BACK_BUTTON_X = MOBILE_SIDE_MARGIN
MOBILE_BACK_BUTTON_Y = 20
MOBILE_SETTINGS_BUTTON_X = SCREEN_WIDTH - MOBILE_SIDE_MARGIN - MOBILE_BUTTON_SIZE
MOBILE_SETTINGS_BUTTON_Y = 20

# Кольори мобільних кнопок
MOBILE_BUTTON_COLOR = (70, 130, 180)  # Steel blue
MOBILE_BUTTON_HOVER_COLOR = (100, 150, 200)
MOBILE_BUTTON_TEXT_COLOR = (255, 255, 255)

# Магазин константи
MOBILE_SHOP_Y = PIECE_CONTAINER_Y + PIECE_CONTAINER_HEIGHT + 20
MOBILE_SHOP_BUTTON_WIDTH = SHOP_CONTAINER_WIDTH // 4
MOBILE_SHOP_BUTTON_HEIGHT = 60

# Кольори кнопок магазину
MOBILE_SHOP_ROTATE_COLOR = (50, 205, 50)    # Lime green
MOBILE_SHOP_RESET_COLOR = (255, 69, 0)      # Red orange  
MOBILE_SHOP_COPY_COLOR = (255, 215, 0)      # Gold
MOBILE_SHOP_HINT_COLOR = (138, 43, 226)     # Blue violet

# Кнопки мобільного магазину
mobile_shop_buttons = [
    (MOBILE_SIDE_MARGIN, "Поворот", MOBILE_SHOP_ROTATE_COLOR, "rotate"),
    (MOBILE_SIDE_MARGIN + SHOP_CONTAINER_WIDTH//4, "Скинути", MOBILE_SHOP_RESET_COLOR, "reset"),
    (MOBILE_SIDE_MARGIN + SHOP_CONTAINER_WIDTH//2, "Бонус", MOBILE_SHOP_COPY_COLOR, "copy"),
    (MOBILE_SIDE_MARGIN + 3*SHOP_CONTAINER_WIDTH//4, "Підказка", MOBILE_SHOP_HINT_COLOR, "hint"),
]