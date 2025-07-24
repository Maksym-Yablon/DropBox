extends Node

# Constants.gd - Автозавантаження для глобальних констант
# Налаштування для Godot v4.4.1

# ===== РОЗМІРИ ТА ПОЗИЦІЇ =====
var TEST_MODE = true  # Встанови false для мобільного режиму

# Розміри екрану
var SCREEN_WIDTH = 1080 if not TEST_MODE else 800
var SCREEN_HEIGHT = 1920 if not TEST_MODE else 600

# Мобільні константи
var MOBILE_SIDE_MARGIN = 40
var GRID_CELL_SIZE = 48
var PIECE_CELL_SIZE = 40
var PIECE_CONTAINER_CELL_SIZE = 32
var GRID_CELL_BORDER_RADIUS = 8
var GRID_SIZE = 8
var GRID_COLS = GRID_SIZE
var GRID_ROWS = GRID_SIZE

# Висоти та позиції
var MOBILE_TOP_BAR_HEIGHT = 100
var MOBILE_BUTTON_SIZE = 80
var MOBILE_SCORE_AREA_HEIGHT = 120
var PIECE_CONTAINER_WIDTH = SCREEN_WIDTH - MOBILE_SIDE_MARGIN * 2
var SHOP_CONTAINER_WIDTH = PIECE_CONTAINER_WIDTH
var SHOP_BUTTON_SIZE = 60
var AD_CONTAINER_WIDTH = PIECE_CONTAINER_WIDTH
var PIECE_MARGIN = 6

# Висоти контейнерів
var MOBILE_HEADER_HEIGHT = MOBILE_TOP_BAR_HEIGHT + MOBILE_SCORE_AREA_HEIGHT
var AVAILABLE_HEIGHT = SCREEN_HEIGHT - MOBILE_HEADER_HEIGHT
var GRID_HEIGHT = GRID_CELL_SIZE * GRID_SIZE
var PIECE_CONTAINER_HEIGHT = 150
var SHOP_CONTAINER_HEIGHT = 120
var AD_CONTAINER_HEIGHT = 80
var CONTAINER_SPACING = 20

# Позиції
var GRID_Y = MOBILE_HEADER_HEIGHT + (AVAILABLE_HEIGHT - GRID_HEIGHT - PIECE_CONTAINER_HEIGHT - SHOP_CONTAINER_HEIGHT - AD_CONTAINER_HEIGHT - CONTAINER_SPACING * 3) / 2
var GRID_X = (SCREEN_WIDTH - GRID_CELL_SIZE * GRID_SIZE) / 2
var GRID_BOTTOM = GRID_Y + GRID_HEIGHT
var PIECE_CONTAINER_Y = GRID_BOTTOM + CONTAINER_SPACING
var SHOP_CONTAINER_Y = PIECE_CONTAINER_Y + PIECE_CONTAINER_HEIGHT + CONTAINER_SPACING
var AD_CONTAINER_Y = SHOP_CONTAINER_Y + SHOP_CONTAINER_HEIGHT + CONTAINER_SPACING
var GRID_Y_FRAME = GRID_Y

# ===== КОЛЬОРИ БЛОКІВ ФІГУР =====
var PIECE_YELLOW = Color(0.855, 0.765, 0.47)
var PIECE_GREEN = Color(0.565, 0.722, 0.565)
var PIECE_RED = Color(0.753, 0.471, 0.471)
var PIECE_BLUE = Color(0.471, 0.588, 0.753)
var PIECE_ORANGE = Color(0.824, 0.627, 0.471)
var PIECE_PINK = Color(0.753, 0.565, 0.659)
var PIECE_CYAN = Color(0.471, 0.706, 0.706)

# Контури блоків
var PIECE_OUTLINE_COLOR = Color(0.314, 0.314, 0.314)

# ===== КОЛЬОРИ СІТКИ =====
var GRID_BACKGROUND_COLOR = Color(0.176, 0.196, 0.216)
var GRID_LINE_COLOR = Color(0.471, 0.392, 0.275)
var EMPTY_CELL_COLOR = Color(0.157, 0.176, 0.196)
var GRID_BORDER_COLOR = Color(0.353, 0.294, 0.196)

# ===== КОЛЬОРИ ІНТЕРФЕЙСУ =====
var BACKGROUND_COLOR = Color(0.110, 0.125, 0.141)
var TEXT_COLOR = Color(0.863, 0.863, 0.843)

# Кольори кнопок
var BUTTON_COLOR = Color(0.216, 0.255, 0.294)
var BUTTON_HOVER_COLOR = Color(0.294, 0.333, 0.373)
var BUTTON_BORDER_COLOR = Color(0.353, 0.392, 0.431)

# Кольори контейнера для фігур
var PIECE_BOX_BORDER_COLOR = Color(0.275, 0.235, 0.176)
var PIECE_BOX_FILL_COLOR = Color(0.196, 0.216, 0.235)

# ===== КОЛЬОРИ UI ЕЛЕМЕНТІВ =====
var UI_SHOP_TITLE_COLOR = Color(0.863, 0.863, 0.843)
var UI_SHOP_BALANCE_COLOR = Color(0.784, 0.667, 0.392)
var UI_SHOP_ITEM_AVAILABLE_COLOR = Color(0.784, 0.784, 0.765)
var UI_SHOP_ITEM_SELECTED_COLOR = Color(0.471, 0.706, 0.471)
var UI_SHOP_ITEM_UNAVAILABLE_COLOR = Color(0.549, 0.549, 0.529)
var UI_SHOP_BACKGROUND_COLOR = Color(0.235, 0.275, 0.314, 0.235)
var UI_SHOP_BORDER_COLOR = Color(0.353, 0.392, 0.431)

# ===== ШАНСИ ПОЯВИ ФІГУР =====
var PIECE_SPAWN_CHANCES = {
	"SingleBlock": 25,
	"Square": 20,
	"Square3x3": 5,
	"Line": 15,
	"Line2x1": 15,
	"Line3x1": 10,
	"LShape": 12,
	"TShape": 8,
	"ZShape": 8,
	"Cross": 6,
	"Corner": 10,
	"Line3": 12,
	"SmallT": 10
}

# ===== ШЛЯХИ ДО РЕСУРСІВ =====
var UI_ICON_PATH = "res://image/icon.png"
var UI_FONT_FAMILY_DEFAULT = "res://assets/fonts/default.ttf"  # Додай шрифт
var UI_FONT_SHOP_TITLE = 24

func get_block_sprite(color):
	"""Повертає шлях до спрайту блоку за кольором"""
	var sprite_map = {
		PIECE_YELLOW: "res://assets/sprites/cats/yelow_block_cat.png",
		PIECE_GREEN: "res://assets/sprites/cats/mind_block_cat.png",
		PIECE_RED: "res://assets/sprites/cats/red_block_cat.png",
		PIECE_BLUE: "res://assets/sprites/cats/blue_block_cat.png",
		PIECE_ORANGE: "res://assets/sprites/cats/orange_block_cat.png",
		PIECE_PINK: "res://assets/sprites/cats/pink_block_cat.png",
		PIECE_CYAN: "res://assets/sprites/cats/blue_block_cat.png"
	}
	return sprite_map.get(color, "")
