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

# Ініціалізуємо кастомний курсор
custom_cursor = CustomCursor()

# Створюємо об'єкти UI, передаючи курсор
grid = grid_module.Grid()  # Ігрове поле
game_over_screen = GameOverScreen(screen, clock, custom_cursor)
game_ui = GameUI(screen)
menu_system = MenuSystem(screen, clock, custom_cursor)
pause_button = PauseButton()
pause_menu = PauseMenu()
settings_menu = SettingsMenu(screen, clock, custom_cursor)
frame_manager = FrameManager()  # Менеджер рамок

# Глобальні змінні стану гри
running = True
dragging = False
dragged_piece = None
dragged_piece_index = None  # Індекс фігури в коробці
drag_offset_x = 0  # Зміщення кліку по X відносно фігури
drag_offset_y = 0  # Зміщення кліку по Y відносно фігури
drag_block_col = 0  # Колонка блоку в фігурі, за яку взялися
drag_block_row = 0  # Рядок блоку в фігурі, за яку взялися
waiting_for_rotate_click = False  # Режим вибору фігури для обертання

# Кешовані значення для оптимізації (адаптовані під мобільний)
CACHED_GRID_HEIGHT = GRID_SIZE * GRID_CELL_SIZE
CACHED_CONTAINER_CENTER_Y = PIECE_CONTAINER_Y  # Використовуємо нову мобільну позицію
CACHED_SCALE_FACTOR = PIECE_CELL_SIZE / PIECE_CONTAINER_CELL_SIZE

# Оптимізація обчислень
game_over_check_counter = 0
GAME_OVER_CHECK_INTERVAL = 60  # Збільшено до 1 секунди замість пів секунди
# Видаляємо hover_update для плавності курсора - обробляємо ховер прямо в циклі

# Додаємо змінні для розрахунку FPS
fps_counter = 0
current_fps = 0
FPS_UPDATE_INTERVAL = 30  # Оновлюємо FPS кожні 30 кадрів для стабільності

# Ініціалізуємо магазин (адаптований під мобільний формат)
shop_font = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, UI_FONT_SHOP_TITLE)  # Використовуємо константи
shop_x = MOBILE_SIDE_MARGIN  # Позиція з відступом
shop_y = SHOP_CONTAINER_Y  # Нова позиція під контейнером фігур
shop_width = SHOP_CONTAINER_WIDTH  # Ширина на весь екран з відступами
shop_height = SHOP_CONTAINER_HEIGHT  # Нова висота для мобільного
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
    """Створює контейнер для фігур з мобільними координатами"""
    return PieceBox(MOBILE_SIDE_MARGIN, CACHED_CONTAINER_CENTER_Y, PIECE_CONTAINER_WIDTH, PIECE_CONTAINER_HEIGHT)

