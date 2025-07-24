extends Node
class_name GameUI

## Основний інтерфейс гри, повна адаптація ui.py для Godot v4.4.1

# --- Глобальні константи (автозавантаження або preload) ---
const Constants = preload("res://Constants.gd")

# --- UIEffects ---
class UIEffects:
	var blink_start_time := 0.0
	var blink_duration := 1.0
	var is_blinking := false
	var _last_alpha := null
	var _alpha_update_interval := 0.05
	var _last_alpha_update := 0.0

	func start_blinking():
		blink_start_time = Time.get_unix_time_from_system()
		is_blinking = true

	func stop_blinking():
		is_blinking = false

	func get_blink_alpha() -> int:
		if not is_blinking:
			return 140
		var current_time = Time.get_unix_time_from_system()
		if current_time - _last_alpha_update < _alpha_update_interval and _last_alpha != null:
			return _last_alpha
		var elapsed = current_time - blink_start_time
		var blink_cycle = sin(elapsed * (2 * PI / blink_duration))
		var alpha = int(100 + blink_cycle * 50)
		alpha = clamp(alpha, 80, 160)
		_last_alpha = alpha
		_last_alpha_update = current_time
		return alpha

# --- PauseButton ---
class PauseButton:
	var rect: Rect2
	var hovered := false
	var font: Font

	func _init():
		rect = Rect2(Constants.PAUSE_BUTTON_X, Constants.PAUSE_BUTTON_Y, Constants.PAUSE_BUTTON_SIZE, Constants.PAUSE_BUTTON_SIZE)
		font = load(Constants.UI_FONT_FAMILY_DEFAULT)

	func handle_mouse_motion(mouse_pos: Vector2):
		hovered = rect.has_point(mouse_pos)

	func handle_click(mouse_pos: Vector2) -> bool:
		if rect.has_point(mouse_pos):
			Constants.SoundManager.play_click_sound()
			return true
		return false

	func draw(canvas_item):
		var color = Constants.PAUSE_BUTTON_HOVER if hovered else Constants.PAUSE_BUTTON_COLOR
		canvas_item.draw_rect(rect, color, true, 8)
		canvas_item.draw_rect(rect, Constants.PAUSE_BUTTON_BORDER, false, 8)
		canvas_item.draw_string(font, rect.position + rect.size/2, "II", Constants.TEXT_COLOR)

# --- ControlPanel ---
class ControlPanel:
	var is_visible := true
	var hover_button := null
	var buttons := {}
	var font: Font
	var screen: Control

	func _init(_screen: Control):
		screen = _screen
		font = load(Constants.UI_FONT_FAMILY_ARIAL)
		_create_buttons()

	func _create_buttons():
		buttons = {
			"pause": _make_button(0, "⏸ Пауза"),
			"restart": _make_button(1, "Нова гра"),
			"settings": _make_button(2, "Налаштування"),
			"help": _make_button(3, "Допомога"),
			"menu": _make_button(4, "Меню")
		}

	func _make_button(index: int, text: String) -> Dictionary:
		var y_pos = Constants.CONTROL_PANEL_Y + 50 + index * (Constants.CONTROL_BUTTON_HEIGHT + Constants.CONTROL_BUTTON_MARGIN)
		return {
			"rect": Rect2(Constants.CONTROL_PANEL_X + 25, y_pos, Constants.CONTROL_BUTTON_WIDTH, Constants.CONTROL_BUTTON_HEIGHT),
			"text": text,
			"enabled": true
		}

	func handle_mouse_motion(mouse_pos: Vector2):
		hover_button = null
		if is_visible:
			for button_name in buttons.keys():
				if buttons[button_name]["rect"].has_point(mouse_pos):
					hover_button = button_name
					break

	func handle_click(mouse_pos: Vector2) -> String:
		if not is_visible:
			return ""
		for button_name in buttons.keys():
			var button = buttons[button_name]
			if button["rect"].has_point(mouse_pos) and button["enabled"]:
				return button_name
		return ""

	func toggle_visibility():
		is_visible = not is_visible

	func draw(canvas_item):
		if not is_visible:
			return
		var panel_rect = Rect2(Constants.CONTROL_PANEL_X, Constants.CONTROL_PANEL_Y, Constants.CONTROL_PANEL_WIDTH, Constants.CONTROL_PANEL_HEIGHT)
		canvas_item.draw_rect(panel_rect, Constants.CONTROL_PANEL_BG, true, 15)
		canvas_item.draw_rect(panel_rect, Constants.CONTROL_PANEL_BORDER, false, 15)
		canvas_item.draw_string(font, Vector2(panel_rect.position.x + panel_rect.size.x/2, panel_rect.position.y + 25), "Керування", Constants.CONTROL_BUTTON_TEXT)
		for button_name in buttons.keys():
			var button = buttons[button_name]
			var color = Constants.CONTROL_BUTTON_HOVER if button_name == hover_button else Constants.CONTROL_BUTTON_COLOR
			canvas_item.draw_rect(button["rect"], color, true, 8)
			canvas_item.draw_rect(button["rect"], Constants.CONTROL_PANEL_BORDER, false, 8)
			canvas_item.draw_string(font, button["rect"].position + button["rect"].size/2, button["text"], Constants.CONTROL_BUTTON_TEXT)

