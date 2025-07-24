extends Node2D
class_name Grid
# Додаємо імпорт Piece для доступу до Piece.generate_weighted_random_piece()
const Piece = preload("res://Piece.gd")

# Клас для управління ігровою сіткою 8x8 в Godot

var size = 8
var cells = []  # Двовимірний масив для збереження кольорів блоків
var score = 0
var combo_multiplier = 1
var last_clear_success = false

# Кешування для оптимізації
var _cached_grid_rect = null
var _cached_cell_rects = []
var _cached_offset_x = 0
var _cached_offset_y = 0
var _last_cell_size = 0

func _init(grid_size = 8, generate_initial = true):
	size = grid_size
	cells = []
	for i in range(size):
		var row = []
		for j in range(size):
			row.append(null)
		cells.append(row)
	
	score = 0
	combo_multiplier = 1
	last_clear_success = false
	
	if generate_initial:
		generate_simple_initial_setup()

func generate_simple_initial_setup():
	"""Проста генерація початкових фігур на сітці"""
	var num_pieces = randi_range(5, 15)
	var placed_pieces = 0
	var max_attempts = 30
	
	print("Генерація ", num_pieces, " початкових фігур...")
	
	for attempt in range(max_attempts):
		if placed_pieces >= num_pieces:
			break
		
		var piece = Piece.generate_weighted_random_piece()
		var grid_x = randi() % (size - 3)
		var grid_y = randi() % (size - 3)
		
		if can_place_piece(piece, grid_x, grid_y):
			place_piece(piece, grid_x, grid_y)
			placed_pieces += 1
	
	if placed_pieces < num_pieces:
		print("Вдалося розмістити лише ", placed_pieces, " з ", num_pieces, " фігур")
	else:
		print("Успішно розміщено всі ", placed_pieces, " фігур")
	
	_check_and_clear_initial_lines()
	score = 0

func _check_and_clear_initial_lines():
	"""Перевіряє та очищує повні лінії після початкової генерації"""
	var lines_cleared = 0
	var max_iterations = 10
	
	for iteration in range(max_iterations):
		var cleared_this_iteration = clear_lines()
		if cleared_this_iteration == 0:
			break
		lines_cleared += cleared_this_iteration
	
	if lines_cleared > 0:
		print("Очищено ", lines_cleared, " ліній після генерації")

func _cache_grid_layout(cell_size):
	"""Кешує розміщення сітки для оптимізації"""
	if _last_cell_size == cell_size and _cached_cell_rects.size() > 0:
		return
	
	_last_cell_size = cell_size
	_cached_offset_x = Constants.GRID_X
	_cached_offset_y = Constants.GRID_Y
	
	# Кешуємо головний прямокутник сітки
	var grid_width = size * cell_size
	var grid_height = size * cell_size
	_cached_grid_rect = Rect2(_cached_offset_x - 10, _cached_offset_y - 10, grid_width + 20, grid_height + 20)
	
	# Кешуємо прямокутники всіх клітинок
	var cell_margin = 3
	var inner_cell_size = cell_size - cell_margin
	_cached_cell_rects = []
	
	for row in range(size):
		var row_rects = []
		for col in range(size):
			var cell_x = _cached_offset_x + col * cell_size + cell_margin / 2
			var cell_y = _cached_offset_y + row * cell_size + cell_margin / 2
			row_rects.append(Rect2(cell_x, cell_y, inner_cell_size, inner_cell_size))
		_cached_cell_rects.append(row_rects)

func _draw():
	"""Малює сітку з м'якими кольорами та заокругленими кутами"""
	var cell_size = Constants.GRID_CELL_SIZE
	_cache_grid_layout(cell_size)
	
	# Малюємо фон сітки
	draw_rect(_cached_grid_rect, Constants.GRID_BACKGROUND_COLOR, true)
	draw_rect(_cached_grid_rect, Constants.GRID_BORDER_COLOR, false, 3)
	
	# Малюємо клітинки
	var cell_margin = 6  # Відступ між клітинками для м'якого вигляду
	var cell_border_radius = Constants.GRID_CELL_BORDER_RADIUS
	
	for row in range(size):
		for col in range(size):
			var cell_x = _cached_offset_x + col * cell_size + cell_margin / 2
			var cell_y = _cached_offset_y + row * cell_size + cell_margin / 2
			var cell_size_adjusted = cell_size - cell_margin
			var cell_rect = Rect2(cell_x, cell_y, cell_size_adjusted, cell_size_adjusted)
			
			var cell_color = cells[row][col] if cells[row][col] != null else Constants.EMPTY_CELL_COLOR
			
			# Заокруглений прямокутник для клітинки
			draw_rect(cell_rect, cell_color, true, -1, cell_border_radius)
			
			# М'який контур
			if cells[row][col] != null:
				draw_rect(cell_rect, Constants.PIECE_OUTLINE_COLOR, false, 2, cell_border_radius)
			else:
				draw_rect(cell_rect, Constants.GRID_LINE_COLOR, false, 1, cell_border_radius)