def draw_mobile_header(surface, score, best_score):
    """Малює мобільний header з кнопками та очками"""
    # Кнопка "Назад" (ліва) - зробимо її більш видимою
    back_button_rect = pygame.Rect(MOBILE_BACK_BUTTON_X, MOBILE_BACK_BUTTON_Y, MOBILE_BUTTON_SIZE, MOBILE_BUTTON_SIZE)
    pygame.draw.rect(surface, MOBILE_BUTTON_COLOR, back_button_rect, border_radius=8)
    pygame.draw.rect(surface, (255, 255, 255), back_button_rect, 2, border_radius=8)  # Біла рамка
    
    # Текст для кнопки назад
    font_button = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, 20)
    back_text = font_button.render("←", True, MOBILE_BUTTON_TEXT_COLOR)
    text_x = MOBILE_BACK_BUTTON_X + (MOBILE_BUTTON_SIZE - back_text.get_width()) // 2
    text_y = MOBILE_BACK_BUTTON_Y + (MOBILE_BUTTON_SIZE - back_text.get_height()) // 2
    surface.blit(back_text, (text_x, text_y))
    
    # Кнопка "Налаштування" (права) - зробимо її більш видимою
    settings_button_rect = pygame.Rect(MOBILE_SETTINGS_BUTTON_X, MOBILE_SETTINGS_BUTTON_Y, MOBILE_BUTTON_SIZE, MOBILE_BUTTON_SIZE)
    pygame.draw.rect(surface, MOBILE_BUTTON_COLOR, settings_button_rect, border_radius=8)
    pygame.draw.rect(surface, (255, 255, 255), settings_button_rect, 2, border_radius=8)  # Біла рамка
    
    # Текст для кнопки налаштувань
    settings_text = font_button.render("⚙", True, MOBILE_BUTTON_TEXT_COLOR)
    text_x = MOBILE_SETTINGS_BUTTON_X + (MOBILE_BUTTON_SIZE - settings_text.get_width()) // 2
    text_y = MOBILE_SETTINGS_BUTTON_Y + (MOBILE_BUTTON_SIZE - settings_text.get_height()) // 2
    surface.blit(settings_text, (text_x, text_y))
    
    # Рекорд (по центру, зверху)
    font_record = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, 28)
    record_text = font_record.render(f"рекорд: {best_score}", True, (255, 200, 0))
    record_x = (SCREEN_WIDTH - record_text.get_width()) // 2
    surface.blit(record_text, (record_x, 25))
    
    # Поточні очки (по центру, нижче рекорду)
    font_score = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, 42)
    score_text = font_score.render(f"Очки: {score}", True, (255, 255, 255))
    score_x = (SCREEN_WIDTH - score_text.get_width()) // 2
    surface.blit(score_text, (score_x, 70))

def draw_mobile_shop(surface):
    """Малює мобільний магазин з кнопками та балансом (адаптивний)"""
    shop_y = SHOP_CONTAINER_Y
    
    # Фон магазину
    shop_rect = pygame.Rect(MOBILE_SIDE_MARGIN, shop_y, SHOP_CONTAINER_WIDTH, SHOP_CONTAINER_HEIGHT)
    pygame.draw.rect(surface, (50, 50, 50), shop_rect, border_radius=10)
    pygame.draw.rect(surface, (100, 100, 100), shop_rect, 2, border_radius=10)  # Рамка
    
    # --- Зона балансу (верхні 35% контейнера) ---
    balance_area_height = SHOP_CONTAINER_HEIGHT * 0.35
    balance = cash_manager.get_cash()
    font_size = int(balance_area_height * 0.7) # Адаптивний розмір шрифту
    font_balance = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, font_size)
    balance_text = font_balance.render(f"💰 {balance} catcoin", True, (255, 215, 0))
    
    # Центруємо текст балансу в його зоні
    balance_x = MOBILE_SIDE_MARGIN + 15
    balance_y = shop_y + (balance_area_height - balance_text.get_height()) // 2
    surface.blit(balance_text, (balance_x, balance_y))
    
    # --- Зона кнопок (нижні 65% контейнера) ---
    buttons_area_y = shop_y + balance_area_height
    buttons_area_height = SHOP_CONTAINER_HEIGHT - balance_area_height
    
    font_size = int(buttons_area_height * 0.25) # Адаптивний шрифт для кнопок
    font_button = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, font_size)
    
    button_width = (SHOP_CONTAINER_WIDTH - 50) // 4  # 4 кнопки, відступи по 10px
    button_height = buttons_area_height * 0.75 # Кнопка займає 75% висоти своєї зони
    
    # Центруємо кнопки по вертикалі в їх зоні
    button_y = buttons_area_y + (buttons_area_height - button_height) // 2
    
    shop_items = [
        ("🔄", "15", MOBILE_SHOP_ROTATE_COLOR, "rotate"),
        ("💥", "25", MOBILE_SHOP_RESET_COLOR, "reset"), 
        ("💎", "0", MOBILE_SHOP_COPY_COLOR, "copy"),
        ("💡", "10", MOBILE_SHOP_HINT_COLOR, "hint")
    ]
    
    for i, (icon, price, color, action) in enumerate(shop_items):
        button_x = MOBILE_SIDE_MARGIN + 10 + i * (button_width + 10)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Перевіряємо чи достатньо коштів
        price_int = int(price) if price != "0" else 0
        can_afford = balance >= price_int
        button_color = color if can_afford else (100, 100, 100)
        
        # Малюємо кнопку
        pygame.draw.rect(surface, button_color, button_rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), button_rect, 2, border_radius=8)
        
        # Іконка (адаптивна позиція)
        icon_text = font_button.render(icon, True, (255, 255, 255))
        icon_x = button_x + (button_width - icon_text.get_width()) // 2
        icon_y = button_y + button_height * 0.15 # Розміщуємо іконку трохи зверху
        surface.blit(icon_text, (icon_x, icon_y))
        
        # Ціна (адаптивна позиція)
        price_color = (255, 255, 255) if can_afford else (150, 150, 150)
        price_text = font_button.render(price, True, price_color)
        price_x = button_x + (button_width - price_text.get_width()) // 2
        price_y = button_y + button_height - font_size - button_height * 0.1
        surface.blit(price_text, (price_x, price_y))

