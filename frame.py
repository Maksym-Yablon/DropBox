import pygame
from constants import *

class FrameManager:
    """Клас для управління рамками ігрового поля залежно від очків гравця"""
    
    def __init__(self):
        self.current_frame = None
        self.frame_levels = {
            0: "assets/sprites/ui/frame_wood.png",      # Дерев'яна рамка (початкова)
            1000: "assets/sprites/ui/frame_wood.png",   # Тимчасово використовуємо ту ж рамку для тестування
            # В майбутньому можна додати більше рівнів:
            # 5000: "assets/sprites/ui/frame_silver.png", # Срібна рамка (5000+ очків)
            # 10000: "assets/sprites/ui/frame_gold.png",  # Золота рамка (10000+ очків)
        }
        self.loaded_frames = {}
        self.current_score = 0
        
        # Завантажуємо всі доступні рамки
        self._load_frames()
        
        # Встановлюємо початкову рамку
        self.update_frame(0)
    
    def _load_frames(self):
        """Завантажує всі рамки з файлів"""
        for score_threshold, frame_path in self.frame_levels.items():
            try:
                frame_image = pygame.image.load(frame_path)
                self.loaded_frames[score_threshold] = frame_image
                print(f"Рамка завантажена: {frame_path}")
            except pygame.error as e:
                print(f"Помилка завантаження рамки {frame_path}: {e}")
                # Якщо рамка не завантажилася, створюємо заглушку
                if score_threshold == 0:  # Для початкової рамки створюємо просту заглушку
                    placeholder = pygame.Surface((GRID_SIZE * GRID_CELL_SIZE + 40, GRID_SIZE * GRID_CELL_SIZE + 40), pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (139, 69, 19), placeholder.get_rect(), 5)
                    self.loaded_frames[score_threshold] = placeholder
    
    def get_frame_for_score(self, score):
        """Повертає найвищий доступний рівень рамки для поточного рахунку"""
        best_threshold = 0
        for threshold in sorted(self.frame_levels.keys(), reverse=True):
            if score >= threshold and threshold in self.loaded_frames:
                best_threshold = threshold
                break
        return best_threshold
    
    def update_frame(self, score):
        """Оновлює рамку залежно від рахунку"""
        new_frame_level = self.get_frame_for_score(score)
        
        # Перевіряємо, чи потрібно змінювати рамку
        if score != self.current_score:
            old_frame_level = self.get_frame_for_score(self.current_score)
            
            if new_frame_level != old_frame_level:
                self.current_frame = self.loaded_frames[new_frame_level]
                frame_name = self.frame_levels[new_frame_level].split('/')[-1]
                print(f"🎉 СЮРПРИЗ! Рамка оновлена на {frame_name}! 🎉")
                return True  # Рамка змінилася
            
            self.current_score = score
        
        # Встановлюємо поточну рамку, якщо вона ще не встановлена
        if self.current_frame is None:
            self.current_frame = self.loaded_frames[new_frame_level]
        
        return False  # Рамка не змінилася
    
    def draw(self, screen):
        """Малює поточну рамку на екрані"""
        if self.current_frame is None:
            return
        
        # Розраховуємо позицію для центрування рамки над сіткою
        frame_x = GRID_X - (self.current_frame.get_width() - (GRID_SIZE * GRID_CELL_SIZE)) // 2
        frame_y = GRID_Y - (self.current_frame.get_height() - (GRID_SIZE * GRID_CELL_SIZE)) // 1.4

        screen.blit(self.current_frame, (frame_x, frame_y))
    
    def get_current_frame_info(self):
        """Повертає інформацію про поточну рамку"""
        current_level = self.get_frame_for_score(self.current_score)
        frame_name = self.frame_levels[current_level].split('/')[-1]
        
        # Знаходимо наступний рівень
        next_levels = [level for level in sorted(self.frame_levels.keys()) if level > current_level]
        next_level = next_levels[0] if next_levels else None
        
        return {
            'current_level': current_level,
            'current_name': frame_name,
            'next_level': next_level,
            'score': self.current_score
        }
    
    def get_next_frame_requirement(self):
        """Повертає очки, необхідні для наступної рамки"""
        current_level = self.get_frame_for_score(self.current_score)
        next_levels = [level for level in sorted(self.frame_levels.keys()) if level > current_level]
        
        if next_levels:
            return next_levels[0] - self.current_score
        return None  # Максимальна рамка досягнута
