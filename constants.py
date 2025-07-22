import pygame
import random

# ===== РОЗМІРИ ТА ПОЗИЦІЇ =====
# Налаштування для тестування на комп'ютері (встановіть TEST_MODE = True для тестування)

# ===== АДАПТИВНА МОБІЛЬНА КОНФІГУРАЦІЯ =====
import math

class AdaptiveMobileConfig:
    def __init__(self, test_mode=True):
        self.TEST_MODE = test_mode
        
        # Базові розміри екрану
        if self.TEST_MODE:
            self.SCREEN_WIDTH = 540
            self.SCREEN_HEIGHT = 960
        else:
            self.SCREEN_WIDTH = 1080
            self.SCREEN_HEIGHT = 2412
        
        # Розрахунок адаптивних параметрів
        self.calculate_adaptive_sizes()
        
    def calculate_adaptive_sizes(self):
        """Розрахунок всіх адаптивних розмірів з перевірками"""
        
        # ===== БАЗОВІ ВІДСТУПИ =====
        # Відступи залежать від розміру екрану
        self.MOBILE_SIDE_MARGIN = max(20, int(self.SCREEN_WIDTH * 0.037))  # ~3.7% від ширини
        
        # ===== ВЕРХНЯ ПАНЕЛЬ =====
        # Адаптивна висота верхньої панелі
        self.MOBILE_TOP_BAR_HEIGHT = max(60, int(self.SCREEN_HEIGHT * 0.083))  # ~8.3%
        self.MOBILE_SCORE_AREA_HEIGHT = max(80, int(self.SCREEN_HEIGHT * 0.125))  # ~12.5%
        self.MOBILE_HEADER_HEIGHT = self.MOBILE_TOP_BAR_HEIGHT + self.MOBILE_SCORE_AREA_HEIGHT
        
        # ===== РОЗРАХУНОК СІТКИ =====
        self.GRID_SIZE = 8
        
        # Доступна ширина для сітки
        available_width = self.SCREEN_WIDTH - (2 * self.MOBILE_SIDE_MARGIN)
        
        # Розмір клітинки - КРИТИЧНО ВАЖЛИВО!
        # Робимо так щоб сітка точно вмістилася
        ideal_cell_size = available_width / self.GRID_SIZE
        self.GRID_CELL_SIZE = int(ideal_cell_size)
        
        # Корегуємо ширину сітки щоб вона була точною
        self.actual_grid_width = self.GRID_CELL_SIZE * self.GRID_SIZE  
        
        # Центруємо сітку
        self.GRID_X = (self.SCREEN_WIDTH - self.actual_grid_width) // 2
        
        # ===== АДАПТИВНИЙ РОЗПОДІЛ ВИСОТИ =====
        self.AVAILABLE_HEIGHT = self.SCREEN_HEIGHT - self.MOBILE_HEADER_HEIGHT
        
        # Мінімальні розміри для кожного компонента
        min_grid_height = self.actual_grid_width  # Квадратна сітка
        min_pieces_height = max(100, int(self.SCREEN_HEIGHT * 0.10))  # Мінімум 10%
        min_shop_height = max(60, int(self.SCREEN_HEIGHT * 0.06))   # Мінімум 6%
        min_ad_height = max(40, int(self.SCREEN_HEIGHT * 0.04))     # Мінімум 4%
        min_spacing = max(10, int(self.SCREEN_HEIGHT * 0.01))       # Мінімум 1%
        
        # Перевірка чи всі мінімальні розміри вміщаються
        min_total = min_grid_height + min_pieces_height + min_shop_height + min_ad_height + (min_spacing * 5)
        
        if min_total > self.AVAILABLE_HEIGHT:
            print(f"⚠️ КРИТИЧНО: Мінімальні розміри ({min_total}px) не вміщаються у доступну висоту ({self.AVAILABLE_HEIGHT}px)")
            # Аварійний режим - зменшуємо все пропорційно
            scale_factor = self.AVAILABLE_HEIGHT / min_total * 0.95  # 5% запас
            
            self.GRID_HEIGHT = int(min_grid_height * scale_factor)
            self.PIECE_CONTAINER_HEIGHT = int(min_pieces_height * scale_factor)
            self.SHOP_CONTAINER_HEIGHT = int(min_shop_height * scale_factor)
            self.AD_CONTAINER_HEIGHT = int(min_ad_height * scale_factor)
            self.CONTAINER_SPACING = int(min_spacing * scale_factor)
        else:
            # Нормальний розрахунок
            remaining_height = self.AVAILABLE_HEIGHT - min_total
            
            # Розподіляємо залишковий простір
            # Пріоритет: сітка > фігури > відступи > магазин > реклама
            extra_for_grid = int(remaining_height * 0.4)
            extra_for_pieces = int(remaining_height * 0.3)
            extra_for_spacing = int(remaining_height * 0.2)
            extra_for_shop = int(remaining_height * 0.1)
            
            self.GRID_HEIGHT = min_grid_height + extra_for_grid
            self.PIECE_CONTAINER_HEIGHT = min_pieces_height + extra_for_pieces
            self.SHOP_CONTAINER_HEIGHT = min_shop_height + extra_for_shop
            self.AD_CONTAINER_HEIGHT = min_ad_height
            self.CONTAINER_SPACING = min_spacing + (extra_for_spacing // 5)
        
        # ===== ПОЗИЦІОНУВАННЯ =====
        # Координата Y для ігрової сітки (grid.py)
        self.GRID_Y = self.MOBILE_HEADER_HEIGHT + self.CONTAINER_SPACING

        # Координата Y для графічної рамки (frame.py) — можна налаштовувати окремо
        self.GRID_Y_FRAME = self.GRID_Y + 100 # За замовчуванням співпадає, але можна змінити окремо

        # Якщо сітка не квадратна, центруємо її вертикально в доступному просторі
        if self.GRID_HEIGHT != self.actual_grid_width:
            grid_vertical_center = self.GRID_Y + (self.GRID_HEIGHT // 2)
            self.GRID_Y = grid_vertical_center - (self.actual_grid_width // 2)
            self.GRID_Y_FRAME = self.GRID_Y  # За замовчуванням теж зміщується

        self.GRID_BOTTOM = self.GRID_Y + self.actual_grid_width  # Використовуємо реальну ширину

        self.PIECE_CONTAINER_Y = self.GRID_BOTTOM + self.CONTAINER_SPACING + 40
        self.SHOP_CONTAINER_Y = self.PIECE_CONTAINER_Y + self.PIECE_CONTAINER_HEIGHT + self.CONTAINER_SPACING
        self.AD_CONTAINER_Y = self.SHOP_CONTAINER_Y + self.SHOP_CONTAINER_HEIGHT + self.CONTAINER_SPACING
        
        # ===== ДОДАТКОВІ ПАРАМЕТРИ =====
        self.PIECE_CELL_SIZE = self.GRID_CELL_SIZE
        self.PIECE_CONTAINER_CELL_SIZE = max(30, self.GRID_CELL_SIZE - 10)
        self.GRID_CELL_BORDER_RADIUS = max(4, int(self.GRID_CELL_SIZE * 0.1))
        
        # Розміри контейнерів
        self.PIECE_CONTAINER_WIDTH = self.SCREEN_WIDTH - (2 * self.MOBILE_SIDE_MARGIN)
        self.SHOP_CONTAINER_WIDTH = self.SCREEN_WIDTH - (2 * self.MOBILE_SIDE_MARGIN)
        self.AD_CONTAINER_WIDTH = self.SCREEN_WIDTH - (2 * self.MOBILE_SIDE_MARGIN)
        
        # Кнопки (адаптивні)
        self.MOBILE_BUTTON_SIZE = max(40, int(self.SCREEN_WIDTH * 0.056))  # ~5.6%
        self.SHOP_BUTTON_SIZE = max(50, int(self.SCREEN_WIDTH * 0.074))    # ~7.4%
        
        # Відступи
        self.PIECE_MARGIN = max(1, int(self.GRID_CELL_SIZE * 0.02))
        
        # ===== ДІАГНОСТИКА =====
        self.print_diagnostics()
        
    def print_diagnostics(self):
        """Виведення діагностичної інформації"""
        total_used = (self.MOBILE_HEADER_HEIGHT + 
                    self.actual_grid_width + 
                    self.PIECE_CONTAINER_HEIGHT + 
                    self.SHOP_CONTAINER_HEIGHT + 
                    self.AD_CONTAINER_HEIGHT + 
                    (self.CONTAINER_SPACING * 5))
        
        remaining = self.SCREEN_HEIGHT - total_used
        
        print(f"\n🎯 АДАПТИВНИЙ РОЗПОДІЛ для {self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}:")
        print(f"� Бокові відступи: {self.MOBILE_SIDE_MARGIN}px ({self.MOBILE_SIDE_MARGIN/self.SCREEN_WIDTH*100:.1f}%)")
        print(f"�📏 Header: {self.MOBILE_HEADER_HEIGHT}px ({self.MOBILE_HEADER_HEIGHT/self.SCREEN_HEIGHT*100:.1f}%)")
        print(f"🎮 Grid: {self.actual_grid_width}x{self.actual_grid_width}px (клітинка: {self.GRID_CELL_SIZE}px)")
        print(f"🧩 Pieces: {self.PIECE_CONTAINER_HEIGHT}px ({self.PIECE_CONTAINER_HEIGHT/self.SCREEN_HEIGHT*100:.1f}%)")
        print(f"� Shop: {self.SHOP_CONTAINER_HEIGHT}px ({self.SHOP_CONTAINER_HEIGHT/self.SCREEN_HEIGHT*100:.1f}%)")
        print(f"� Ads: {self.AD_CONTAINER_HEIGHT}px ({self.AD_CONTAINER_HEIGHT/self.SCREEN_HEIGHT*100:.1f}%)")
        print(f"📏 Відступи: {self.CONTAINER_SPACING}px кожен")
        print(f"✅ Використано: {total_used}px, Залишилося: {remaining}px")
        
        # Перевірка пропорцій
        if remaining < 0:
            print(f"❌ ПЕРЕПОВНЕННЯ: {abs(remaining)}px")
        elif remaining > 50:
            print(f"⚠️ НЕДОВИКОРИСТАННЯ: {remaining}px")
        else:
            print(f"✅ ОПТИМАЛЬНО: залишок {remaining}px")

# Створюємо конфігурацію і експортуємо змінні
config = AdaptiveMobileConfig(test_mode=True)

    # Експортуємо всі необхідні змінні для сумісності
TEST_MODE = config.TEST_MODE
SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT
MOBILE_SIDE_MARGIN = config.MOBILE_SIDE_MARGIN
GRID_CELL_SIZE = config.GRID_CELL_SIZE
PIECE_CELL_SIZE = config.PIECE_CELL_SIZE
PIECE_CONTAINER_CELL_SIZE = config.PIECE_CONTAINER_CELL_SIZE
GRID_CELL_BORDER_RADIUS = config.GRID_CELL_BORDER_RADIUS
GRID_SIZE = config.GRID_SIZE
GRID_COLS = config.GRID_SIZE
GRID_ROWS = config.GRID_SIZE
MOBILE_TOP_BAR_HEIGHT = config.MOBILE_TOP_BAR_HEIGHT
MOBILE_BUTTON_SIZE = config.MOBILE_BUTTON_SIZE
MOBILE_SCORE_AREA_HEIGHT = config.MOBILE_SCORE_AREA_HEIGHT
PIECE_CONTAINER_WIDTH = config.PIECE_CONTAINER_WIDTH
SHOP_CONTAINER_WIDTH = config.SHOP_CONTAINER_WIDTH
SHOP_BUTTON_SIZE = config.SHOP_BUTTON_SIZE
AD_CONTAINER_WIDTH = config.AD_CONTAINER_WIDTH
AD_CONTAINER_VISIBLE = True
PIECE_MARGIN = config.PIECE_MARGIN
MOBILE_HEADER_HEIGHT = config.MOBILE_HEADER_HEIGHT
AVAILABLE_HEIGHT = config.AVAILABLE_HEIGHT
GRID_HEIGHT = config.GRID_HEIGHT
PIECE_CONTAINER_HEIGHT = config.PIECE_CONTAINER_HEIGHT
SHOP_CONTAINER_HEIGHT = config.SHOP_CONTAINER_HEIGHT
AD_CONTAINER_HEIGHT = config.AD_CONTAINER_HEIGHT
CONTAINER_SPACING = config.CONTAINER_SPACING
GRID_Y = config.GRID_Y
GRID_X = config.GRID_X
GRID_BOTTOM = config.GRID_BOTTOM
PIECE_CONTAINER_Y = config.PIECE_CONTAINER_Y
SHOP_CONTAINER_Y = config.SHOP_CONTAINER_Y
AD_CONTAINER_Y = config.AD_CONTAINER_Y

# Окрема координата для графічної рамки (frame.py)
GRID_Y_FRAME = config.GRID_Y_FRAME

# Розміри кнопок (залишаємо для сумісності)
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