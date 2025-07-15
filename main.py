import pygame
from sys import exit
import time  # Імпорт модуля для роботи з часом

# імпорт модулів гри з папки DROPBOX
from constants import*  # Імпорт констант
import grid
import piece
import ui
from menu import Menu
#-------------------

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Drop Box")
pygame.display.set_icon(pygame.image.load("image/icon.png"))

# Додаємо шрифт для очок
score_font = pygame.font.SysFont("Arial", 36, bold=True)


# Створюємо об'єкти
grid = grid.Grid() # ігрове поле
test_piece = piece.SingleBlock()
test_piece2 = piece.TShape() 
test_piece3 = piece.LShape()




menu = Menu(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE)

# Показуємо заставку та меню
menu.show_splash_screen()
menu.main_menu()  # Запускаємо меню і чекаємо натискання "Грати"



# Основний цикл гри (запускається після натискання "Грати")
running = True
dragging = False
dragged_piece = None

def get_piece_at_mouse(mouse_pos):
    """Перевіряє, на яку фігуру натиснув користувач"""
    mouse_x, mouse_y = mouse_pos
    
    # Перевіряємо test_piece (позиція 1000, 200, розмір 48x48)
    if 1000 <= mouse_x <= 1048 and 200 <= mouse_y <= 248:
        return test_piece
    
    # Перевіряємо test_piece2 (позиція 950, 270)
    if 950 <= mouse_x <= 1046 and 270 <= mouse_y <= 366:  # TShape більша
        return test_piece2
    
    # Перевіряємо test_piece3 (позиція 1000, 420)
    if 1000 <= mouse_x <= 1096 and 420 <= mouse_y <= 564:  # LShape більша
        return test_piece3
    
    return None  # Якщо не натиснули на жодну фігуру





while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Почати перетягування
            mouse_pos = pygame.mouse.get_pos()
            clicked_piece = get_piece_at_mouse(mouse_pos)
            if clicked_piece:
                dragging = True
                dragged_piece = clicked_piece
                print(f"Почали перетягувати фігуру з позиції: {mouse_pos}")
            
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
                    print(f"Фігуру розміщено на позиції ({grid_x}, {grid_y})")
                else:
                    print(f"Неможливо розмістити фігуру на позиції ({grid_x}, {grid_y})")
            dragging = False
            dragged_piece = None
            
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

    # Підсвічування під час перетягування
    if dragging and dragged_piece:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = grid.mouse_to_grid(mouse_x, mouse_y)
        valid = grid.can_place_piece(dragged_piece, grid_x, grid_y)
        grid.highlight_position(screen, grid_x, grid_y, dragged_piece, valid=valid)

    # Малюємо фігури (але не ту, яку перетягуємо)
    if not (dragging and dragged_piece == test_piece):
        test_piece.draw(screen, 1000, 200, 48)
    if not (dragging and dragged_piece == test_piece2):
        test_piece2.draw(screen, 950, 270, 48)
    if not (dragging and dragged_piece == test_piece3):
        test_piece3.draw(screen, 1000, 420, 48)

    # Якщо перетягуємо фігуру - малюємо її під мишею
    if dragging and dragged_piece:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dragged_piece.draw(screen, mouse_x - 24, mouse_y - 24, 48)
        dragged_piece.draw(screen, mouse_x - 24, mouse_y - 24, 48)



    pygame.display.flip() # Оновлюємо екран
    clock.tick(60)
pygame.quit()
exit()    