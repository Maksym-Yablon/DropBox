extends Resource
class_name SaveManager

# SaveManager.gd - Управління збереженнями гри

var save_file_path = "user://game_save.save"

func save_game(grid: Grid, piece_box: PieceBox) -> bool:
	"""Зберігає поточний стан гри"""
	if not grid or not piece_box:
		return false
	
	var save_data = {
		"has_save": true,
		"score": grid.score,
		"catcoins": CashManager.get_balance(),
		"grid_cells": _serialize_grid(grid),
		"pieces_in_box": _serialize_pieces(piece_box),
		"save_date": Time.get_datetime_string_from_system()
	}
	
	var file = FileAccess.open(save_file_path, FileAccess.WRITE)
	if file:
		var json_string = JSON.stringify(save_data)
		file.store_string(json_string)
		file.close()
		print("Гру збережено! Очки: ", grid.score)
		return true
	else:
		print("Помилка збереження гри")
		return false

func load_game():
	"""Завантажує збережений стан гри"""
	if not FileAccess.file_exists(save_file_path):
		return null
	
	var file = FileAccess.open(save_file_path, FileAccess.READ)
	if not file:
		return null
	
	var json_string = file.get_as_text()
	file.close()
	
	var json = JSON.new()
	var parse_result = json.parse(json_string)
	if parse_result != OK:
		return null
	
	var save_data = json.data
	if not save_data.get("has_save", false):
		return null
	
	return {
		"score": save_data.get("score", 0),
		"catcoins": save_data.get("catcoins", 0),
		"grid_cells": _deserialize_grid(save_data.get("grid_cells", [])),
		"pieces_in_box": _deserialize_pieces(save_data.get("pieces_in_box", [])),
		"save_date": save_data.get("save_date", "")
	}

func has_saved_game() -> bool:
	"""Перевіряє, чи є збережена гра"""
	if not FileAccess.file_exists(save_file_path):
		return false
	
	var save_data = load_game()
	return save_data != null

func delete_save() -> bool:
	"""Видаляє збережену гру"""
	if FileAccess.file_exists(save_file_path):
		var dir = DirAccess.open("user://")
		if dir:
			dir.remove(save_file_path)
			return true
	return false

func _serialize_grid(grid: Grid) -> Array:
	"""Серіалізує сітку для збереження"""
	var serialized_grid = []
	for row in grid.cells:
		var serialized_row = []
		for cell in row:
			if cell == null:
				serialized_row.append(null)
			else:
				# Зберігаємо колір як масив [r, g, b, a]
				serialized_row.append([cell.r, cell.g, cell.b, cell.a])
		serialized_grid.append(serialized_row)
	return serialized_grid

func _deserialize_grid(serialized_grid: Array) -> Array:
	"""Десеріалізує сітку з збереження"""
	var grid_cells = []
	for row in serialized_grid:
		var grid_row = []
		for cell in row:
			if cell == null:
				grid_row.append(null)
			else:
				# Відновлюємо колір з масиву
				grid_row.append(Color(cell[0], cell[1], cell[2], cell[3]))
		grid_cells.append(grid_row)
	return grid_cells

func _serialize_pieces(piece_box: PieceBox) -> Array:
	"""Серіалізує фігури для збереження"""
	var serialized_pieces = []
	for piece in piece_box.pieces:
		if piece == null:
			serialized_pieces.append(null)
		else:
			serialized_pieces.append({
				"shape": piece.shape,
				"color": [piece.color.r, piece.color.g, piece.color.b, piece.color.a]
			})
	return serialized_pieces

func _deserialize_pieces(serialized_pieces: Array) -> Array:
	"""Десеріалізує фігури з збереження"""
	var pieces = []
	for piece_data in serialized_pieces:
		if piece_data == null:
			pieces.append(null)
		else:
			var piece = Piece.new()
			piece.shape = piece_data.shape
			piece.color = Color(piece_data.color[0], piece_data.color[1], piece_data.color[2], piece_data.color[3])
			pieces.append(piece)
	return pieces
