extends Resource
class_name RecordsManager

# RecordsManager.gd - Управління рекордами гри

var records = []
var records_file_path = "user://records.save"

func _init():
	load_records()

func load_records():
	"""Завантажує рекорди з файлу"""
	if FileAccess.file_exists(records_file_path):
		var file = FileAccess.open(records_file_path, FileAccess.READ)
		if file:
			var json_string = file.get_as_text()
			file.close()
			
			var json = JSON.new()
			var parse_result = json.parse(json_string)
			if parse_result == OK:
				records = json.data
			else:
				print("Помилка парсингу рекордів")
				records = []
	else:
		records = []

func save_records():
	"""Зберігає рекорди у файл"""
	var file = FileAccess.open(records_file_path, FileAccess.WRITE)
	if file:
		var json_string = JSON.stringify(records)
		file.store_string(json_string)
		file.close()
		print("Рекорди збережено")
	else:
		print("Помилка збереження рекордів")

func add_record(score: int, player_name: String = "Гравець"):
	"""Додає новий рекорд"""
	var new_record = {
		"score": score,
		"player": player_name,
		"date": Time.get_datetime_string_from_system()
	}
	
	records.append(new_record)
	
	# Сортуємо рекорди за очками (від найбільшого до найменшого)
	records.sort_custom(func(a, b): return a.score > b.score)
	
	# Залишаємо тільки топ-10 рекордів
	if records.size() > 10:
		records = records.slice(0, 10)
	
	save_records()
	return is_new_record(score)

func is_new_record(score: int) -> bool:
	"""Перевіряє, чи є результат новим рекордом"""
	if records.size() == 0:
		return true
	
	if records.size() < 10:
		return true
	
	return score > records[-1].score

func get_best_score() -> int:
	"""Повертає найкращий результат"""
	if records.size() > 0:
		return records[0].score
	return 0

func get_top_records(count: int = 10) -> Array:
	"""Повертає топ рекордів"""
	return records.slice(0, min(count, records.size()))

func clear_records():
	"""Очищає всі рекорди"""
	records = []
	save_records()
