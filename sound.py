# Система звуків для гри
import pygame
import os

class SoundManager:
    """Менеджер для управління всіма звуками в грі"""
    
    def __init__(self):
        # Ініціалізуємо звуковий міксер
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Словник для зберігання звукових ефектів
        self.sounds = {}
        
        # Словник для музики
        self.music = {}
        
        # Налаштування гучності
        self.sfx_volume = 0.7  # Гучність звукових ефектів (0.0 - 1.0)
        self.music_volume = 0.1  # Гучність музики (0.0 - 1.0)
        
        # Стан звуку
        self.sound_enabled = True
        self.music_enabled = True
        
        # Оптимізація: кешування і обмеження частоти звуків
        self._sound_cooldowns = {}  # Час останнього відтворення для кожного звуку
        self._min_sound_interval = 0.1  # Мінімальний інтервал між однаковими звуками (100ms)
        
        # Завантажуємо звуки
        self.load_sounds()
        
        # Автоматично запускаємо фонову музику після завантаження
        self.start_background_music()
    
    def load_sounds(self):
        """Завантажує всі звукові файли"""
        try:
            # Завантажуємо звук комбо x2
            combo_path = "assets/sounds/effects/kombo 1.mp3"
            if os.path.exists(combo_path):
                self.sounds['combo'] = pygame.mixer.Sound(combo_path)
                self.sounds['combo'].set_volume(self.sfx_volume)
                print(f"Звук комбо x2 завантажено: {combo_path}")
            else:
                print(f"Файл звуку не знайдено: {combo_path}")
            
            # Завантажуємо звук комбо x3
            combo2_path = "assets/sounds/effects/kombo_2.mp3"
            if os.path.exists(combo2_path):
                self.sounds['combo2'] = pygame.mixer.Sound(combo2_path)
                self.sounds['combo2'].set_volume(self.sfx_volume)
                print(f"Звук комбо x3 завантажено: {combo2_path}")
            else:
                print(f"Файл звуку не знайдено: {combo2_path}")
            
            # Завантажуємо звук нової гри
            new_game_path = "assets/sounds/effects/new_game.mp3"
            if os.path.exists(new_game_path):
                self.sounds['new_game'] = pygame.mixer.Sound(new_game_path)
                self.sounds['new_game'].set_volume(self.sfx_volume)
                print(f"Звук нової гри завантажено: {new_game_path}")
            else:
                print(f"Файл звуку не знайдено: {new_game_path}")
            
            # Завантажуємо звук розміщення фігури
            pick_path = "assets/sounds/effects/pick.mp3"
            if os.path.exists(pick_path):
                self.sounds['pick'] = pygame.mixer.Sound(pick_path)
                self.sounds['pick'].set_volume(self.sfx_volume)
                print(f"Звук розміщення фігури завантажено: {pick_path}")
            else:
                print(f"Файл звуку не знайдено: {pick_path}")
                
            # Завантажуємо звук гейм овер
            game_over_path = "assets/sounds/effects/game_ower.mp3"
            if os.path.exists(game_over_path):
                self.sounds['game_over'] = pygame.mixer.Sound(game_over_path)
                self.sounds['game_over'].set_volume(self.sfx_volume)
                print(f"Звук гейм овер завантажено: {game_over_path}")
            else:
                print(f"Файл звуку не знайдено: {game_over_path}")
            
            # Завантажуємо основну фонову музику
            background_music_path = "assets/sounds/music/back_musik.mp3"
            if os.path.exists(background_music_path):
                self.background_music_path = background_music_path
                print(f"Основна фонова музика знайдена: {background_music_path}")
            else:
                print(f"Файл основної фонової музики не знайдено: {background_music_path}")
                self.background_music_path = None
            
            
        except pygame.error as e:
            print(f"Помилка завантаження звуків: {e}")
    
    def _can_play_sound(self, sound_name):
        """Перевіряє, чи можна відтворити звук (обмеження частоти)"""
        import time
        current_time = time.time()
        
        if sound_name in self._sound_cooldowns:
            if current_time - self._sound_cooldowns[sound_name] < self._min_sound_interval:
                return False
        
        self._sound_cooldowns[sound_name] = current_time
        return True
    
    def play_combo_sound(self, combo_level=2):
        """Відтворює звук комбо залежно від рівня"""
        if not self.sound_enabled or self.sfx_volume == 0:
            return
        
        sound_name = 'combo' if combo_level == 2 else 'combo2'
        if not self._can_play_sound(sound_name):
            return
            
        if combo_level == 2 and 'combo' in self.sounds:
            try:
                self.sounds['combo'].play()
                print("Відтворюється звук комбо x2!")
            except pygame.error as e:
                print(f"Помилка відтворення звуку комбо x2: {e}")
        elif combo_level >= 3 and 'combo2' in self.sounds:
            try:
                self.sounds['combo2'].play()
                print(f"Відтворюється звук комбо x{combo_level}!")
            except pygame.error as e:
                print(f"Помилка відтворення звуку комбо x{combo_level}: {e}")
    
    def play_new_game_sound(self):
        """Відтворює звук нової гри"""
        if (self.sound_enabled and self.sfx_volume > 0 and 'new_game' in self.sounds and 
            self._can_play_sound('new_game')):
            try:
                self.sounds['new_game'].play()
                print("Відтворюється звук нової гри!")
            except pygame.error as e:
                print(f"Помилка відтворення звуку нової гри: {e}")
    
    def play_pick_sound(self):
        """Відтворює звук розміщення фігури"""
        if (self.sound_enabled and self.sfx_volume > 0 and 'pick' in self.sounds and 
            self._can_play_sound('pick')):
            try:
                self.sounds['pick'].play()
                print("Відтворюється звук розміщення фігури!")
            except pygame.error as e:
                print(f"Помилка відтворення звуку розміщення фігури: {e}")
    
    def play_game_over_sound(self):
        """Відтворює звук гейм овер"""
        if (self.sound_enabled and self.sfx_volume > 0 and 'game_over' in self.sounds and 
            self._can_play_sound('game_over')):
            try:
                self.sounds['game_over'].play()
                print("Відтворюється звук гейм овер!")
            except pygame.error as e:
                print(f"Помилка відтворення звуку гейм овер: {e}")

    def play_rotate_sound(self):
        """Відтворює звук обертання фігури (використовує звук pick)"""
        if (self.sound_enabled and self.sfx_volume > 0 and 'pick' in self.sounds and 
            self._can_play_sound('rotate')):
            try:
                self.sounds['pick'].play()
                print("Відтворюється звук обертання!")
            except pygame.error as e:
                print(f"Помилка відтворення звуку обертання: {e}")

    def play_clear_cells_sound(self):
        """Відтворює звук очищення комірок (використовує звук комбо)"""
        if self.sound_enabled and self.sfx_volume > 0 and 'combo' in self.sounds:
            try:
                self.sounds['combo'].play()
                print("Відтворюється звук очищення комірок!")
            except pygame.error as e:
                print(f"Помилка відтворення звуку очищення комірок: {e}")
    
    def start_background_music(self):
        """Запускає фонову музику"""
        if not self.music_enabled or self.music_volume == 0:
            return
        
        if self.background_music_path:
            try:
                pygame.mixer.music.load(self.background_music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # -1 означає нескінченне повторення
                print("Фонова музика запущена!")
            except pygame.error as e:
                print(f"Помилка запуску фонової музики: {e}")
        
    
    def stop_background_music(self):
        """Зупиняє фонову музику"""
        try:
            pygame.mixer.music.stop()
            print("Фонова музика зупинена!")
        except pygame.error as e:
            print(f"Помилка зупинки фонової музики: {e}")
    
    def play_sound(self, sound_name):
        """Відтворює звук за назвою"""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
                print(f"Відтворюється звук: {sound_name}")
            except pygame.error as e:
                print(f"Помилка відтворення звуку {sound_name}: {e}")
    
    def set_sfx_volume(self, volume):
        """Встановлює гучність звукових ефектів (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        
        # Оновлюємо гучність звукових ефектів
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
        
        # Автоматично вмикаємо/вимикаємо звуки
        if self.sfx_volume == 0:
            self.sound_enabled = False
        elif not self.sound_enabled and self.sfx_volume > 0:
            self.sound_enabled = True
    
    def set_music_volume(self, volume):
        """Встановлює гучність музики (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        
        # Оновлюємо гучність основної музики
        pygame.mixer.music.set_volume(self.music_volume)
        
        # Автоматично вмикаємо/вимикаємо музику
        if self.music_volume == 0:
            self.music_enabled = False
            self.stop_background_music()
        elif not self.music_enabled and self.music_volume > 0:
            self.music_enabled = True
            self.start_background_music()
    
    def toggle_sound(self):
        """Перемикає увімкнення/вимкнення звуків"""
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            pygame.mixer.stop()  # Зупиняємо всі звуки
    
    def toggle_music(self):
        """Перемикає увімкнення/вимкнення музики"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            # Тут можна додати логіку відновлення музики
            pass
        else:
            pygame.mixer.music.stop()
    
    def stop_all_sounds(self):
        """Зупиняє всі звуки"""
        pygame.mixer.stop()
    
    def is_sound_enabled(self):
        """Повертає стан звуків"""
        return self.sound_enabled
    
    def is_music_enabled(self):
        """Повертає стан музики"""
        return self.music_enabled

# Створюємо глобальний екземпляр менеджера звуків
sound_manager = SoundManager()
