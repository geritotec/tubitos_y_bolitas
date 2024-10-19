import pygame, sys, os, math
from components.button import draw_button
from utilities.generar_tubitos import generar_tubitos
from utilities.mover_bolita import mover_bolita
from components.limbo import limbo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
OFFSET_X = 160
OFFSET_Y = 150
TUBE_WIDTH, TUBE_HEIGHT = 130, 180
TUBE_MARGIN = 0
BALLS_PER_COLOR = 4
FLOWER_PATH = "static/flores/"
HEART_IMAGE_PATH = "static/heart.png"

color_map = {
    "rosa": "1", "amarillo": "2", "aqua": "3",
    "naranja": "4", "morado": "5", "checker_blanco": "6",
    "checker_aqua": "7", "checker_rosa": "8", "checker_naranja": "9"
}

def load_flower_image(color_key, pose, index):
    color_number = color_map[color_key]
    filename = f"{color_number}_{pose}.png"
    flower_image = pygame.image.load(os.path.join(FLOWER_PATH, filename)).convert_alpha()

    if index == 2:
        flower_image = pygame.transform.scale(flower_image, (160, 160)) 
        flower_image = pygame.transform.rotate(flower_image, 30) 
    elif index == 3:
        flower_image = pygame.transform.scale(flower_image, (160, 160))  
        flower_image = pygame.transform.rotate(flower_image, 35)  
    else:
        flower_image = pygame.transform.scale(flower_image, (192, 192))  

    if index in [1, 3]:  
        flower_image = pygame.transform.flip(flower_image, True, False)
    
    flower_image.set_alpha(128)

    return flower_image


