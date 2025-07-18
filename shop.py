# Внутрішньоігровий магазин
import pygame
from cash import cash_manager
from constants import *  # Імпортуємо всі константи

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
            ShopItem("Обернути фігуру", 3, "Повертає обрану фігуру на 90°"),
            ShopItem("Очистити 5 комірок", 5, "Випадково очищає 5 комірок сітки")
        ]

    def draw(self, surface):
        # Малюємо панель магазину в темному стилі
        # Створюємо поверхню з прозорістю для заливки
        shop_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # М'яка темна заливка з прозорістю
        fill_color = UI_SHOP_BACKGROUND_COLOR  # Використовуємо константу
        pygame.draw.rect(shop_surface, fill_color, (0, 0, self.width, self.height), border_radius=10)
        
        # Малюємо заливку на екрані
        surface.blit(shop_surface, (self.x, self.y))
        
        # М'який темний контур
        border_color = UI_SHOP_BORDER_COLOR  # Використовуємо константу
        pygame.draw.rect(surface, border_color, (self.x, self.y, self.width, self.height), width=2, border_radius=10)
        
        # Заголовок магазину по центру контейнера
        title = self.font.render("МАГАЗИН", True, UI_SHOP_TITLE_COLOR)  # Використовуємо константу
        title_rect = title.get_rect(center=(self.x + self.width // 2, self.y + 30))
        surface.blit(title, title_rect)
        
        # Показуємо баланс catcoin по центру контейнера
        balance_text = self.font.render(f"{cash_manager.get_balance()} catcoin", True, UI_SHOP_BALANCE_COLOR)  # Використовуємо константу
        balance_rect = balance_text.get_rect(center=(self.x + self.width // 2, self.y + 60))
        surface.blit(balance_text, balance_rect)
        
        # Малюємо товари
        y_offset = self.y + 100
        for idx, item in enumerate(self.items):
            # Визначаємо колір тексту для темної теми (використовуємо константи)
            if cash_manager.get_balance() >= item.price:
                color = UI_SHOP_ITEM_SELECTED_COLOR if idx == self.selected_index else UI_SHOP_ITEM_AVAILABLE_COLOR
            else:
                color = UI_SHOP_ITEM_UNAVAILABLE_COLOR
            
            item_text = self.font.render(f"{item.name} - {item.price} cc", True, color)
            item_rect = item_text.get_rect(center=(self.x + self.width // 2, y_offset))
            surface.blit(item_text, item_rect)
            y_offset += 40

    def handle_mouse_event(self, mouse_pos):
        # Визначаємо, чи клікнули по товару
        y_offset = self.y + 100
        for idx, item in enumerate(self.items):
            # Створюємо область кліку по центру для кожного товару
            item_text = self.font.render(f"{item.name} - {item.price} cc", True, UI_SHOP_ITEM_AVAILABLE_COLOR)  # Використовуємо константу
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

    def handle_click(self, mouse_x, mouse_y, cash_manager, piece_box=None):
        """Обробляє клік по товару та покупку"""
        y_offset = self.y + 100
        for idx, item in enumerate(self.items):
            # Створюємо область кліку по центру для кожного товару
            item_text = self.font.render(f"{item.name} - {item.price} cc", True, (255, 255, 255))
            item_rect = item_text.get_rect(center=(self.x + self.width // 2, y_offset))
            
            if item_rect.collidepoint((mouse_x, mouse_y)):
                # Спробувати купити товар
                if cash_manager.get_balance() >= item.price:
                    # Обробляємо різні типи товарів
                    if item.name == "Обернути фігуру":
                        # Для обертання потрібен piece_box
                        if piece_box is None:
                            print("Помилка: не передано piece_box для обертання")
                            return "error"
                        cash_manager.spend(item.price)
                        return "rotate_purchased"
                    elif item.name == "Очистити 5 комірок":
                        cash_manager.spend(item.price)
                        return "clear_cells_purchased"
                else:
                    return "insufficient_funds"
            y_offset += 40
        
        return None
