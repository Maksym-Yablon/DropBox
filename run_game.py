#!/usr/bin/env python3
"""
Швидкий запуск гри DropBox
Цей скрипт автоматично запускає гру з перевірками
"""

import sys
import os
import traceback

def check_dependencies():
    """Перевірка необхідних залежностей"""
    try:
        import pygame
        print(f"✓ Pygame version: {pygame.version.ver}")
        return True
    except ImportError:
        print("✗ Pygame не встановлено!")
        print("Для встановлення виконайте: pip install pygame")
        return False

def main():
    """Головна функція запуску"""
    print("=" * 50)
    print("      ЗАПУСК ГРИ DROPBOX")
    print("=" * 50)
    
    # Перевірка залежностей
    if not check_dependencies():
        return False
    
    # Додавання поточної директорії в шлях
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        # Імпорт та запуск гри
        print("Запуск гри...")
        from main import main as game_main
        game_main()
        
    except KeyboardInterrupt:
        print("\nГру зупинено користувачем")
        return True
        
    except Exception as e:
        print(f"\n✗ Помилка при запуску гри:")
        print(f"   {e}")
        print(f"\nДеталі помилки:")
        traceback.print_exc()
        return False
    
    print("Гру завершено успішно")
    return True

if __name__ == "__main__":
    success = main()
    
    # Пауза перед закриттям (для Windows)
    if not success:
        input("\nНатисніть Enter для виходу...")
    
    sys.exit(0 if success else 1)
