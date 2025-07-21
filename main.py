from builtins import range
import pygame
import random
import os
from sys import exit

# Імпорт модулів гри
from constants import *
import grid as grid_module
from piece import PieceBox, Piece
import ui
from ui import ui_effects, GameOverScreen, GameUI, MenuSystem, PauseButton, PauseMenu, SettingsMenu, CustomCursor
from records import records_manager
from save_manager import game_save_manager
from cash import cash_manager
from shop import Shop
from sound import sound_manager
from frame import FrameManager

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Drop Box")
pygame.display.set_icon(pygame.image.load(UI_ICON_PATH))

# Створюємо об'єкти UI
grid = grid_module.Grid()  # Ігрове поле
game_over_screen = GameOverScreen(screen, clock)
game_ui = GameUI(screen)
menu_system = MenuSystem(screen, clock)
pause_button = PauseButton()
pause_menu = PauseMenu()
settings_menu = SettingsMenu(screen, clock)
frame_manager = FrameManager()  # Менеджер рамок

# Ініціалізуємо глобальний курсор
import ui
ui.global_cursor = CustomCursor()
custom_cursor = ui.global_cursor  # Локальна змінна для зручності


# Основний цикл гри (запускається після натискання "Грати")
running = True
dragging = False
dragged_piece = None
dragged_piece_index = None  # Індекс фігури в коробці
drag_offset_x = 0  # Зміщення кліку по X відносно фігури
drag_offset_y = 0  # Зміщення кліку по Y відносно фігури
drag_block_col = 0  # Колонка блоку в фігурі, за яку взялися
drag_block_row = 0  # Рядок блоку в фігурі, за яку взялися
waiting_for_rotate_click = False  # Режим вибору фігури для обертання

# Кешовані значення для оптимізації
CACHED_GRID_HEIGHT = GRID_SIZE * GRID_CELL_SIZE
CACHED_CONTAINER_CENTER_Y = GRID_Y + (CACHED_GRID_HEIGHT - PIECE_CONTAINER_HEIGHT) // 2
CACHED_SCALE_FACTOR = PIECE_CELL_SIZE / PIECE_CONTAINER_CELL_SIZE

# Оптимізація обчислень
game_over_check_counter = 0
GAME_OVER_CHECK_INTERVAL = 60  # Збільшено до 1 секунди замість пів секунди
# Видаляємо hover_update для плавності курсора - обробляємо ховер прямо в циклі

# Додаємо змінні для розрахунку FPS
fps_counter = 0
current_fps = 0
FPS_UPDATE_INTERVAL = 30  # Оновлюємо FPS кожні 30 кадрів для стабільності

# Ініціалізуємо магазин (зліва від ігрового поля, вирівнюється з блоком фігур)
shop_font = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, UI_FONT_SHOP_TITLE)  # Використовуємо константи
shop_x = 50
shop_y = CACHED_CONTAINER_CENTER_Y  # Використовуємо ту ж вертикальну позицію що й блок фігур
shop_width = PIECE_CONTAINER_WIDTH
shop_height = PIECE_CONTAINER_HEIGHT
shop = Shop(shop_x, shop_y, shop_width, shop_height, shop_font)


def get_background_image():
    """Повертає фонове зображення для меню"""
    try:
        return pygame.image.load("image/icon.png")
    except pygame.error:
        # Якщо не вдалося завантажити зображення, створюємо просту поверхню
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill(BACKGROUND_COLOR)
        return bg

def create_piece_container(x_position):
    """Створює контейнер для фігур з кешованими значеннями (оптимізація)"""
    return PieceBox(x_position, CACHED_CONTAINER_CENTER_Y)

def get_piece_at_mouse(mouse_pos):
    """Перевіряє, чи клікнули на фігуру в коробці"""
    return piece_box.get_piece_at_mouse(mouse_pos[0], mouse_pos[1])

def save_current_game():
    """Зберігає поточний стан гри"""
    return game_save_manager.save_game(grid, piece_box)