func is_row_full(row):
	"""Перевіряє, чи заповнений рядок повністю"""
	for col in range(size):
		if cells[row][col] == null:
			return false
	return true

func is_col_full(col):
	"""Перевіряє, чи заповнена колонка повністю"""
	for row in range(size):
		if cells[row][col] == null:
			return false
	return true

func clear_full_rows():
	"""Очищує повні рядки"""
	var cleared_count = 0
	for row in range(size):
		if is_row_full(row):
			for col in range(size):
				cells[row][col] = null
			cleared_count += 1
	return cleared_count

func clear_full_cols():
	"""Очищує повні колонки"""
	var cleared_count = 0
	for col in range(size):
		if is_col_full(col):
			for row in range(size):
				cells[row][col] = null
			cleared_count += 1
	return cleared_count

func clear_lines():
	"""Головна функція очищення ліній"""
	var rows_cleared = clear_full_rows()
	var cols_cleared = clear_full_cols()
	var total_cleared = rows_cleared + cols_cleared
	
	if total_cleared > 0:
		var points = total_cleared * 50 * combo_multiplier
		score += points
		combo_multiplier += 1
		last_clear_success = true
		queue_redraw()  # Перемалювати сітку
	else:
		combo_multiplier = 1
		last_clear_success = false
	
	return total_cleared

func mouse_to_grid(mouse_pos):
	"""Конвертує позицію миші в координати сітки"""
	var grid_x = int((mouse_pos.x - Constants.GRID_X) / Constants.GRID_CELL_SIZE)
	var grid_y = int((mouse_pos.y - Constants.GRID_Y) / Constants.GRID_CELL_SIZE)
	
	if grid_x >= 0 and grid_x < size and grid_y >= 0 and grid_y < size:
		return Vector2i(grid_x, grid_y)
	return Vector2i(-1, -1)

func can_place_piece(piece, grid_x, grid_y):
	"""Перевіряє, чи можна розмістити фігуру в заданій позиції"""
	for row in range(piece.shape.size()):
		for col in range(piece.shape[row].size()):
			if piece.shape[row][col] == 1:
				var cell_x = grid_x + col
				var cell_y = grid_y + row
				
				if cell_x < 0 or cell_x >= size or cell_y < 0 or cell_y >= size:
					return false
				
				if cells[cell_y][cell_x] != null:
					return false
	return true

func place_piece(piece, grid_x, grid_y):
	"""Розміщує фігуру на сітці"""
	if not can_place_piece(piece, grid_x, grid_y):
		return false
	
	for row in range(piece.shape.size()):
		for col in range(piece.shape[row].size()):
			if piece.shape[row][col] == 1:
				var cell_x = grid_x + col
				var cell_y = grid_y + row
				cells[cell_y][cell_x] = piece.color
	
	queue_redraw()  # Перемалювати сітку
	return true

func highlight_position(grid_pos, piece, valid = true):
	"""Підсвічує позицію для розміщення фігури"""
	# TODO: Реалізувати підсвічування
	pass

func print_grid_state(title = "Стан сітки"):
	"""Виводить стан сітки в консоль для налагодження"""
	print(title)
	for row in cells:
		var row_str = ""
		for cell in row:
			if cell == null:
				row_str += "- "
			else:
				row_str += "# "
		print(row_str)

func clear_random_cells(count = 5):
	"""Очищує випадкові заповнені клітинки"""
	var filled_cells = []
	for row in range(size):
		for col in range(size):
			if cells[row][col] != null:
				filled_cells.append(Vector2i(col, row))
	
	if filled_cells.size() == 0:
		return 0
	
	var cleared_count = min(count, filled_cells.size())
	filled_cells.shuffle()
	
	for i in range(cleared_count):
		var pos = filled_cells[i]
		cells[pos.y][pos.x] = null
	
	queue_redraw()
	return cleared_count
