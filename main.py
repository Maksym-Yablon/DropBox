import pygame
from sys import exit
import time  # Імпорт модуля для роботи з часом

# імпорт модулів гри з папки DROPBOX
from constants import*  # Імпорт констант
import grid
import piece
import ui
from menu import Menu
from records import records_manager  # Імпортуємо менеджер рекордів
#-------------------

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Drop Box")
pygame.display.set_icon(pygame.image.load("image/icon.png"))

# Додаємо шрифти
score_font = pygame.font.SysFont("Arial", 36, bold=True)
record_font = pygame.font.SysFont("Arial", 24, bold=True)

# Створюємо об'єкти
import grid as grid_module
grid = grid_module.Grid() # ігрове поле

menu = Menu(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE)

# Показуємо заставку та меню
menu.show_splash_screen()
menu.main_menu()  # Запускаємо меню і чекаємо натискання "Грати"



# Основний цикл гри (запускається після натискання "Грати")
running = True
dragging = False
dragged_piece = None
dragged_piece_index = None  # Індекс фігури в коробці

def get_piece_at_mouse(mouse_pos):
    """Перевіряє, чи клікнули на фігуру в коробці"""
    return piece_box.get_piece_at_mouse(mouse_pos[0], mouse_pos[1])

def replace_used_piece(piece_index):
    """Замінює використану фігуру на нову випадкову"""
    piece_box.replace_piece(piece_index)

# Створюємо коробку для фігур (розміщена праворуч від сітки)
from piece import PieceBox
piece_box = PieceBox(1000, 100)

