extends Node2D
class_name Shop

# Shop.gd - Внутрішньоігровий магазин

class ShopItem:
	var name: String
	var price: int
	var description: String
	var icon: Texture2D
	
	func _init(item_name: String, item_price: int, item_description: String, item_icon: Texture2D = null):
		name = item_name
		price = item_price
		description = item_description
		icon = item_icon

var x: float
var y: float
var width: float
var height: float
var font: Font
var items: Array[ShopItem]
var selected_index: int = -1

func _init(shop_x: float, shop_y: float, shop_width: float, shop_height: float, shop_font: Font):
	x = shop_x
	y = shop_y
	width = shop_width
	height = shop_height
	font = shop_font
	items = create_items()
	selected_index = -1

func create_items() -> Array[ShopItem]:
	"""Створює список товарів магазину"""
	var shop_items: Array[ShopItem] = []
	shop_items.append(ShopItem.new("Обернути фігуру", 3, "Повертає обрану фігуру на 90°"))
	shop_items.append(ShopItem.new("Очистити 5 комірок", 5, "Випадково очищає 5 комірок сітки"))
	return shop_items

func _draw():
	"""Малює панель магазину в темному стилі"""
	# М'яка темна заливка з прозорістю
	var shop_surface = RenderingServer.canvas_item_create()
	
	var fill_color = Constants.UI_SHOP_BACKGROUND_COLOR
	draw_rect(Rect2(x, y, width, height), fill_color, true, -1, 10)
	
	# М'який темний контур
	var border_color = Constants.UI_SHOP_BORDER_COLOR
	draw_rect(Rect2(x, y, width, height), border_color, false, 2, 10)
	
	# Заголовок магазину по центру контейнера
	var title_text = "МАГАЗИН"
	var title_size = font.get_string_size(title_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 24)
	var title_pos = Vector2(x + width / 2 - title_size.x / 2, y + 30)
	draw_string(font, title_pos, title_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 24, Constants.UI_SHOP_TITLE_COLOR)
	
	# Показуємо баланс catcoin по центру контейнера
	var balance_text = str(CashManager.get_balance()) + " catcoin"
	var balance_size = font.get_string_size(balance_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 20)
	var balance_pos = Vector2(x + width / 2 - balance_size.x / 2, y + 60)
	draw_string(font, balance_pos, balance_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 20, Constants.UI_SHOP_BALANCE_COLOR)
	
	# Малюємо товари
	var y_offset = y + 100
	for idx in range(items.size()):
		var item = items[idx]
		var color: Color
		
		# Визначаємо колір тексту для темної теми
		if CashManager.get_balance() >= item.price:
			if idx == selected_index:
				color = Constants.UI_SHOP_ITEM_SELECTED_COLOR
			else:
				color = Constants.UI_SHOP_ITEM_AVAILABLE_COLOR
		else:
			color = Constants.UI_SHOP_ITEM_UNAVAILABLE_COLOR
		
		var item_text = item.name + " - " + str(item.price) + " cc"
		var item_size = font.get_string_size(item_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 18)
		var item_pos = Vector2(x + width / 2 - item_size.x / 2, y_offset)
		draw_string(font, item_pos, item_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 18, color)
		y_offset += 40

func _input(event):
	"""Обробляє події введення"""
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		handle_mouse_event(event.position)

func handle_mouse_event(mouse_pos: Vector2):
	"""Визначає, чи клікнули по товару"""
	var y_offset = y + 100
	for idx in range(items.size()):
		var item = items[idx]
		var item_text = item.name + " - " + str(item.price) + " cc"
		var item_size = font.get_string_size(item_text, HORIZONTAL_ALIGNMENT_CENTER, -1, 18)
		var item_rect = Rect2(x + width / 2 - item_size.x / 2, y_offset - item_size.y, item_size.x, item_size.y)
		
		if item_rect.has_point(mouse_pos):
			selected_index = idx
			var result = buy_selected()
			if result:
				print("Куплено: ", item.name)
			else:
				print("Недостатньо коштів для покупки: ", item.name)
			queue_redraw()
			return
		y_offset += 40
	
	selected_index = -1

func buy_selected():
	"""Спроба купити вибраний товар"""
	if selected_index >= 0 and selected_index < items.size():
		var item = items[selected_index]
		if CashManager.spend_catcoins(item.price):
			execute_item_effect(item)
			return true
		else:
			print("Недостатньо catcoin! Потрібно: ", item.price, ", є: ", CashManager.get_balance())
			return false
	return false

func execute_item_effect(item: ShopItem):
	"""Виконує ефект купленого товару"""
	match item.name:
		"Обернути фігуру":
			print("Режим обертання активовано! Клікніть на фігуру для обертання.")
			# TODO: Активувати режим обертання
		"Очистити 5 комірок":
			print("Очищено 5 випадкових комірок!")
			# TODO: Очистити 5 випадкових комірок на сітці
			var grid = get_parent().get_node("Grid")
			if grid:
				grid.clear_random_cells(5)

func handle_click(mouse_x: float, mouse_y: float, piece_box = null):
	"""Обробляє клік по товару та покупку (для зовнішнього використання)"""
	handle_mouse_event(Vector2(mouse_x, mouse_y))
