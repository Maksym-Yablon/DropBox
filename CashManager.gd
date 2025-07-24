extends Node

# CashManager.gd - Автозавантаження для управління валютою гри

var catcoins = 0
var _unconverted_score = 0

func _ready():
	# Ініціалізація менеджера валюти
	catcoins = 0
	_unconverted_score = 0

func add_coins(amount):
	"""Додає вказану кількість catcoin до балансу."""
	catcoins += amount

func update_from_score(score_increase):
	"""
	Оновлює баланс catcoin на основі отриманих очок.
	Кожні 10 очок конвертуються в 1 catcoin.
	"""
	var total_potential_score = score_increase + _unconverted_score
	var new_coins = total_potential_score / 10
	catcoins += new_coins
	_unconverted_score = total_potential_score % 10
	if new_coins > 0:
		print("Отримано ", new_coins, " catcoin!")

func spend_catcoins(amount):
	"""
	Витрачає catcoin, якщо на балансі достатньо коштів.
	Повертає true, якщо покупка успішна, інакше false.
	"""
	if catcoins >= amount:
		catcoins -= amount
		return true
	return false

func spend(amount):
	"""Псевдонім для spend_catcoins для сумісності з магазином"""
	return spend_catcoins(amount)

func get_balance():
	"""Повертає поточний баланс catcoin."""
	return catcoins

func set_balance(amount):
	"""Встановлює баланс catcoin (для завантаження гри)."""
	catcoins = amount

func get_cash():
	"""Псевдонім для get_balance для сумісності"""
	return get_balance()

func spend_cash(amount):
	"""Псевдонім для spend_catcoins для сумісності"""
	return spend_catcoins(amount)

func apply_bonus_multiplier(score):
	"""Застосовує бонусний множник до очок"""
	var bonus_coins = score / 5  # 1 catcoin за кожні 5 очок бонусу
	add_coins(bonus_coins)
	print("Бонус застосовано! Отримано ", bonus_coins, " catcoin!")
