extends Node2D
class_name PieceBox

# PieceBox.gd - Контейнер для фігур з drag & drop функціональністю

var pieces = []
var next_piece = null
var dragging_index = null
var dragging = false
var drag_offset = Vector2.ZERO

# Позиції та розміри
var start_x
var start_y
var width
var height
var piece_positions = []

func _init(x = 0, y = 0, w = 400, h = 150):
	start_x = x
	start_y = y
	width = w
	height = h
	
	# Генеруємо початкові фігури
	pieces = [
		Piece.generate_weighted_random_piece(),
		Piece.generate_weighted_random_piece(),
		Piece.generate_weighted_random_piece()
	]
	next_piece = Piece.generate_weighted_random_piece()
	dragging_index = null
	
	_calculate_piece_positions()

func _ready():
	# Підключаємо сигнали для обробки введення
	pass

func _calculate_piece_positions():
	"""Обчислює позиції фігур в контейнері"""
	piece_positions = []
	var piece_width = width / 3
	
	for i in range(3):
		var piece_x = start_x + i * piece_width + piece_width / 2
		var piece_y = start_y + height / 2
		piece_positions.append(Vector2(piece_x, piece_y))

func _draw():
	"""Малює контейнер та фігури"""
	# Малюємо фон контейнера
	var container_rect = Rect2(start_x, start_y, width, height)
	draw_rect(container_rect, Constants.PIECE_BOX_FILL_COLOR, true, -1, 10)
	draw_rect(container_rect, Constants.PIECE_BOX_BORDER_COLOR, false, 3, 10)
	
	# Малюємо фігури
	for i in range(pieces.size()):
		if pieces[i] != null and i != dragging_index:
			var pos = piece_positions[i]
			var piece_size = Constants.PIECE_CONTAINER_CELL_SIZE
			
			# Центруємо фігуру
			var piece_dims = _get_piece_dimensions(pieces[i])
			var center_x = pos.x - (piece_dims.x * piece_size) / 2
			var center_y = pos.y - (piece_dims.y * piece_size) / 2
			
			pieces[i].draw(self, center_x, center_y, piece_size)

func _get_piece_dimensions(piece):
	"""Повертає розміри фігури"""
	if piece == null or piece.shape.size() == 0:
		return Vector2(1, 1)
	
	var rows = piece.shape.size()
	var cols = piece.shape[0].size()
	return Vector2(cols, rows)

func _input(event):
	"""Обробляє події введення для drag & drop"""
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				_on_mouse_pressed(event.position)
			else:
				_on_mouse_released(event.position)
	
	elif event is InputEventMouseMotion and dragging:
		_on_mouse_motion(event.position)

func _on_mouse_pressed(mouse_pos):
	"""Обробляє натискання миші"""
	var piece_index = _get_piece_at_position(mouse_pos)
	if piece_index != -1 and pieces[piece_index] != null:
		dragging_index = piece_index
		dragging = true
		
		# Обчислюємо зміщення для плавного перетягування
		var piece_pos = piece_positions[piece_index]
		drag_offset = mouse_pos - piece_pos
		
		queue_redraw()

func _on_mouse_released(mouse_pos):
	"""Обробляє відпускання миші"""
	if dragging and dragging_index != null:
		# Перевіряємо, чи можна розмістити фігуру на сітці
		var grid = get_parent().get_node("Grid")  # Припускаємо, що Grid є сусіднім вузлом
		if grid:
			var grid_pos = grid.mouse_to_grid(mouse_pos)
			if grid_pos.x != -1 and grid.can_place_piece(pieces[dragging_index], grid_pos.x, grid_pos.y):
				# Розміщуємо фігуру
				grid.place_piece(pieces[dragging_index], grid_pos.x, grid_pos.y)
				
				# Видаляємо фігуру з контейнера
				pieces[dragging_index] = null
				
				# Перевіряємо, чи всі фігури використані
				if _all_pieces_used():
					_refill_pieces()
	
	dragging = false
	dragging_index = null
	queue_redraw()

func _on_mouse_motion(mouse_pos):
	"""Обробляє рух миші під час перетягування"""
	if dragging and dragging_index != null:
		# Оновлюємо позицію фігури, що перетягується
		queue_redraw()

func _get_piece_at_position(mouse_pos):
	"""Повертає індекс фігури в позиції миші"""
	for i in range(piece_positions.size()):
		if pieces[i] == null:
			continue
		
		var pos = piece_positions[i]
		var piece_size = Constants.PIECE_CONTAINER_CELL_SIZE
		var piece_dims = _get_piece_dimensions(pieces[i])
		
		var piece_rect = Rect2(
			pos.x - (piece_dims.x * piece_size) / 2,
			pos.y - (piece_dims.y * piece_size) / 2,
			piece_dims.x * piece_size,
			piece_dims.y * piece_size
		)
		
		if piece_rect.has_point(mouse_pos):
			return i
	
	return -1

func _all_pieces_used():
	"""Перевіряє, чи всі фігури використані"""
	for piece in pieces:
		if piece != null:
			return false
	return true

func _refill_pieces():
	"""Поповнює контейнер новими фігурами"""
	pieces = [
		Piece.generate_weighted_random_piece(),
		Piece.generate_weighted_random_piece(),
		Piece.generate_weighted_random_piece()
	]
	next_piece = Piece.generate_weighted_random_piece()
	queue_redraw()

func get_piece_at_mouse(mouse_pos):
	"""Повертає фігуру в позиції миші (для зовнішнього використання)"""
	var index = _get_piece_at_position(mouse_pos)
	if index != -1:
		return pieces[index]
	return null

func remove_piece(index):
	"""Видаляє фігуру за індексом"""
	if index >= 0 and index < pieces.size():
		pieces[index] = null
		queue_redraw()

func rotate_piece(index):
	"""Обертає фігуру за індексом"""
	if index >= 0 and index < pieces.size() and pieces[index] != null:
		if pieces[index].can_rotate():
			pieces[index].rotate_90_clockwise()
			queue_redraw()
			return true
	return false
