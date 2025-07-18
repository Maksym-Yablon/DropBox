# cash.py

class CashManager:
    def __init__(self):
        self.catcoins = 0
        self._unconverted_score = 0

    def update_from_score(self, score_increase):
        """
        Оновлює баланс catcoin на основі отриманих очок.
        Кожні 10 очок конвертуються в 1 catcoin.
        """
        total_potential_score = score_increase + self._unconverted_score
        new_coins = total_potential_score // 10
        self.catcoins += new_coins
        self._unconverted_score = total_potential_score % 10
        if new_coins > 0:
            print(f"Отримано {new_coins} catcoin!")

    def spend_catcoins(self, amount):
        """
        Витрачає catcoin, якщо на балансі достатньо коштів.
        Повертає True, якщо покупка успішна, інакше False.
        """
        if self.catcoins >= amount:
            self.catcoins -= amount
            return True
        return False

    def spend(self, amount):
        """Псевдонім для spend_catcoins для сумісності з магазином"""
        return self.spend_catcoins(amount)

    def get_balance(self):
        """Повертає поточний баланс catcoin."""
        return self.catcoins

    def set_balance(self, amount):
        """Встановлює баланс catcoin (для завантаження гри)."""
        self.catcoins = amount

# Створюємо єдиний екземпляр менеджера для всієї гри
cash_manager = CashManager()
