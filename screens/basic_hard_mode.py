import pygame, sys, os
from utilities.generar_tubitos import generar_tubitos
from utilities.mover_bolita import mover_bolita

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

WHITE = (255, 255, 255)
OFFSET_X = 201
OFFSET_Y = 150
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
TUBE_WIDTH, TUBE_HEIGHT = 51, 180
TUBE_MARGIN = 0
BALLS_PER_COLOR = 4
FLOWER_PATH = "static/flores/"

# Adjusted color map to link with flower images
color_map = {
    "rosa": "1", "amarillo": "2", "aqua": "3",
    "naranja": "4", "morado": "5", "checker_blanco": "6",
    "checker_aqua": "7", "checker_rosa": "8", "checker_naranja": "9"
}

def load_flower_image(color_key, pose, index):
    color_number = color_map[color_key]
    filename = f"{color_number}_{pose}.png"
    flower_image = pygame.image.load(os.path.join(FLOWER_PATH, filename)).convert_alpha()

    # Adjust size based on index 2 and 3, and rotate accordingly
    if index == 2:
        flower_image = pygame.transform.scale(flower_image, (160, 160))  # Slightly smaller
        flower_image = pygame.transform.rotate(flower_image, 30)  # Rotate left
    elif index == 3:
        flower_image = pygame.transform.scale(flower_image, (160, 160))  # Slightly smaller
        flower_image = pygame.transform.rotate(flower_image, 35)  # Rotate right
    else:
        flower_image = pygame.transform.scale(flower_image, (192, 192))  # Default size

    if index in [1, 3]:  # Flip image horizontally for specific flowers
        flower_image = pygame.transform.flip(flower_image, True, False)
    
    flower_image.set_alpha(128)

    return flower_image


def basic_hard_mode(screen, switch_screen, font):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    tubitos = generar_tubitos(3)

    mariachis_image = pygame.image.load("static/mariachis11.png")
    background = pygame.transform.scale(mariachis_image, (screen_width, screen_height))

    total_tubitos = len(tubitos)
    tubes = [pygame.Rect(TUBE_MARGIN + i * (TUBE_WIDTH + TUBE_MARGIN) + OFFSET_X,
                         screen_height // 2 - TUBE_HEIGHT // 2 + OFFSET_Y,
                         TUBE_WIDTH, TUBE_HEIGHT) for i in range(total_tubitos)]

    selected_tube = None
    solved = False
    fade_start_time = None  # Track the start of the fade-out
    alpha = 255  # Initial alpha value for flowers (fully visible)

    def check_solved():
        for tube in tubitos:
            if len(set(tube)) != 1 and tube.count("nada") != BALLS_PER_COLOR:
                return False
        return True

    while True:
        screen.blit(background, (0, 0))

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
                                print(f"Moved ball from tube {selected_tube + 1} to tube {i + 1}")
                                if check_solved():
                                    solved = True
                                    fade_start_time = pygame.time.get_ticks()  # Start fade-out timer
                                    print("Solved is set to true")
                            selected_tube = None

        if solved and fade_start_time:  # Manage the fade-out effect
            elapsed_time = pygame.time.get_ticks() - fade_start_time
            alpha = max(255 - elapsed_time // 5, 0)  # Decrease alpha gradually
            if alpha == 0:
                pass
                # Iniciar animación

        # Draw flowers with fade-out effect
        for i, tube in enumerate(tubes):
            y_offset = TUBE_HEIGHT - 30
            for ball_idx, ball_color in enumerate(tubitos[i]):
                if ball_color != "nada" and ball_color in color_map:
                    pose = 'b' if selected_tube == i and ball_idx == len(tubitos[i]) - tubitos[i].count("nada") - 1 else 'a'
                    flower_image = load_flower_image(ball_color, pose, ball_idx)
                    flower_image.set_alpha(alpha)  # Apply current alpha value

                    x_offset, more_y_offset = (9 if ball_idx in [0, 2] else -9), 0
                    if selected_tube == i and ball_idx == len(tubitos[i]) - tubitos[i].count("nada") - 1:
                        more_y_offset = -50

                    x_translation = 0
                    y_translation = 0

                    if ball_idx == 2:  # Translate the flower at index 2
                        y_translation += -15   # Move up

                    elif ball_idx == 3:  # Translate the flower at index 3
                        y_translation += 15

                    screen.blit(
                        flower_image,
                        (tube.centerx - flower_image.get_width() // 2 + x_offset,
                         tube.y + y_offset - 160 + more_y_offset + y_translation)
                    )
                    y_offset -= flower_image.get_height() - 183

        if solved:
            congrats_text = font.render("Ganaste!", True, WHITE)
            screen.blit(congrats_text, (screen_width // 2 - congrats_text.get_width() // 2,
                                        screen_height // 2 - congrats_text.get_height() // 2))

        pygame.display.flip()