def draw_mobile_ad_space(surface):
    """Малює рекламний блок"""
    if AD_CONTAINER_VISIBLE:
        ad_rect = pygame.Rect(MOBILE_SIDE_MARGIN, AD_CONTAINER_Y, AD_CONTAINER_WIDTH, AD_CONTAINER_HEIGHT)
        pygame.draw.rect(surface, (30, 30, 30), ad_rect, border_radius=10)
        pygame.draw.rect(surface, (80, 80, 80), ad_rect, 2, border_radius=10)  # Рамка
        
        # Текст-заглушка для реклами
        font = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, min(18, AD_CONTAINER_HEIGHT // 4))
        ad_text = font.render("📱 Місце для реклами", True, (100, 100, 100))
        text_x = MOBILE_SIDE_MARGIN + (AD_CONTAINER_WIDTH - ad_text.get_width()) // 2
        text_y = AD_CONTAINER_Y + (AD_CONTAINER_HEIGHT - ad_text.get_height()) // 2
        surface.blit(ad_text, (text_x, text_y))

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
        piece_box = create_piece_container(MOBILE_SIDE_MARGIN)
        piece_box.pieces = []
        
        for piece_data in saved_data["pieces_in_box"]:
            piece = Piece(piece_data["shape"], piece_data["color"])
            piece_box.pieces.append(piece)
        
        # ВАЖЛИВО: Перераховуємо позиції фігур після завантаження
        piece_box._calculate_piece_positions()
        
        print(f"Гру завантажено! Очки: {saved_data['score']}")
        return True
        
    except Exception as e:
        print(f"Помилка завантаження гри: {e}")
        return False


# Створюємо коробку для фігур (адаптовану під мобільний формат)
piece_box = create_piece_container(MOBILE_SIDE_MARGIN)

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
    global grid, piece_box, dragging, dragged_piece, dragged_piece_index, drag_offset_x, drag_offset_y, drag_block_col, drag_block_row, game_over_check_counter, waiting_for_rotate_click
    
    # Відтворюємо звук нової гри
    sound_manager.play_new_game_sound()
    
    # Створюємо нову сітку
    grid = grid_module.Grid()
    
    # Створюємо нову коробку з фігурами (адаптовану під мобільний)
    piece_box = create_piece_container(MOBILE_SIDE_MARGIN)
    
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

def handle_menu_result(result):
    """Обробляє результат вибору в меню (нова гра, продовжити, вихід)"""
    global running
    print(f"Обробляю результат меню: {result}")
    if result == 'continue':
        if not load_saved_game():
            reset_game()
    elif result == 'new_game':
        print("Запускаю нову гру...")
        game_save_manager.delete_save()
        reset_game()
    elif result == 'menu':
        print("Повертаюся в головне меню...")
        # Повертаємося в головне меню
        save_current_game()
        menu_result = menu_system.main_menu_loop(records_manager, background_image, game_save_manager)
        custom_cursor.ensure_custom_cursor()
        handle_menu_result(menu_result)
    elif result == 'quit':
        print("Вихід з гри...")
        running = False

def handle_events():
    """Обробляє всі події (миша, клавіатура)"""
    global running, dragging, dragged_piece, dragged_piece_index, drag_offset_x, drag_offset_y, drag_block_col, drag_block_row, waiting_for_rotate_click, mouse_pos

    for event in pygame.event.get():
        custom_cursor.handle_mouse_event(event)

        if event.type == pygame.QUIT:
            running = False
            return

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu.toggle_pause()
            elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                reset_game()
            elif event.key == pygame.K_c:
                cash_manager.add_coins(1000)
                sound_manager.play_pick_sound()
                print(f"💰 Додано 1000 catcoin! Поточний баланс: {cash_manager.get_balance()}")
            elif not pause_menu.is_paused:
                if event.key == pygame.K_r:
                    # Очищаємо сітку
                    for row in range(grid.size):
                        for col in range(grid.size):
                            grid.cells[row][col] = None
                    grid.score = 0
                elif event.key == pygame.K_n:
                    reset_game()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pause_menu.is_paused:
                pause_action = pause_menu.handle_click(mouse_pos)
                if pause_action:
                    if pause_action == 'resume':
                        pause_menu.toggle_pause()
                    elif pause_action == 'restart':
                        pause_menu.toggle_pause()
                        reset_game()
                    elif pause_action == 'settings':
                        result = settings_menu.show_settings_screen()
                        custom_cursor.ensure_custom_cursor()
                        if result == "quit":
                            running = False
                    elif pause_action == 'help':
                        print("Перетягніть фігури на сітку щоб заповнити лінії!")
                    elif pause_action == 'menu':
                        save_current_game()
                        pause_menu.toggle_pause()
                        menu_result = menu_system.main_menu_loop(records_manager, background_image, game_save_manager)
                        handle_menu_result(menu_result)
                continue

            # Перевіряємо клік по мобільним кнопкам header'а
            if MOBILE_BACK_BUTTON_X <= mouse_pos[0] <= MOBILE_BACK_BUTTON_X + MOBILE_BUTTON_SIZE and \
               MOBILE_BACK_BUTTON_Y <= mouse_pos[1] <= MOBILE_BACK_BUTTON_Y + MOBILE_BUTTON_SIZE:
                save_current_game()
                pause_menu.toggle_pause()
                menu_result = menu_system.main_menu_loop(records_manager, background_image, game_save_manager)
                handle_menu_result(menu_result)
                continue
            
            if MOBILE_SETTINGS_BUTTON_X <= mouse_pos[0] <= MOBILE_SETTINGS_BUTTON_X + MOBILE_BUTTON_SIZE and \
               MOBILE_SETTINGS_BUTTON_Y <= mouse_pos[1] <= MOBILE_SETTINGS_BUTTON_Y + MOBILE_BUTTON_SIZE:
                result = settings_menu.show_settings_screen()
                custom_cursor.ensure_custom_cursor()
                if result == "quit":
                    running = False
                continue

            if pause_button.handle_click(mouse_pos):
                pause_menu.toggle_pause()
                continue

            # Перевіряємо кліки по мобільним кнопкам магазину (адаптивні розміри)
            shop_clicked = False
            button_width = (SHOP_CONTAINER_WIDTH - 60) // 4
            button_height = max(40, SHOP_CONTAINER_HEIGHT - 35)
            button_y = SHOP_CONTAINER_Y + 25
            
            shop_items = [
                ("🔄", 15, "rotate"),
                ("💥", 25, "reset"), 
                ("💎", 0, "copy"),
                ("💡", 10, "hint")
            ]
            
            for i, (icon, price, action) in enumerate(shop_items):
                button_x = MOBILE_SIDE_MARGIN + 10 + i * (button_width + 10)
                
                if (button_x <= mouse_pos[0] <= button_x + button_width and 
                    button_y <= mouse_pos[1] <= button_y + button_height):
                    shop_clicked = True
                    
                    if cash_manager.get_cash() >= price:
                        if action == "rotate":
                            cash_manager.spend_cash(price)
                            print("Куплено: Обернути фігуру! Клікніть на фігуру для обертання.")
                            sound_manager.play_shop_sound()
                            waiting_for_rotate_click = True
                        elif action == "reset":
                            cash_manager.spend_cash(price)
                            cleared_count = grid.clear_random_cells(5)
                            print(f"Куплено: Очистити 5 комірок! Очищено {cleared_count} комірок.")
                            sound_manager.play_shop_sound()
                        elif action == "copy":
                            # Безкоштовний бонус
                            cash_manager.apply_bonus_multiplier(grid.score)
                            print("Бонус застосовано!")
                            sound_manager.play_shop_sound()
                        elif action == "hint":
                            cash_manager.spend_cash(price)
                            print("Підказка активована! (поки що заглушка)")
                            sound_manager.play_shop_sound()
                    else:
                        print(f"Недостатньо коштів! Потрібно {price} catcoin.")
                        sound_manager.play_click_sound()
                    break
                    
            if shop_clicked:
                continue

            shop_result = shop.handle_click(mouse_pos[0], mouse_pos[1], cash_manager, piece_box)
            if shop_result:
                if shop_result == "rotate_purchased":
                    print("Куплено: Обернути фігуру! Клікніть на фігуру для обертання.")
                    sound_manager.play_shop_sound()
                    waiting_for_rotate_click = True
                elif shop_result == "clear_cells_purchased":
                    cleared_count = grid.clear_random_cells(5)
                    print(f"Куплено: Очистити 5 комірок! Очищено {cleared_count} комірок.")
                    sound_manager.play_shop_sound()
                elif shop_result == "insufficient_funds":
                    print("Недостатньо коштів!")
                continue

            if waiting_for_rotate_click:
                piece_index, _, _ = piece_box.get_piece_at_mouse(mouse_pos[0], mouse_pos[1])
                if piece_index is not None:
                    # Перевіряємо, чи можна повернути фігуру перед витратою купленого повороту
                    piece = piece_box.pieces[piece_index]
                    if not piece.can_rotate():
                        print("⚠️ Цю фігуру не можна повернути - вона симетрична!")
                        sound_manager.play_click_sound()  # Звук помилки замість витрати повороту
                        # НЕ скидаємо waiting_for_rotate_click, щоб гравець міг вибрати іншу фігуру
                        continue
                    
                    # Фігуру можна повернути - виконуємо поворот
                    if piece_box.rotate_piece(piece_index):
                        print("Фігуру повернуто!")
                        sound_manager.play_rotate_sound()
                    waiting_for_rotate_click = False
                    continue
                else:
                    waiting_for_rotate_click = False
                    print("Обертання скасовано")

            clicked_piece_index, offset_x, offset_y = get_piece_at_mouse(mouse_pos)
            if clicked_piece_index is not None:
                piece_index, block_col, block_row = piece_box.get_block_position_in_piece(mouse_pos[0], mouse_pos[1])
                dragging = True
                dragged_piece = piece_box.pieces[clicked_piece_index]
                dragged_piece_index = clicked_piece_index
                drag_offset_x = offset_x
                drag_offset_y = offset_y
                drag_block_col = block_col if block_col is not None else 0
                drag_block_row = block_row if block_row is not None else 0
                piece_box.start_dragging(clicked_piece_index)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging and dragged_piece:
                grid_x, grid_y = grid.mouse_to_grid(mouse_pos[0], mouse_pos[1])
                target_grid_x = grid_x - drag_block_col
                target_grid_y = grid_y - drag_block_row
                
                placed = False
                if grid.can_place_piece(dragged_piece, target_grid_x, target_grid_y):
                    old_score = grid.score
                    grid.place_piece(dragged_piece, target_grid_x, target_grid_y)
                    grid.clear_lines()
                    score_increase = grid.score - old_score
                    if score_increase > 0:
                        cash_manager.update_from_score(score_increase)
                    placed = True
                else:
                    print("Неможливо розмістити фігуру тут")
                
                piece_box.stop_dragging(placed)
            
            dragging = False
            dragged_piece = None
            dragged_piece_index = None

def draw_game_elements():
    """Малює всі елементи гри на екрані (адаптовано під мобільний)"""
    global mouse_pos
    screen.fill(BACKGROUND_COLOR)
    
    # Малюємо мобільний header
    best_score = records_manager.get_best_score()
    draw_mobile_header(screen, grid.score, best_score)
    
    # Малюємо ігрове поле
    grid.draw(screen)
    
    # Малюємо рамку (якщо потрібно)
    frame_manager.update_frame(grid.score)
    frame_manager.draw(screen)

    if not pause_menu.is_paused:
        # Замість старого магазину малюємо мобільний
        draw_mobile_shop(screen)
        
        # Малюємо рекламний блок
        draw_mobile_ad_space(screen)

        if dragging and dragged_piece:
            grid_x, grid_y = grid.mouse_to_grid(mouse_pos[0], mouse_pos[1])
            target_grid_x = grid_x - drag_block_col
            target_grid_y = grid_y - drag_block_row
            ui_effects.draw_enhanced_preview(screen, grid, dragged_piece, target_grid_x, target_grid_y)
        else:
            ui_effects.stop_blinking()

        ui_effects.draw_simple_piece_box(screen, piece_box)
        piece_box.draw(screen)

        if waiting_for_rotate_click:
            # Малюємо рамку навколо контейнера
            pygame.draw.rect(screen, UI_ROTATION_HIGHLIGHT_COLOR, 
                            (piece_box.start_x - 5, piece_box.start_y - 5, 
                            piece_box.width + 10, piece_box.height + 10), 3)
            
            # Текст підказки
            font = pygame.font.Font(UI_FONT_FAMILY_DEFAULT, UI_FONT_ROTATION_HINT)
            hint_text = font.render("Оберіть фігуру для обертання", True, UI_ROTATION_HINT_COLOR)
            text_x = piece_box.start_x + (piece_box.width - hint_text.get_width()) // 2
            text_y = piece_box.start_y - 40
            screen.blit(hint_text, (text_x, text_y))

        if dragging and dragged_piece:
            scaled_offset_x = drag_offset_x * CACHED_SCALE_FACTOR
            scaled_offset_y = drag_offset_y * CACHED_SCALE_FACTOR
            dragged_piece.draw(screen, mouse_pos[0] - scaled_offset_x, mouse_pos[1] - scaled_offset_y, PIECE_CELL_SIZE)

    if pause_menu.is_paused:
        pause_menu.draw(screen)
    
    if settings_menu.show_fps:
        game_ui.draw_fps(clock.get_fps(), settings_menu.show_fps)
    
    custom_cursor.draw(screen, mouse_pos)
    pygame.display.flip()

# --- Основний потік гри ---

# Оптимізація: завантажуємо фон один раз
background_image = get_background_image()

# Показуємо заставку та меню
menu_result = menu_system.main_menu_loop(records_manager, background_image, game_save_manager)
custom_cursor.ensure_custom_cursor()
handle_menu_result(menu_result)

# Якщо гра не була закрита з меню, але могла бути запущена з 'продовжити'
if running and menu_result != 'continue':
    reset_game()

# Головний ігровий цикл
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # Оновлення ховер-ефектів
    if pause_menu.is_paused:
        pause_menu.handle_mouse_motion(mouse_pos)
    else:
        pause_button.handle_mouse_motion(mouse_pos)
    
    handle_events()

    if not pause_menu.is_paused:
        game_over_check_counter += 1
        if game_over_check_counter >= GAME_OVER_CHECK_INTERVAL:
            game_over_check_counter = 0
            if check_game_over():
                print("🎮 GAME OVER! Показую екран завершення гри...")
                sound_manager.play_game_over_sound()
                result = show_game_over_screen()
                print(f"Результат з екрану Game Over: {result}")
                if result == "quit":
                    running = False
                else:
                    handle_menu_result(result)

    draw_game_elements()
    
    clock.tick(60)

# --- Завершення гри ---

save_current_game()
custom_cursor.cleanup()
pygame.quit()
exit()