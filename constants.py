import pygame

# ===== РОЗМІРИ ТА ПОЗИЦІЇ =====
# Розміри екрану
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700

# Розміри клітинок
GRID_CELL_SIZE = 50  # Розмір клітинки сітки
PIECE_CELL_SIZE = 48  # Розмір клітинки для фігур

# Контейнер для фігур
PIECE_CONTAINER_WIDTH = 250
PIECE_CONTAINER_HEIGHT = 500

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

# Фонове зображення з масштабуванням під розмір екрану
BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load("image/icon.png"), 
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
