import json
import os
from datetime import datetime
from cash import cash_manager

class GameSaveManager:
    """Клас для збереження та завантаження прогресу гри"""
    
    def __init__(self, save_file="game_save.json"):
        self.save_file = save_file
        self.default_save = {
            "has_save": False,
            "score": 0,
            "grid_cells": None,
            "pieces_in_box": None,
            "save_date": None
        }
    
    def save_game(self, grid, piece_box):
        """Зберігає поточний стан гри"""
        try:
            # Підготовуємо дані сітки (конвертуємо кольори в рядки для JSON)
            grid_data = []
            for row in grid.cells:
                grid_row = []
                for cell in row:
                    if cell is None:
                        grid_row.append(None)
                    else:
                        # Зберігаємо колір як список [R, G, B]
                        grid_row.append(list(cell))
                grid_data.append(grid_row)
            
            # Підготовуємо дані фігур в коробці
            pieces_data = []
            for piece in piece_box.pieces:
                piece_data = {
                    "shape": piece.shape,
                    "color": list(piece.color)  # Конвертуємо колір в список
                }
                pieces_data.append(piece_data)
            
            save_data = {
                "has_save": True,
                "score": grid.score,
                "catcoins": cash_manager.get_balance(),  # Зберігаємо баланс catcoin
                "grid_cells": grid_data,
                "pieces_in_box": pieces_data,
                "save_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print(f"Гру збережено! Очки: {grid.score}")
            return True
            
        except Exception as e:
            print(f"Помилка збереження гри: {e}")
            return False
    
    def load_game(self):
        """Завантажує збережений стан гри"""
        try:
            if not os.path.exists(self.save_file):
                return None
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            if not save_data.get("has_save", False):
                return None
            
            # Конвертуємо дані сітки назад в кольори
            grid_cells = []
            for row in save_data["grid_cells"]:
                grid_row = []
                for cell in row:
                    if cell is None:
                        grid_row.append(None)
                    else:
                        # Конвертуємо список назад в tuple
                        grid_row.append(tuple(cell))
                grid_cells.append(grid_row)
            
            # Конвертуємо дані фігур
            pieces_data = []
            for piece_data in save_data["pieces_in_box"]:
                pieces_data.append({
                    "shape": piece_data["shape"],
                    "color": tuple(piece_data["color"])  # Конвертуємо в tuple
                })
            
            loaded_data = {
                "score": save_data["score"],
                "catcoins": save_data.get("catcoins", 0),  # Завантажуємо catcoin (0 за замовчуванням)
                "grid_cells": grid_cells,
                "pieces_in_box": pieces_data,
                "save_date": save_data["save_date"]
            }
            
            print(f"Гру завантажено! Очки: {save_data['score']}, збережено: {save_data['save_date']}")
            return loaded_data
            
        except Exception as e:
            print(f"Помилка завантаження гри: {e}")
            return None
    
    def has_saved_game(self):
        """Перевіряє, чи є збережена гра"""
        try:
            if not os.path.exists(self.save_file):
                return False
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            return save_data.get("has_save", False)
            
        except Exception:
            return False
    
    def delete_save(self):
        """Видаляє збережену гру"""
        try:
            if os.path.exists(self.save_file):
                # Замість видалення файлу, просто позначаємо що збереження немає
                save_data = self.default_save.copy()
                with open(self.save_file, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                print("Збережену гру видалено")
                return True
        except Exception as e:
            print(f"Помилка видалення збереження: {e}")
        return False
    
    def get_save_info(self):
        """Повертає інформацію про збережену гру"""
        try:
            if not os.path.exists(self.save_file):
                return None
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            if not save_data.get("has_save", False):
                return None
                
            return {
                "score": save_data["score"],
                "save_date": save_data["save_date"]
            }
            
        except Exception:
            return None

# Створюємо глобальний екземпляр менеджера збережень
game_save_manager = GameSaveManager()
