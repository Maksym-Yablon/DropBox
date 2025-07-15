import pygame
from sys import exit

# Імпорт модулів гри
from constants import *
import grid as grid_module
from piece import PieceBox
import ui
from ui import ui_effects, GameOverScreen, GameUI, MenuSystem
from records import records_manager

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Drop Box")
pygame.display.set_icon(pygame.image.load("image/icon.png"))

# Створюємо об'єкти UI
grid = grid_module.Grid()  # Ігрове поле
game_over_screen = GameOverScreen(screen, clock)
game_ui = GameUI(screen)
menu_system = MenuSystem(screen, clock)

# Показуємо заставку та меню
menu_system.main_menu_loop(records_manager, get_background_image())


# Основний цикл гри (запускається після натискання "Грати")
running = True
dragging = False
dragged_piece = None
dragged_piece_index = None  # Індекс фігури в коробці
drag_offset_x = 0  # Зміщення кліку по X відносно фігури
drag_offset_y = 0  # Зміщення кліку по Y відносно фігури
drag_block_col = 0  # Колонка блоку в фігурі, за яку взялися
drag_block_row = 0  # Рядок блоку в фігурі, за яку взялися


def get_piece_at_mouse(mouse_pos):
    """Перевіряє, чи клікнули на фігуру в коробці"""
    return piece_box.get_piece_at_mouse(mouse_pos[0], mouse_pos[1])


# Створюємо коробку для фігур (центрована по висоті ігрового поля)
grid_height = GRID_SIZE * GRID_CELL_SIZE
container_center_y = GRID_Y + (grid_height - PIECE_CONTAINER_HEIGHT) // 2
piece_box = PieceBox(1000, container_center_y)

def show_game_over_screen():
    """Показує екран завершення гри з результатами"""
    return game_over_screen.show(grid.score, records_manager)

def game_over():
    """Обробляє завершення гри та збереження рекорду"""
    final_score = grid.score
    
    # Додаємо рекорд
    is_new_record = records_manager.add_record(final_score)
    
    # Повідомляємо гравця
    if is_new_record:
        print(f"🎉 НОВИЙ РЕКОРД! Очки: {final_score}")
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
    """Перевіряє, чи можна розмістити хоча б одну фігуру"""
    for piece in piece_box.pieces:
        # Перевіряємо всі можливі позиції на сітці
        for row in range(8):
            for col in range(8):
                if grid.can_place_piece(piece, col, row):
                    return False  # Є хоча б одна можлива позиція
    return True  # Немає жодної можливої позиції

def reset_game():
    """Скидає гру до початкового стану"""
    global grid, piece_box, dragging, dragged_piece, dragged_piece_index, drag_offset_x, drag_offset_y, drag_block_col, drag_block_row
    
    # Створюємо нову сітку
    grid = grid_module.Grid()
    
    # Створюємо нову коробку з фігурами (центрована по висоті ігрового поля)
    grid_height = GRID_SIZE * GRID_CELL_SIZE
    container_center_y = GRID_Y + (grid_height - PIECE_CONTAINER_HEIGHT) // 2
    piece_box = PieceBox(1000, container_center_y)
    
    # Скидаємо стан перетягування
    dragging = False
    dragged_piece = None
    dragged_piece_index = None
    drag_offset_x = 0
    drag_offset_y = 0
    drag_block_col = 0
    drag_block_row = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Почати перетягування
            mouse_pos = pygame.mouse.get_pos()
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
            # Закінчити перетягування
            if dragging and dragged_piece:
                mouse_pos = pygame.mouse.get_pos()
                grid_x, grid_y = grid.mouse_to_grid(mouse_pos[0], mouse_pos[1])
                
                # Корегуємо позицію з урахуванням того, за який блок фігури взялися
                target_grid_x = grid_x - drag_block_col
                target_grid_y = grid_y - drag_block_row
                
                placed = False
                # Перевіряємо, чи можна розмістити фігуру
                if grid.can_place_piece(dragged_piece, target_grid_x, target_grid_y):
                    # Розміщуємо фігуру на сітці
                    grid.place_piece(dragged_piece, target_grid_x, target_grid_y)
                    grid.clear_lines()  # Перевіряємо на очищення ліній
                    placed = True
                else:
                    print("❌ Неможливо розмістити фігуру тут")
                
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
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                # Оновлюємо позицію для відображення під мишею
        
        elif event.type == pygame.KEYDOWN:
            # Команди для налагодження
            if event.key == pygame.K_r:  # R - скидання сітки
                for row in range(8):
                    for col in range(8):
                        grid.cells[row][col] = None
                grid.score = 0
            elif event.key == pygame.K_n:  # N - Нова гра
                reset_game()
            
    # код гри
    screen.fill(BACKGROUND_COLOR)
    grid.draw(screen)  # малюємо ігрове поле

    # Відображаємо HUD (очки та рекорд)
    best_score = records_manager.get_best_score()
    game_ui.draw_hud(grid.score, best_score)

    # Підсвічування під час перетягування з новими ефектами
    if dragging and dragged_piece:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = grid.mouse_to_grid(mouse_x, mouse_y)
        
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
    piece_box.draw(screen, dragged_piece_index if dragging else None)

    # Якщо перетягуємо фігуру - малюємо її під мишею з урахуванням зміщення кліку
    if dragging and dragged_piece:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Розраховуємо скореговане зміщення через різницю розмірів
        scale_factor = PIECE_CELL_SIZE / PIECE_CONTAINER_CELL_SIZE
        scaled_offset_x = drag_offset_x * scale_factor
        scaled_offset_y = drag_offset_y * scale_factor
        
        # Віднімаємо скореговане зміщення кліку
        dragged_piece.draw(screen, mouse_x - scaled_offset_x, mouse_y - scaled_offset_y, PIECE_CELL_SIZE)


    # Перевірка на кінець гри
    if check_game_over():
        result = show_game_over_screen()
        if result == "restart":
            reset_game()
        elif result == "menu":
            # Повертаємося до меню
            menu_system.main_menu_loop(records_manager, get_background_image())
            reset_game()
        elif result == "quit":
            running = False
    
    pygame.display.flip() # Оновлюємо екран
    clock.tick(60) # FPS в грі
pygame.quit()
exit()