# --- PauseMenu ---
class PauseMenu:
	var is_paused := false
	var overlay_alpha := 128
	var buttons := []

	func _init():
		_create_buttons()

	func _create_buttons():
		var button_width = 200
		var button_height = 50
		var button_spacing = 60
		var start_x = (Constants.SCREEN_WIDTH - button_width) / 2
		var start_y = (Constants.SCREEN_HEIGHT - (5 * button_height + 4 * button_spacing)) / 2
		var buttons_data = [
			["resume", "Продовжити"],
			["restart", "Перезапустити"],
			["settings", "Налаштування"],
			["help", "Допомога"],
			["menu", "Головне меню"]
		]
		for i in buttons_data.size():
			var y = start_y + i * (button_height + button_spacing)
			buttons.append({
				"action": buttons_data[i][0],
				"rect": Rect2(start_x, y, button_width, button_height),
				"text": buttons_data[i][1],
				"hovered": false
			})

	func toggle_pause() -> bool:
		is_paused = not is_paused
		return is_paused

	func handle_click(mouse_pos: Vector2) -> String:
		if not is_paused:
			return ""
		for button in buttons:
			if button["rect"].has_point(mouse_pos):
				Constants.SoundManager.play_click_sound()
				return button["action"]
		return ""

	func handle_mouse_motion(mouse_pos: Vector2):
		if not is_paused:
			return
		for button in buttons:
			button["hovered"] = button["rect"].has_point(mouse_pos)

	func draw(canvas_item):
		if not is_paused:
			return
		var overlay_rect = Rect2(Vector2.ZERO, Vector2(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
		canvas_item.draw_rect(overlay_rect, Color(0,0,0,overlay_alpha/255.0), true)
		var title_font = load(Constants.UI_FONT_FAMILY_DEFAULT)
		canvas_item.draw_string(title_font, Vector2(Constants.SCREEN_WIDTH/2, 150), "ПАУЗА", Constants.TEXT_COLOR)
		for button in buttons:
			var button_color = Constants.CONTROL_BUTTON_HOVER if button["hovered"] else Constants.CONTROL_BUTTON_COLOR
			canvas_item.draw_rect(button["rect"], button_color, true, 8)
			canvas_item.draw_rect(button["rect"], Constants.TEXT_COLOR, false, 8)
			canvas_item.draw_string(title_font, button["rect"].position + button["rect"].size/2, button["text"], Constants.CONTROL_BUTTON_TEXT)

# --- GameUI ---
var ui_effects := UIEffects.new()
var control_panel := null
var pause_menu := null
var settings_menu := null
var game_over_screen := null
var menu_system := null
var global_cursor := null

func _ready():
	control_panel = ControlPanel.new(self)
	pause_menu = PauseMenu.new()
	# settings_menu, game_over_screen, menu_system, global_cursor — ініціалізуються у відповідних сценах

func draw_hud(score: int, best_score: int):
	var font = load(Constants.UI_FONT_FAMILY_ARIAL)
	var offset_x = int(Constants.SCREEN_WIDTH * 0.02)
	var offset_y = int(Constants.SCREEN_HEIGHT * 0.02)
	draw_string(font, Vector2(35 - offset_x, offset_y), "Рекорд: %s" % best_score, Constants.UI_HUD_RECORD_COLOR)
	draw_string(font, Vector2(Constants.SCREEN_WIDTH/2, offset_y), "Очки: %s" % score, Constants.UI_HUD_SCORE_COLOR)
	var hint_font = load(Constants.UI_FONT_FAMILY_ARIAL)
	draw_string(hint_font, Vector2(Constants.SCREEN_WIDTH - 30, 30), "N - Нова гра", Constants.UI_HINT_COLOR)

func draw_fps(fps: float, show_fps := true):
	if not show_fps:
		return
	var color := Color(0,1,0) if fps >= 50 else Color(1,1,0) if fps >= 30 else Color(1,0.65,0) if fps >= 20 else Color(1,0,0)
	var font = load(Constants.UI_FONT_FAMILY_ARIAL)
	var text = "FPS: %.1f" % fps
	var pos = Vector2(Constants.SCREEN_WIDTH - 10, Constants.SCREEN_HEIGHT - 10)
	draw_string(font, pos, text, color)