def reto_easy_mode(screen, switch_screen, font):
    
    screen_width, screen_height = pygame.display.get_surface().get_size()
    tubitos = generar_tubitos(1)
    vidas = [3]
    actual = ["main_game"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if actual[0] == "main_game":
            main_game(screen, font, screen_width, screen_height, tubitos, actual, vidas)
        elif actual[0] == "limbo":
            limbo(screen, switch_screen, font, screen_width, screen_height, actual, vidas, 1)

        pygame.display.flip()


def main_game(screen, font, screen_width, screen_height, tubitos, actual, vidas):
    pygame.mixer.init() 
    pygame.mixer.music.load("static/lallorona.mp3")  
    mariachis_image = pygame.image.load("static/mariachis_asleep_5.png")
    mariachis_win_image = pygame.image.load("static/mariachis_win_5.png")
    background_win = pygame.transform.scale(mariachis_win_image, (screen_width, screen_height))
    background = pygame.transform.scale(mariachis_image, (screen_width, screen_height))

    try:
        heart_image = pygame.image.load(HEART_IMAGE_PATH).convert_alpha()
        heart_image = pygame.transform.scale(heart_image, (64,64)) 
    except pygame.error:
        heart_image = None  

    total_tubitos = len(tubitos)
    tubes = [pygame.Rect(TUBE_MARGIN + i * (TUBE_WIDTH + TUBE_MARGIN) + OFFSET_X,
                         screen_height // 2 - TUBE_HEIGHT // 2 + OFFSET_Y,
                         TUBE_WIDTH, TUBE_HEIGHT) for i in range(total_tubitos)]    
    selected_tube = None
    solved = False
    fade_start_time = None  
    alpha = 255 
    shaking = False
    shake_start_time = 0
    shake_duration = 500  
    shake_amplitude = 10 

    retry_button_text = "Retry"
    retry_button_color = GRAY
    retry_button_hover_color = WHITE
    retry_button_width = 100
    retry_button_height = 50
    retry_button_x = screen_width - retry_button_width - 20  
    retry_button_y = 20 

    retry_button_rect = pygame.Rect(retry_button_x, retry_button_y, retry_button_width, retry_button_height)

    def check_solved():
        for tube in tubitos:
            if len(set(tube)) != 1 and tube.count("nada") != BALLS_PER_COLOR:
                return False
        return True

    while True:
        offset_x = 0
        offset_y = 0
        if shaking:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - shake_start_time
            if elapsed < shake_duration:
                shake_progress = elapsed / shake_duration
                angle = shake_progress * math.pi * 4  
                offset_x = shake_amplitude * math.sin(angle)
                offset_y = shake_amplitude * math.cos(angle)
            else:
                shaking = False 

        temp_surface = pygame.Surface((screen_width, screen_height)).convert_alpha()

        if solved and fade_start_time:
            elapsed_time = pygame.time.get_ticks() - fade_start_time
            alpha = max(255 - elapsed_time // 5, 0)  
            if alpha == 0:
                temp_surface.blit(background_win, (0, 0))  
            else:
                temp_surface.blit(background, (0, 0))  
                win_alpha = 255 - alpha  
                win_surface = pygame.Surface((screen_width, screen_height)).convert_alpha()
                win_surface.blit(background_win, (0, 0)) 
                win_surface.set_alpha(win_alpha)
                temp_surface.blit(win_surface, (0, 0))  

        else:
            temp_surface.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  

            elif event.type == pygame.MOUSEBUTTONDOWN and not solved:
                mouse_pos = pygame.mouse.get_pos()
                adjusted_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

                if retry_button_rect.collidepoint(mouse_pos):
                    tubitos.clear()
                    tubitos.extend(generar_tubitos(1)) 
                    vidas[0] = 3 
                    selected_tube = None
                    solved = False
                    alpha = 255
                    fade_start_time = None
                    shake_start_time = 0
                    shaking = False
                    continue  

                for i, tube in enumerate(tubes):
                    if tube.collidepoint(adjusted_mouse_pos):
                        if selected_tube is None:
                            if any(ball != "nada" for ball in tubitos[i]):
                                selected_tube = i
                        else:
                            if mover_bolita(tubitos, selected_tube, i):
                                if check_solved():
                                    solved = True
                                    fade_start_time = pygame.time.get_ticks()
                                    pygame.mixer.music.play()

                            else:
                                if vidas[0] > 1:
                                    vidas[0] -= 1
                                    shaking = True
                                    shake_start_time = pygame.time.get_ticks()
                                else:
                                    actual[0] = "limbo"
                                    return
                            selected_tube = None

        if solved and fade_start_time:
            elapsed_time = pygame.time.get_ticks() - fade_start_time
            alpha = max(255 - elapsed_time // 5, 0) 
            if alpha == 0:
                pass

        for i, tube in enumerate(tubes):
            y_offset = TUBE_HEIGHT - 30
            for ball_idx, ball_color in enumerate(tubitos[i]):
                if ball_color != "nada" and ball_color in color_map:
                    pose = 'b' if selected_tube == i and ball_idx == len(tubitos[i]) - tubitos[i].count("nada") - 1 else 'a'
                    flower_image = load_flower_image(ball_color, pose, ball_idx)
                    flower_image.set_alpha(alpha) 

                    x_offset_flower, more_y_offset = (9 if ball_idx in [0, 2] else -9), 0
                    if selected_tube == i and ball_idx == len(tubitos[i]) - tubitos[i].count("nada") - 1:
                        more_y_offset = -50

                    x_translation = 0
                    y_translation = 0

                    if ball_idx == 2:
                        y_translation += -15 

                    elif ball_idx == 3:
                        y_translation += 15

                    temp_surface.blit(
                        flower_image,
                        (
                            tube.centerx - flower_image.get_width() // 2 + x_offset_flower + x_translation,
                            tube.y + y_offset - 160 + more_y_offset + y_translation
                        )
                    )
                    y_offset -= flower_image.get_height() - 183


        lives_position = (20, 20)  
        if heart_image:
            for life in range(vidas[0]):
                temp_surface.blit(heart_image, (lives_position[0] + life * (heart_image.get_width()), lives_position[1]))
        else:
            lives_text = font.render(f"Vidas: {vidas[0]}", True, BLACK)
            temp_surface.blit(lives_text, lives_position)

        mouse_pos = pygame.mouse.get_pos()
        if retry_button_rect.collidepoint(mouse_pos):
            button_color = retry_button_hover_color
        else:
            button_color = retry_button_color

        pygame.draw.rect(temp_surface, button_color, retry_button_rect)
        retry_text = font.render(retry_button_text, True, BLACK)
        retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
        temp_surface.blit(retry_text, retry_text_rect)

        screen.blit(temp_surface, (offset_x, offset_y))
        pygame.display.flip()
