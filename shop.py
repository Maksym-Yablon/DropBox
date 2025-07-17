# Внутрішньоігровий магазин
import pygame
from cash import cash_manager

class ShopItem:
    def __init__(self, name, price, description, icon=None):
        self.name = name
        self.price = price
        self.description = description
        self.icon = icon  # pygame.Surface або шлях до зображення

class Shop:
    def __init__(self, x, y, width, height, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.items = self.create_items()
        self.selected_index = None

    def create_items(self):
        # Список товарів магазину (можна розширювати)
        return [
            ShopItem("Підказка", 5, "Показує найкращий хід"),
            ShopItem("Тест товар", 1, "Тестовий предмет для перевірки")
        ]

    def draw(self, surface):
        # Малюємо панель магазину в стилі контейнера фігур
        # Створюємо поверхню з прозорістю для заливки
        shop_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Заливка з прозорістю (використовуємо інший колір ніж для фігур)
        fill_color = (100, 149, 237, 40)  # Корнфлавер синій з прозорістю 40/255
        pygame.draw.rect(shop_surface, fill_color, (0, 0, self.width, self.height), border_radius=10)
        
        # Малюємо заливку на екрані
        surface.blit(shop_surface, (self.x, self.y))
        
        # Обводка (синій колір замість коричневого)
        border_color = (70, 130, 180)  # Сталево-синій
        pygame.draw.rect(surface, border_color, (self.x, self.y, self.width, self.height), width=2, border_radius=10)
        
        # Заголовок магазину по центру контейнера
        title = self.font.render("МАГАЗИН", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.x + self.width // 2, self.y + 30))
        surface.blit(title, title_rect)
        
        # Показуємо баланс catcoin по центру контейнера
        balance_text = self.font.render(f"{cash_manager.get_balance()} catcoin", True, (255, 215, 0))
        balance_rect = balance_text.get_rect(center=(self.x + self.width // 2, self.y + 60))
        surface.blit(balance_text, balance_rect)
        
        # Малюємо товари
        y_offset = self.y + 100
        for idx, item in enumerate(self.items):
            # Визначаємо колір тексту
            if cash_manager.get_balance() >= item.price:
                color = (80, 200, 120) if idx == self.selected_index else (200, 200, 200)
            else:
                color = (120, 120, 120)  # Сірий, якщо недостатньо коштів
            
            item_text = self.font.render(f"{item.name} - {item.price} cc", True, color)
            item_rect = item_text.get_rect(center=(self.x + self.width // 2, y_offset))
            surface.blit(item_text, item_rect)
            y_offset += 40

    def handle_mouse_event(self, mouse_pos):
        # Визначаємо, чи клікнули по товару
        y_offset = self.y + 100
        for idx, item in enumerate(self.items):
            # Створюємо область кліку по центру для кожного товару
            item_text = self.font.render(f"{item.name} - {item.price} cc", True, (255, 255, 255))
            item_rect = item_text.get_rect(center=(self.x + self.width // 2, y_offset))
            
            if item_rect.collidepoint(mouse_pos):
                self.selected_index = idx
                return idx
            y_offset += 40
        self.selected_index = None
        return None

    def buy_selected(self):
        # Спроба купити вибраний товар
        if self.selected_index is not None:
            item = self.items[self.selected_index]
            if cash_manager.spend_catcoins(item.price):
                print(f"Куплено: {item.name} за {item.price} catcoin!")
                return item  # Покупка успішна
            else:
                print(f"Недостатньо коштів! Потрібно {item.price} catcoin, а у вас {cash_manager.get_balance()}")
        return None
