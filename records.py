import json
import os
from datetime import datetime

class RecordsManager:
    """Клас для управління рекордами гри"""
    
    def __init__(self, records_file="records.json"):
        self.records_file = records_file
        self.records = self.load_records()
    
    def load_records(self):
        """Завантажує рекорди з файлу"""
        try:
            if os.path.exists(self.records_file):
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Створюємо порожній список рекордів
                return []
        except (json.JSONDecodeError, FileNotFoundError):
            print("Помилка при завантаженні рекордів. Створюємо новий файл.")
            return []
    
    def save_records(self):
        """Зберігає рекорди у файл"""
        try:
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
            print(f"Рекорди збережено у файл {self.records_file}")
        except Exception as e:
            print(f"Помилка при збереженні рекордів: {e}")
    
    def add_record(self, score, player_name="Гравець"):
        """Додає новий рекорд"""
        new_record = {
            "score": score,
            "player": player_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.records.append(new_record)
        
        # Сортуємо рекорди за очками (від найбільшого до найменшого)
        self.records.sort(key=lambda x: x["score"], reverse=True)
        
        # Залишаємо тільки топ-10 рекордів
        self.records = self.records[:10]
        
        # Зберігаємо рекорди
        self.save_records()
        
        # Перевіряємо, чи це новий рекорд
        return self.is_new_record(score)
    
    def is_new_record(self, score):
        """Перевіряє, чи є результат новим рекордом"""
        if not self.records:
            return True  # Перший рекорд
        
        # Перевіряємо, чи потрапляє у топ-10
        if len(self.records) < 10:
            return True
        
        # Перевіряємо, чи більше за найменший рекорд у топ-10
        return score > self.records[-1]["score"]
    
    def get_best_score(self):
        """Повертає найкращий результат"""
        if self.records:
            return self.records[0]["score"]
        return 0
    
    def get_top_records(self, count=10):
        """Повертає топ рекордів"""
        return self.records[:count]
    
    def get_player_position(self, score):
        """Повертає позицію гравця в таблиці рекордів"""
        position = 1
        for record in self.records:
            if score > record["score"]:
                return position
            position += 1
        
        # Якщо не потрапив у топ-10, але рекордів менше 10
        if len(self.records) < 10:
            return len(self.records) + 1
        
        return None  # Не потрапив у топ-10

    def clear_records(self):
        """Очищує всі рекорди (для налагодження)"""
        self.records = []
        self.save_records()
        print("Всі рекорди очищено!")

# Створюємо глобальний екземпляр менеджера рекордів
records_manager = RecordsManager()
