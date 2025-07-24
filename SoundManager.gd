extends Node

# SoundManager.gd - Автозавантаження для управління звуками

var sounds = {}
var music_player: AudioStreamPlayer
var sfx_players = []

var sfx_volume = 0.7
var music_volume = 0.1
var sound_enabled = true
var music_enabled = true

# Оптимізація: кешування і обмеження частоти звуків
var _sound_cooldowns = {}
var _min_sound_interval = 0.1  # Мінімальний інтервал між однаковими звуками (100ms)

func _ready():
	# Ініціалізуємо аудіо плеєри
	music_player = AudioStreamPlayer.new()
	add_child(music_player)
	music_player.volume_db = linear_to_db(music_volume)
	
	# Створюємо кілька SFX плеєрів для одночасного відтворення
	for i in range(8):
		var sfx_player = AudioStreamPlayer.new()
		add_child(sfx_player)
		sfx_player.volume_db = linear_to_db(sfx_volume)
		sfx_players.append(sfx_player)
	
	load_sounds()
	start_background_music()

func load_sounds():
	"""Завантажує всі звукові файли"""
	var sound_files = {
		"combo": "res://assets/sounds/effects/kombo 1.mp3",
		"combo2": "res://assets/sounds/effects/kombo_2.mp3",
		"new_game": "res://assets/sounds/effects/new_game.mp3",
		"pick": "res://assets/sounds/effects/pick.wav",
		"game_over": "res://assets/sounds/effects/game_over.mp3",
		"click": "res://assets/sounds/effects/click_may_2.wav",
		"shop": "res://assets/sounds/effects/pick_shop.wav",
		"grid_click": "res://assets/sounds/effects/click_grid.mp3",
		"background": "res://assets/sounds/music/back_musik.mp3"
	}
	
	for sound_name in sound_files:
		var sound_path = sound_files[sound_name]
		if ResourceLoader.exists(sound_path):
			sounds[sound_name] = load(sound_path)
		else:
			print("Не вдалося завантажити звук: ", sound_path)

func _can_play_sound(sound_name: String) -> bool:
	"""Перевіряє, чи можна відтворити звук (обмеження частоти)"""
	var current_time = Time.get_time_dict_from_system()
	var time_key = str(current_time.hour) + ":" + str(current_time.minute) + ":" + str(current_time.second)
	
	if sound_name in _sound_cooldowns:
		var last_time = _sound_cooldowns[sound_name]
		# Простий cooldown
		if last_time == time_key:
			return false
	
	_sound_cooldowns[sound_name] = time_key
	return true

func _get_available_sfx_player() -> AudioStreamPlayer:
	"""Повертає доступний SFX плеєр"""
	for player in sfx_players:
		if not player.playing:
			return player
	# Якщо всі зайняті, використовуємо перший
	return sfx_players[0]

func play_combo_sound(combo_level = 2):
	"""Відтворює звук комбо залежно від рівня"""
	if not sound_enabled or sfx_volume == 0:
		return
	
	var sound_name = "combo" if combo_level == 2 else "combo2"
	if not _can_play_sound(sound_name):
		return
	
	var sound_stream = null
	if combo_level == 2 and "combo" in sounds:
		sound_stream = sounds["combo"]
	elif combo_level >= 3 and "combo2" in sounds:
		sound_stream = sounds["combo2"]
	
	if sound_stream:
		var player = _get_available_sfx_player()
		player.stream = sound_stream
		player.play()

func play_new_game_sound():
	"""Відтворює звук нової гри"""
	if sound_enabled and sfx_volume > 0 and "new_game" in sounds and _can_play_sound("new_game"):
		var player = _get_available_sfx_player()
		player.stream = sounds["new_game"]
		player.play()

func play_pick_sound():
	"""Відтворює звук розміщення фігури"""
	if sound_enabled and sfx_volume > 0 and "pick" in sounds and _can_play_sound("pick"):
		var player = _get_available_sfx_player()
		player.stream = sounds["pick"]
		player.play()

func play_game_over_sound():
	"""Відтворює звук гейм овер"""
	if sound_enabled and sfx_volume > 0 and "game_over" in sounds and _can_play_sound("game_over"):
		var player = _get_available_sfx_player()
		player.stream = sounds["game_over"]
		player.play()

func play_rotate_sound():
	"""Відтворює звук обертання фігури"""
	if sound_enabled and sfx_volume > 0 and "pick" in sounds and _can_play_sound("rotate"):
		var player = _get_available_sfx_player()
		player.stream = sounds["pick"]
		player.play()

func play_clear_cells_sound():
	"""Відтворює звук очищення комірок"""
	if sound_enabled and sfx_volume > 0 and "combo" in sounds:
		var player = _get_available_sfx_player()
		player.stream = sounds["combo"]
		player.play()

func play_click_sound():
	"""Відтворює звук кліку"""
	if sound_enabled and sfx_volume > 0 and "click" in sounds and _can_play_sound("click"):
		var player = _get_available_sfx_player()
		player.stream = sounds["click"]
		player.play()

func play_shop_sound():
	"""Відтворює звук магазину"""
	if sound_enabled and sfx_volume > 0 and "shop" in sounds and _can_play_sound("shop"):
		var player = _get_available_sfx_player()
		player.stream = sounds["shop"]
		player.play()

func start_background_music():
	"""Запускає фонову музику"""
	if music_enabled and "background" in sounds:
		music_player.stream = sounds["background"]
		music_player.play()
		music_player.finished.connect(_on_music_finished)

func _on_music_finished():
	"""Перезапускає музику в циклі"""
	if music_enabled:
		music_player.play()

func stop_background_music():
	"""Зупиняє фонову музику"""
	music_player.stop()

func play_sound(sound_name: String):
	"""Відтворює звук за назвою"""
	if sound_enabled and sound_name in sounds:
		var player = _get_available_sfx_player()
		player.stream = sounds[sound_name]
		player.play()

func set_sfx_volume(volume: float):
	"""Встановлює гучність звукових ефектів"""
	sfx_volume = clamp(volume, 0.0, 1.0)
	for player in sfx_players:
		player.volume_db = linear_to_db(sfx_volume)

func set_music_volume(volume: float):
	"""Встановлює гучність музики"""
	music_volume = clamp(volume, 0.0, 1.0)
	music_player.volume_db = linear_to_db(music_volume)

func toggle_sound():
	"""Перемикає звукові ефекти"""
	sound_enabled = not sound_enabled
	return sound_enabled

func toggle_music():
	"""Перемикає музику"""
	music_enabled = not music_enabled
	if music_enabled:
		start_background_music()
	else:
		stop_background_music()
	return music_enabled

func stop_all_sounds():
	"""Зупиняє всі звуки"""
	for player in sfx_players:
		player.stop()
	music_player.stop()

func is_sound_enabled() -> bool:
	return sound_enabled

func is_music_enabled() -> bool:
	return music_enabled