def load_saved_game():
    """Завантажує збережену гру"""
    global grid, piece_box
    
    saved_data = game_save_manager.load_game()
    if saved_data is None:
        print("Немає збереженої гри для завантаження")
        return False
    
    try:
        # Відновлюємо стан сітки
        grid.score = saved_data["score"]
        grid.cells = saved_data["grid_cells"]
        
        # Відновлюємо баланс catcoin
        cash_manager.set_balance(saved_data.get("catcoins", 0))
        
        # Відновлюємо фігури в коробці
        piece_box = create_piece_container(1000)
        piece_box.pieces = []
        
        for piece_data in saved_data["pieces_in_box"]:
            piece = Piece(piece_data["shape"], piece_data["color"])
            piece_box.pieces.append(piece)
        
        print(f"Гру завантажено! Очки: {saved_data['score']}")
        return True
        
    except Exception as e:
        print(f"Помилка завантаження гри: {e}")
        return False


# Створюємо коробку для фігур (центрована по висоті ігрового поля)
piece_box = create_piece_container(1000)

def show_game_over_screen():
    """Показує екран завершення гри з результатами"""
    return game_over_screen.show(grid.score, records_manager)

def game_over():
    """Обробляє завершення гри та збереження рекорду"""
    final_score = grid.score
    
    # Відтворюємо звук гейм овер
    sound_manager.play_game_over_sound()
    
    # Додаємо рекорд
    is_new_record = records_manager.add_record(final_score)
    
    # Повідомляємо гравця
    if is_new_record:
        print(f"НОВИЙ РЕКОРД! Очки: {final_score}")
        position = records_manager.get_player_position(final_score)
        if position:
            print(f"Ваша позиція: {position} місце")
    else:
        print(f"Гра завершена! Очки: {final_score}")
        best_score = records_manager.get_best_score()
        print(f"Найкращий результат: {best_score}")
    
    # Показуємо топ-5 рекордів
    print("\n🏆 ТОП-5 РЕКОРДІВ:")
    top_records = records_manager.get_top_records(5)
    for i, record in enumerate(top_records, 1):
        print(f"{i}. {record['score']} очок - {record['player']} ({record['date']})")

def check_game_over():
    """Перевіряє, чи можна розмістити хоча б одну фігуру (оптимізована версія)"""
    # Оптимізація: перевіряємо спочатку кутові позиції як найбільш ймовірні
    priority_positions = [(0,0), (0,7), (7,0), (7,7), (3,3), (3,4), (4,3), (4,4)]
    
    for piece in piece_box.pieces:
        # Спочатку перевіряємо пріоритетні позиції
        for row, col in priority_positions:
            if grid.can_place_piece(piece, col, row):
                return False
                
        # Якщо в пріоритетних місцях не підходить, перевіряємо всі інші
        for row in range(8):
            for col in range(8):
                if (row, col) not in priority_positions:
                    if grid.can_place_piece(piece, col, row):
                        return False
    return True

def reset_game():
    """Скидає гру до початкового стану"""
    global grid, piece_box, dragging, dragged_piece, dragged_piece_index, drag_offset_x, drag_offset_y, drag_block_col, drag_block_row, game_over_check_counter, waiting_for_rotate_click, fps_counter, current_fps
    
    # Відтворюємо звук нової гри
    sound_manager.play_new_game_sound()
    
    # Створюємо нову сітку
    grid = grid_module.Grid()
    
    # Створюємо нову коробку з фігурами (використовуємо кешовані значення)
    piece_box = create_piece_container(1000)
    
    # Скидаємо баланс catcoin
    cash_manager.set_balance(0)
    
    # Скидаємо стан перетягування
    dragging = False
    dragged_piece = None
    dragged_piece_index = None
    drag_offset_x = 0
    drag_offset_y = 0
    drag_block_col = 0
    drag_block_row = 0
    game_over_check_counter = 0
    waiting_for_rotate_click = False

# Показуємо заставку та меню
menu_result = menu_system.main_menu_loop(records_manager, get_background_image(), game_save_manager)

# Перевіряємо результат меню
if menu_result == 'continue':
    # Завантажуємо збережену гру
    if not load_saved_game():
        # Якщо завантаження не вдалося, створюємо нову гру
        reset_game()
elif menu_result == 'new_game':
    # Видаляємо старе збереження та починаємо нову гру
    game_save_manager.delete_save()
    reset_game()
else:
    # За замовчуванням створюємо нову гру
    reset_game()