def show_game_over_screen():
    """Показує екран завершення гри з результатами"""
    final_score = grid.score
    
    # Додаємо рекорд
    is_new_record = records_manager.add_record(final_score)
    
    # Повідомляємо гравця в консоль
    if is_new_record:
        print(f"🎉 НОВИЙ РЕКОРД! Очки: {final_score}")
        position = records_manager.get_player_position(final_score)
        if position:
            print(f"Ваша позиція: {position} місце")
    else:
        print(f"Гра завершена! Очки: {final_score}")
        best_score = records_manager.get_best_score()
        print(f"Найкращий результат: {best_score}")
    
    # Екран результатів
    while True:
        # Ініціалізуємо кнопки
        try_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 350, 300, 60)
        menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 430, 200, 60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Перевіряємо натискання кнопок
                if try_again_button.collidepoint(event.pos):
                    return "restart"
                elif menu_button.collidepoint(event.pos):
                    return "menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
        
        # Малюємо екран результатів
        screen.fill(CARROT)
        
        # Заголовок
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        if is_new_record:
            title_text = title_font.render("🎉 НОВИЙ РЕКОРД!", True, (255, 0, 0))
        else:
            title_text = title_font.render("ГРА ЗАВЕРШЕНА", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Очки
        score_display_font = pygame.font.SysFont("Arial", 36, bold=True)
        score_display_text = score_display_font.render(f"Ваш результат: {final_score} очок", True, BLACK)
        score_display_rect = score_display_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(score_display_text, score_display_rect)
        
        # Найкращий результат
        best_score = records_manager.get_best_score()
        best_score_text = record_font.render(f"Найкращий результат: {best_score}", True, (100, 0, 0))
        best_score_rect = best_score_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
        screen.blit(best_score_text, best_score_rect)
        
        # Кнопки
        button_font = pygame.font.SysFont("Arial", 32, bold=True)
        
        # Малюємо кнопку "Спробувати ще раз"
        pygame.draw.rect(screen, GREEN, try_again_button)
        try_again_text = button_font.render("Спробувати ще раз", True, BLACK)
        try_again_text_rect = try_again_text.get_rect(center=try_again_button.center)
        screen.blit(try_again_text, try_again_text_rect)
        
        # Малюємо кнопку "Головне меню"
        pygame.draw.rect(screen, LIGHTBLUE, menu_button)
        menu_text = button_font.render("Головне меню", True, BLACK)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        screen.blit(menu_text, menu_text_rect)
        
        # Інструкції
        instruction_font = pygame.font.SysFont("Arial", 20)
        instruction1 = instruction_font.render("ПРОБІЛ - грати знову, ESC - меню", True, (100, 100, 100))
        instruction1_rect = instruction1.get_rect(center=(SCREEN_WIDTH // 2, 550))
        screen.blit(instruction1, instruction1_rect)
        
        pygame.display.flip()
        clock.tick(60)

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
    global grid, piece_box, dragging, dragged_piece, dragged_piece_index
    
    # Створюємо нову сітку
    grid = grid_module.Grid()
    
    # Створюємо нову коробку з фігурами
    piece_box = PieceBox(1000, 100)
    
    # Скидаємо стан перетягування
    dragging = False
    dragged_piece = None
    dragged_piece_index = None
    
    print("Гру скинуто! Нова гра почалася.")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Почати перетягування
            mouse_pos = pygame.mouse.get_pos()
            clicked_piece_index = get_piece_at_mouse(mouse_pos)
            if clicked_piece_index is not None:
                dragging = True
                dragged_piece = piece_box.pieces[clicked_piece_index]
                dragged_piece_index = clicked_piece_index
                print(f"Почали перетягувати фігуру {clicked_piece_index} з позиції: {mouse_pos}")
            
        elif event.type == pygame.MOUSEBUTTONUP:
            # Закінчити перетягування
            if dragging and dragged_piece:
                mouse_pos = pygame.mouse.get_pos()
                grid_x, grid_y = grid.mouse_to_grid(mouse_pos[0], mouse_pos[1])
                
                # Перевіряємо, чи можна розмістити фігуру
                if grid.can_place_piece(dragged_piece, grid_x, grid_y):
                    # Розміщуємо фігуру на сітці
                    grid.place_piece(dragged_piece, grid_x, grid_y)
                    grid.clear_lines()  # Перевіряємо на очищення ліній
                    
                    # Замінюємо використану фігуру на нову
                    replace_used_piece(dragged_piece_index)
                    
                    print(f"Фігуру розміщено на позиції ({grid_x}, {grid_y})")
                else:
                    print(f"Неможливо розмістити фігуру на позиції ({grid_x}, {grid_y})")
            dragging = False
            dragged_piece = None
            dragged_piece_index = None
            
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                # Оновлюємо позицію для відображення під мишею
            
    # код гри
    screen.fill(CARROT)
    grid.draw(screen)  # малюємо ігрове поле

    # Відображаємо очки у верхньому лівому куті
    score_text = score_font.render(f"Очки: {grid.score}", True, (0, 0, 0))
    screen.blit(score_text, (30, 30))
    
    # Відображаємо найкращий рекорд
    best_score = records_manager.get_best_score()
    record_text = record_font.render(f"Рекорд: {best_score}", True, (100, 0, 0))
    screen.blit(record_text, (30, 80))

    # Підсвічування під час перетягування
    if dragging and dragged_piece:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = grid.mouse_to_grid(mouse_x, mouse_y)
        valid = grid.can_place_piece(dragged_piece, grid_x, grid_y)
        grid.highlight_position(screen, grid_x, grid_y, dragged_piece, valid=valid)

    # Малюємо коробку з фігурами (крім тої, що перетягується)
    piece_box.draw(screen, dragged_piece_index if dragging else None)
    
    # Для налагодження: малюємо рамку коробки
    piece_box.draw_box_outline(screen)

    # Якщо перетягуємо фігуру - малюємо її під мишею
    if dragging and dragged_piece:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dragged_piece.draw(screen, mouse_x - 24, mouse_y - 24, 48)


    # Перевірка на кінець гри
    if check_game_over():
        result = show_game_over_screen()
        if result == "restart":
            reset_game()
        elif result == "menu":
            # Повертаємося до меню
            menu.main_menu()
            reset_game()
        elif result == "quit":
            running = False
    
    pygame.display.flip() # Оновлюємо екран
    clock.tick(60) # FPS в грі
pygame.quit()
exit()