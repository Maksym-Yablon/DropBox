extends Node2D

# GameMain.gd - Головна сцена гри в Godot

# Компоненти гри
var grid: Grid
var piece_box: PieceBox
var shop: Shop
var ui: GameUI

# Стан гри
var running = true
var dragging = false
var dragged_piece = null
var dragged_piece_index = -1
var drag_offset = Vector2.ZERO
var waiting_for_rotate_click = false

# UI елементи
var pause_button: Button
var score_label: Label
var balance_label: Label

# Оптимізація
var game_over_check_counter = 0
var GAME_OVER_CHECK_INTERVAL = 60
var fps_counter = 0
var current_fps = 0
var FPS_UPDATE_INTERVAL = 30

func _ready():
	# Ініціалізуємо компоненти гри
	setup_game_components()
	setup_ui()
	
	# Завантажуємо збережену гру або починаємо нову
	load_or_start_new_game()

func setup_game_components():
	"""Налаштовує основні компоненти гри"""
	# Створюємо сітку
	grid = Grid.new(8, true)
	add_child(grid)
	grid.position = Vector2(Constants.GRID_X, Constants.GRID_Y)
	
	# Створюємо контейнер фігур
	piece_box = PieceBox.new(
		Constants.MOBILE_SIDE_MARGIN,
		Constants.PIECE_CONTAINER_Y,
		Constants.PIECE_CONTAINER_WIDTH,
		Constants.PIECE_CONTAINER_HEIGHT
	)
	add_child(piece_box)
	
	# Створюємо магазин
	var font = load("res://assets/fonts/default.ttf") if ResourceLoader.exists("res://assets/fonts/default.ttf") else ThemeDB.fallback_font
	shop = Shop.new(
		Constants.MOBILE_SIDE_MARGIN,
		Constants.SHOP_CONTAINER_Y,
		Constants.SHOP_CONTAINER_WIDTH,
		Constants.SHOP_CONTAINER_HEIGHT,
		font
	)
	add_child(shop)

func setup_ui():
	"""Налаштовує UI елементи"""
	# Створюємо лейбл рахунку
	score_label = Label.new()
	score_label.position = Vector2(20, 20)
	score_label.text = "Рахунок: 0"
	add_child(score_label)
	
	# Створюємо лейбл балансу
	balance_label = Label.new()
	balance_label.position = Vector2(20, 50)
	balance_label.text = "Catcoin: 0"
	add_child(balance_label)
	
	# Створюємо кнопку паузи
	pause_button = Button.new()
	pause_button.text = "⏸"
	pause_button.position = Vector2(Constants.SCREEN_WIDTH - 80, 20)
	pause_button.size = Vector2(60, 40)
	pause_button.pressed.connect(_on_pause_pressed)
	add_child(pause_button)

func load_or_start_new_game():
	"""Завантажує збережену гру або починає нову"""
	# TODO: Реалізувати завантаження збереженої гри
	reset_game()

func reset_game():
	"""Скидає гру до початкового стану"""
	if grid:
		grid.score = 0
		grid.combo_multiplier = 1
		grid.cells = []
		for i in range(grid.size):
			var row = []
			for j in range(grid.size):
				row.append(null)
			grid.cells.append(row)
		grid.generate_simple_initial_setup()
		grid.queue_redraw()
	
	if piece_box:
		piece_box._refill_pieces()
	
	update_ui()

func _process(_delta):
	"""Головний цикл гри"""
	# Оновлюємо UI
	update_ui()
	
	# Перевіряємо Game Over
	game_over_check_counter += 1
	if game_over_check_counter >= GAME_OVER_CHECK_INTERVAL:
		game_over_check_counter = 0
		check_game_over()
	
	# Оновлюємо FPS
	fps_counter += 1
	if fps_counter >= FPS_UPDATE_INTERVAL:
		current_fps = Engine.get_frames_per_second()
		fps_counter = 0

func update_ui():
	"""Оновлює UI елементи"""
	if score_label and grid:
		score_label.text = "Рахунок: " + str(grid.score)
	
	if balance_label:
		balance_label.text = "Catcoin: " + str(CashManager.get_balance())