while running:
    # Кешуємо позицію миші один раз на початку кадру для оптимізації
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = (mouse_x, mouse_y)
    
    # Оновлюємо ховер ефекти без додаткових лічильників для максимальної плавності
    if pause_menu.is_paused:
        pause_menu.handle_mouse_motion(mouse_pos)
    else:
        pause_button.handle_mouse_motion(mouse_pos)
    
    for event in pygame.event.get():
        # Обробляємо події для кастомного курсора
        custom_cursor.handle_mouse_event(event)
        
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu.toggle_pause()
            elif event.key == pygame.K_r and pygame.key.get_pressed()[pygame.K_LCTRL]:
                reset_game()
            # Тимчасова функція для нарахування catcoin (клавіша C)
            elif event.key == pygame.K_c:
                cash_manager.catcoins += 1000
                sound_manager.play_pick_sound()  # Звуковий ефект
                print(f"💰 Додано 1000 catcoin! Поточний баланс: {cash_manager.get_balance()}")
            # Команди для налагодження (тільки якщо гра не на паузі)
            elif not pause_menu.is_paused:
                if event.key == pygame.K_r:  # R - скидання сітки
                    for row in range(8):
                        for col in range(8):
                            grid.cells[row][col] = None
                    grid.score = 0
                elif event.key == pygame.K_n:  # N - Нова гра
                    reset_game()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Перевіряємо, що натиснута саме ліва кнопка миші (event.button == 1)
            if event.button != 1:  # 1 = ліва кнопка, 2 = колесо, 3 = права кнопка
                continue  # Ігноруємо всі інші кнопки миші
                
            # Якщо гра на паузі, передаємо клік до меню паузи
            if pause_menu.is_paused:
                pause_action = pause_menu.handle_click(mouse_pos)
                if pause_action:
                    if pause_action == 'resume':
                        pause_menu.toggle_pause()
                    elif pause_action == 'restart':
                        pause_menu.toggle_pause()  # Вимикаємо паузу
                        reset_game()
                    elif pause_action == 'settings':
                        result = settings_menu.show_settings_screen()
                        if result == "quit":
                            running = False
                    elif pause_action == 'help':
                        # TODO: Додати екран допомоги
                        print("Перетягніть фігури на сітку щоб заповнити лінії!")
                    elif pause_action == 'menu':
                        # Повернення до головного меню - зберігаємо гру
                        save_current_game()
                        pause_menu.toggle_pause()  # Вимикаємо паузу
                        menu_result = menu_system.main_menu_loop(records_manager, get_background_image(), game_save_manager)
                        
                        # Обробляємо результат меню
                        if menu_result == 'continue':
                            if not load_saved_game():
                                reset_game()
                        elif menu_result == 'new_game':
                            game_save_manager.delete_save()
                            reset_game()
                        else:
                            reset_game()
                continue  # Не обробляємо інші кліки, якщо гра на паузі
            
            # Перевіряємо клік по кнопці паузи (якщо гра не на паузі)
            if pause_button.handle_click(mouse_pos):
                pause_menu.toggle_pause()
                continue  # Пропускаємо обробку перетягування фігур
            
            # Перевіряємо клік по магазину (якщо гра не на паузі)
            if not pause_menu.is_paused:
                shop_result = shop.handle_click(mouse_pos[0], mouse_pos[1], cash_manager, piece_box)
                if shop_result:
                    if shop_result == "rotate_purchased":
                        print("Куплено: Обернути фігуру! Клікніть на фігуру для обертання.")
                        # Відтворюємо звук покупки в магазині
                        sound_manager.play_shop_sound()
                        # Активуємо режим вибору фігури для обертання
                        waiting_for_rotate_click = True
                    elif shop_result == "clear_cells_purchased":
                        # Виконуємо очищення комірок відразу
                        cleared_count = grid.clear_random_cells(5)
                        print(f"Куплено: Очистити 5 комірок! Очищено {cleared_count} комірок.")
                        # Відтворюємо звук покупки в магазині
                        sound_manager.play_shop_sound()
                    elif shop_result == "insufficient_funds":
                        print("Недостатньо коштів!")
                    continue  # Пропускаємо обробку перетягування фігур
            
            # Почати перетягування фігур (тільки якщо гра не на паузі)
            if not pause_menu.is_paused:
                # Якщо чекаємо на клік для обертання
                if waiting_for_rotate_click:
                    piece_index, _, _ = piece_box.get_piece_at_mouse(mouse_pos[0], mouse_pos[1])
                    if piece_index is not None:
                        # Повертаємо фігуру
                        if piece_box.rotate_piece(piece_index):
                            print("Фігуру повернуто!")
                            # Відтворюємо звук обертання
                            sound_manager.play_rotate_sound()
                        waiting_for_rotate_click = False
                        continue  # Не починаємо перетягування
                    else:
                        # Клікнули не на фігуру - скасовуємо режим обертання
                        waiting_for_rotate_click = False
                        print("Обертання скасовано")
                
                clicked_piece_index, offset_x, offset_y = get_piece_at_mouse(mouse_pos)
            if clicked_piece_index is not None:
                # Також визначаємо, за який блок фігури взялися
                piece_index, block_col, block_row = piece_box.get_block_position_in_piece(mouse_pos[0], mouse_pos[1])
                
                # Починаємо перетягування
                dragging = True
                dragged_piece = piece_box.pieces[clicked_piece_index]
                dragged_piece_index = clicked_piece_index
                drag_offset_x = offset_x
                drag_offset_y = offset_y
                drag_block_col = block_col if block_col is not None else 0
                drag_block_row = block_row if block_row is not None else 0
                
                # Повідомляємо piece_box про початок перетягування
                piece_box.start_dragging(clicked_piece_index)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            # Перевіряємо, що відпущена саме ліва кнопка миші
            if event.button != 1:  # Ігноруємо всі інші кнопки миші
                continue
                
            # Закінчити перетягування
            if dragging and dragged_piece:
                grid_x, grid_y = grid.mouse_to_grid(mouse_pos[0], mouse_pos[1])
                
                # Корегуємо позицію з урахуванням того, за який блок фігури взялися
                target_grid_x = grid_x - drag_block_col
                target_grid_y = grid_y - drag_block_row
                
                placed = False
                # Перевіряємо, чи можна розмістити фігуру
                if grid.can_place_piece(dragged_piece, target_grid_x, target_grid_y):
                    # Зберігаємо поточний рахунок перед розміщенням
                    old_score = grid.score
                    
                    # Розміщуємо фігуру на сітці
                    grid.place_piece(dragged_piece, target_grid_x, target_grid_y)
                    grid.clear_lines()  # Перевіряємо на очищення ліній
                    
                    # Обчислюємо нарахованих очок та конвертуємо в catcoin
                    score_increase = grid.score - old_score
                    if score_increase > 0:
                        cash_manager.update_from_score(score_increase)
                    
                    placed = True
                else:
                    print("Неможливо розмістити фігуру тут")
                
                # Завершуємо перетягування з результатом (це замінить фігуру якщо placed=True)
                piece_box.stop_dragging(placed)
            dragging = False
            dragged_piece = None
            dragged_piece_index = None
            drag_offset_x = 0
            drag_offset_y = 0
            drag_block_col = 0
            drag_block_row = 0
            
        elif event.type == pygame.MOUSEMOTION:
            # Обробляємо рух миші тільки для перетягування (ховер вже оброблено на початку циклу)
            if dragging and not pause_menu.is_paused:
                # Позиція миші вже кешована на початку кадру
                pass
        
        elif event.type == pygame.MOUSEWHEEL:
            # Ігноруємо прокручування колеса миші
            continue
        
        elif event.type == pygame.KEYDOWN:
            # Команди клавіатури вже оброблено вище
            pass
            
    # код гри (тільки якщо не на паузі)
    screen.fill(BACKGROUND_COLOR)
    grid.draw(screen)  # малюємо ігрове поле
    
    # Оновлюємо та малюємо рамку залежно від рахунку
    frame_manager.update_frame(grid.score)
    frame_manager.draw(screen)

    # Відображаємо HUD (очки та рекорд)
    best_score = records_manager.get_best_score()
    game_ui.draw_hud(grid.score, best_score, frame_manager)

    # Малюємо магазин (тільки якщо гра не на паузі)
    if not pause_menu.is_paused:
        shop.draw(screen)

    # Малюємо кнопку паузи (тільки якщо гра не на паузі)
    if not pause_menu.is_paused:
        pause_button.draw(screen)

    if not pause_menu.is_paused:
        # Підсвічування під час перетягування з новими ефектами
        if dragging and dragged_piece:
            grid_x, grid_y = grid.mouse_to_grid(mouse_pos[0], mouse_pos[1])
            
            # Корегуємо позицію з урахуванням того, за який блок фігури взялися
            target_grid_x = grid_x - drag_block_col
            target_grid_y = grid_y - drag_block_row
            
            # Використовуємо нову систему візуальних ефектів з коригованою позицією
            ui_effects.draw_enhanced_preview(screen, grid, dragged_piece, target_grid_x, target_grid_y)
        else:
            # Зупиняємо мигання, коли не перетягуємо
            ui_effects.stop_blinking()

        # Малюємо просту коробку для фігур
        ui_effects.draw_simple_piece_box(screen, piece_box)
        
        # Малюємо фігури в коробці (крім тої, що перетягується)
        piece_box.draw(screen)

        # Візуальний індикатор режиму обертання
        if waiting_for_rotate_click:
            # Додаємо підсвічування контейнера фігур
            pygame.draw.rect(screen, UI_ROTATION_HIGHLIGHT_COLOR, 
                           (piece_box.start_x - 5, piece_box.start_y - 5, 
                            piece_box.width + 10, piece_box.height + 10), 3)
            
            # Показуємо текст підказки
            font = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, UI_FONT_ROTATION_HINT)
            hint_text = font.render("Оберіть фігуру для обертання", True, UI_ROTATION_HINT_COLOR)
            text_x = piece_box.start_x + (piece_box.width - hint_text.get_width()) // 2
            text_y = piece_box.start_y - 40
            screen.blit(hint_text, (text_x, text_y))

        # Якщо перетягуємо фігуру - малюємо її під мишею з урахуванням зміщення кліку
        if dragging and dragged_piece:
            # Використовуємо кешований scale_factor та позицію миші для оптимізації
            scaled_offset_x = drag_offset_x * CACHED_SCALE_FACTOR
            scaled_offset_y = drag_offset_y * CACHED_SCALE_FACTOR
            
            # Віднімаємо скореговане зміщення кліку
            dragged_piece.draw(screen, mouse_pos[0] - scaled_offset_x, mouse_pos[1] - scaled_offset_y, PIECE_CELL_SIZE)

        # Оптимізована перевірка на кінець гри (не кожен кадр)
        game_over_check_counter += 1
        if game_over_check_counter >= GAME_OVER_CHECK_INTERVAL:
            game_over_check_counter = 0
            if check_game_over():
                # Відтворюємо звук завершення гри
                sound_manager.play_game_over_sound()
                
                result = show_game_over_screen()
                if result == "restart":
                    reset_game()
                elif result == "menu":
                    # Повертаємося до меню - зберігаємо гру перед завершенням
                    save_current_game()
                    menu_result = menu_system.main_menu_loop(records_manager, get_background_image(), game_save_manager)
                    
                    # Обробляємо результат меню
                    if menu_result == 'continue':
                        if not load_saved_game():
                            reset_game()
                    elif menu_result == 'new_game':
                        game_save_manager.delete_save()
                        reset_game()
                    else:
                        reset_game()
                elif result == "quit":
                    running = False
    
    # Малюємо меню паузи поверх всього (якщо активне)
    if pause_menu.is_paused:
        pause_menu.draw(screen)
    
    # Розраховуємо та відображаємо FPS
    if settings_menu.show_fps:
        fps_counter += 1
        if fps_counter >= FPS_UPDATE_INTERVAL:
            current_fps = clock.get_fps()
            fps_counter = 0
        
        # Малюємо FPS лічильник
        game_ui.draw_fps(current_fps, settings_menu.show_fps)
    
    # Малюємо кастомний курсор поверх всього
    custom_cursor.draw(screen, mouse_pos)
    
    pygame.display.flip() # Оновлюємо екран
    clock.tick(60) # FPS в грі

# Зберігаємо гру при виході
save_current_game()

# Очищуємо глобальний курсор при виході
if ui.global_cursor:
    ui.global_cursor.cleanup()

pygame.quit()
exit()