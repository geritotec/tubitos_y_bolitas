import pygame, sys, os
from utilities.generar_tubitos import generar_tubitos
from utilities.mover_bolita import mover_bolita

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BALL_RADIUS = 20
TUBE_WIDTH, TUBE_HEIGHT = 60, 220
TUBE_MARGIN = 20
BALLS_PER_COLOR = 4

def basic_normal_mode(screen, switch_screen, font):
    screen_width, screen_height = pygame.display.get_surface().get_size()

    tubitos = generar_tubitos(2)
    
    color_map = {
        "rosa": (255, 192, 203),
        "amarillo": (255, 255, 0),
        "aqua": (0, 255, 255),
        "naranja": (255, 165, 0),
        "morado": (128, 0, 128),
        "checker_blanco": (200, 200, 200), 
        "checker_aqua": (0, 200, 255),      
        "checker_rosa": (255, 182, 193),   
        "checker_naranja": (255, 140, 0)   
    }

    
    total_tubitos = len(tubitos)
    tubes = [pygame.Rect(TUBE_MARGIN + i * (TUBE_WIDTH + TUBE_MARGIN), screen_height // 2 - TUBE_HEIGHT // 2, TUBE_WIDTH, TUBE_HEIGHT) for i in range(total_tubitos)]
    
    selected_tube = None
    solved = False

    def check_solved():
        for tube in tubitos:
            print(tube)
            if len(set(tube)) != 1 and tube.count("nada") != BALLS_PER_COLOR:
                return False
        return True

    while True:
        screen.fill(WHITE) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False 
            elif event.type == pygame.MOUSEBUTTONDOWN and not solved:
                pos = pygame.mouse.get_pos()
                for i, tube in enumerate(tubes):
                    if tube.collidepoint(pos):
                        if selected_tube is None:
                            if any(ball != "nada" for ball in tubitos[i]):
                                selected_tube = i
                        else:
                            if mover_bolita(tubitos, selected_tube, i):
                                print(f"Moviste bolita del tubito {selected_tube + 1} al tubito {i + 1} ")
                                if check_solved():
                                    solved = True
                                    print("Solved is set to true")
                            selected_tube = None

        
        for tube in tubes:
            pygame.draw.rect(screen, GRAY, tube, 2)

        for i, tube in enumerate(tubes):
            y_offset = TUBE_HEIGHT - BALL_RADIUS * 2
            for ball_idx, ball_color in enumerate(tubitos[i]):
                if ball_color != "nada":
                    color = color_map.get(ball_color, BLACK)
                    if selected_tube == i and ball_idx == len(tubitos[i]) - tubitos[i].count("nada") - 1:  
                        pygame.draw.circle(screen, color, (tube.centerx, tube.y - BALL_RADIUS - 10), BALL_RADIUS)
                    else:
                        pygame.draw.circle(screen, color, (tube.centerx, tube.y + y_offset), BALL_RADIUS)
                    y_offset -= BALL_RADIUS * 2 + 10  

        if solved:
            congrats_text = font.render("Ganaste!", True, BLACK)
            screen.blit(congrats_text, (screen_width // 2 - congrats_text.get_width() // 2, screen_height // 2 - congrats_text.get_height() // 2))

        pygame.display.flip()