func check_game_over():
	"""Перевіряє умови завершення гри"""
	if not piece_box or not grid:
		return
	
	# Перевіряємо, чи можна розмістити хоча б одну фігуру
	for piece in piece_box.pieces:
		if piece == null:
			continue
		
		# Перевіряємо всі можливі позиції на сітці
		for row in range(grid.size):
			for col in range(grid.size):
				if grid.can_place_piece(piece, col, row):
					return  # Фігуру можна розмістити, гра продовжується
	
	# Жодну фігуру не можна розмістити - Game Over
	game_over()

func game_over():
	"""Завершує гру"""
	print("Game Over! Фінальний рахунок: ", grid.score)
	SoundManager.play_game_over_sound()
	
	# TODO: Показати екран Game Over
	show_game_over_screen()

func show_game_over_screen():
	"""Показує екран завершення гри"""
	# TODO: Реалізувати екран Game Over
	print("Показуємо екран Game Over")

func _input(event):
	"""Обробляє події введення"""
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				_on_mouse_pressed(event.position)
			else:
				_on_mouse_released(event.position)
	
	elif event is InputEventMouseMotion and dragging:
		_on_mouse_motion(event.position)

func _on_mouse_pressed(mouse_pos: Vector2):
	"""Обробляє натискання миші"""
	# Перевіряємо чи клікнули на фігуру в контейнері
	if piece_box:
		var piece_index = piece_box._get_piece_at_position(mouse_pos)
		if piece_index != -1 and piece_box.pieces[piece_index] != null:
			dragging = true
			dragged_piece = piece_box.pieces[piece_index]
			dragged_piece_index = piece_index
			
			# Обчислюємо зміщення для плавного перетягування
			var piece_pos = piece_box.piece_positions[piece_index]
			drag_offset = mouse_pos - piece_pos
			
			SoundManager.play_click_sound()

func _on_mouse_released(mouse_pos: Vector2):
	"""Обробляє відпускання миші"""
	if dragging and dragged_piece != null and grid:
		var grid_pos = grid.mouse_to_grid(mouse_pos)
		
		if grid_pos.x != -1 and grid.can_place_piece(dragged_piece, grid_pos.x, grid_pos.y):
			# Розміщуємо фігуру на сітці
			if grid.place_piece(dragged_piece, grid_pos.x, grid_pos.y):
				# Видаляємо фігуру з контейнера
				piece_box.remove_piece(dragged_piece_index)
				
				# Очищуємо лінії та нараховуємо очки
				var lines_cleared = grid.clear_lines()
				if lines_cleared > 0:
					SoundManager.play_combo_sound(min(lines_cleared, 3))
					# Нараховуємо catcoin
					CashManager.update_from_score(lines_cleared * 10)
				
				# Перевіряємо, чи всі фігури використані
				if piece_box._all_pieces_used():
					piece_box._refill_pieces()
					# Бонус за використання всіх фігур
					CashManager.add_coins(5)
				
				SoundManager.play_pick_sound()
	
	# Скидаємо стан перетягування
	dragging = false
	dragged_piece = null
	dragged_piece_index = -1

func _on_mouse_motion(mouse_pos: Vector2):
	"""Обробляє рух миші під час перетягування"""
	if dragging and dragged_piece != null:
		# TODO: Реалізувати візуальне відображення фігури, що перетягується
		pass

func _on_pause_pressed():
	"""Обробляє натискання кнопки паузи"""
	get_tree().paused = not get_tree().paused
	print("Гра на паузі: ", get_tree().paused)

func save_game():
	"""Зберігає поточний стан гри"""
	# TODO: Реалізувати збереження гри
	print("Збереження гри...")

func _draw():
	"""Малює додаткові елементи гри"""
	# Малюємо фон
	draw_rect(Rect2(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), Constants.BACKGROUND_COLOR, true)
	
	# Малюємо FPS (якщо потрібно для налагодження)
	if Constants.TEST_MODE:
		var fps_text = "FPS: " + str(current_fps)
		var font = ThemeDB.fallback_font
		draw_string(font, Vector2(Constants.SCREEN_WIDTH - 100, Constants.SCREEN_HEIGHT - 20), fps_text, HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color.WHITE)

func _notification(what):
	"""Обробляє системні повідомлення"""
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		save_game()
		get_tree().quit()
