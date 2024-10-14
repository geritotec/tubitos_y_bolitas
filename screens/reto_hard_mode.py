import pygame, sys, os, math
from components.button import draw_button
from utilities.generar_tubitos import generar_tubitos
from utilities.mover_bolita import mover_bolita
from components.limbo import limbo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
OFFSET_X = 201
OFFSET_Y = 150
TUBE_WIDTH, TUBE_HEIGHT = 51, 180
TUBE_MARGIN = 0
BALLS_PER_COLOR = 4
FLOWER_PATH = "static/flores/"
HEART_IMAGE_PATH = "static/heart.png"

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


def reto_hard_mode(screen, switch_screen, font):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    tubitos = generar_tubitos(3)
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
            limbo(screen, switch_screen, font, screen_width, screen_height, actual, vidas)

        pygame.display.flip()  # Update the full display surface to the screen


def main_game(screen, font, screen_width, screen_height, tubitos, actual, vidas):

    mariachis_image = pygame.image.load("static/mariachis11.png")
    background = pygame.transform.scale(mariachis_image, (screen_width, screen_height))

    # Load heart image for lives display (if using icons)
    try:
        heart_image = pygame.image.load(HEART_IMAGE_PATH).convert_alpha()
        heart_image = pygame.transform.scale(heart_image, (96, 96))  # Resize as needed
    except pygame.error:
        print(f"Error: Cannot load heart image from {HEART_IMAGE_PATH}. Lives will be displayed as text.")
        heart_image = None  # Fallback to text display

    # Create tubes as Pygame Rect objects
    total_tubitos = len(tubitos)
    tubes = [pygame.Rect(TUBE_MARGIN + i * (TUBE_WIDTH + TUBE_MARGIN) + OFFSET_X,
                         screen_height // 2 - TUBE_HEIGHT // 2 + OFFSET_Y,
                         TUBE_WIDTH, TUBE_HEIGHT) for i in range(total_tubitos)]    
    selected_tube = None
    solved = False
    fade_start_time = None  # Track the start of the fade-out
    alpha = 255  # Initial alpha value for flowers (fully visible)
    shaking = False
    shake_start_time = 0
    shake_duration = 500  # Duration in milliseconds
    shake_amplitude = 10  # Maximum pixels to move

    # Define the Retry button
    retry_button_text = "Retry"
    retry_button_font = pygame.font.Font(None, 36)  # Use default font; adjust size as needed
    retry_button_color = GRAY
    retry_button_hover_color = WHITE
    retry_button_width = 100
    retry_button_height = 50
    retry_button_x = screen_width - retry_button_width - 20  # 20 pixels from the right edge
    retry_button_y = 20  # 20 pixels from the top edge

    retry_button_rect = pygame.Rect(retry_button_x, retry_button_y, retry_button_width, retry_button_height)

    def check_solved():
        for tube in tubitos:
            if len(set(tube)) != 1 and tube.count("nada") != BALLS_PER_COLOR:
                return False
        return True

    while True:
        # Calculate shake offset
        offset_x = 0
        offset_y = 0
        if shaking:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - shake_start_time
            if elapsed < shake_duration:
                # Sine wave for smooth shaking
                shake_progress = elapsed / shake_duration
                angle = shake_progress * math.pi * 4  # 2 full shakes
                offset_x = shake_amplitude * math.sin(angle)
                offset_y = shake_amplitude * math.cos(angle)
            else:
                shaking = False  # Stop shaking after duration

        # Create a temporary surface for drawing
        temp_surface = pygame.Surface((screen_width, screen_height)).convert_alpha()
        temp_surface.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Ensure the program exits

            elif event.type == pygame.MOUSEBUTTONDOWN and not solved:
                mouse_pos = pygame.mouse.get_pos()
                # Adjust mouse position by subtracting the shake offsets
                adjusted_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

                # Check if the Retry button is clicked
                if retry_button_rect.collidepoint(mouse_pos):
                    # Reset the game
                    tubitos.clear()
                    tubitos.extend(generar_tubitos(3))  # Generate new tubitos
                    vidas[0] = 3  # Reset lives
                    selected_tube = None
                    solved = False
                    alpha = 255
                    fade_start_time = None
                    shake_start_time = 0
                    shaking = False
                    print("Game has been reset.")
                    continue  # Skip further processing in this loop iteration

                for i, tube in enumerate(tubes):
                    if tube.collidepoint(adjusted_mouse_pos):
                        if selected_tube is None:
                            # Select the tube
                            if any(ball != "nada" for ball in tubitos[i]):
                                selected_tube = i
                        else:
                            # Move the ball if valid
                            if mover_bolita(tubitos, selected_tube, i):
                                print(f"Moved ball from tube {selected_tube + 1} to tube {i + 1}")
                                if check_solved():
                                    solved = True
                                    fade_start_time = pygame.time.get_ticks()
                                    print("Solved is set to true")
                            else:
                                print("Invalid move")
                                if vidas[0] > 1:
                                    vidas[0] -= 1
                                    print("Lives:", vidas[0])
                                    shaking = True
                                    shake_start_time = pygame.time.get_ticks()
                                else:
                                    actual[0] = "limbo"
                                    return
                            selected_tube = None

        if solved and fade_start_time:
            elapsed_time = pygame.time.get_ticks() - fade_start_time
            alpha = max(255 - elapsed_time // 5, 0)  # Decrease alpha gradually
            if alpha == 0:
                # Here you can add additional actions when fade-out is complete
                pass

        # Draw flowers with fade-out effect on temp_surface
        for i, tube in enumerate(tubes):
            y_offset = TUBE_HEIGHT - 30
            for ball_idx, ball_color in enumerate(tubitos[i]):
                if ball_color != "nada" and ball_color in color_map:
                    pose = 'b' if selected_tube == i and ball_idx == len(tubitos[i]) - tubitos[i].count("nada") - 1 else 'a'
                    flower_image = load_flower_image(ball_color, pose, ball_idx)
                    flower_image.set_alpha(alpha)  # Apply current alpha value

                    x_offset_flower, more_y_offset = (9 if ball_idx in [0, 2] else -9), 0
                    if selected_tube == i and ball_idx == len(tubitos[i]) - tubitos[i].count("nada") - 1:
                        more_y_offset = -50

                    x_translation = 0
                    y_translation = 0

                    if ball_idx == 2:  # Translate the flower at index 2
                        y_translation += -15   # Move up

                    elif ball_idx == 3:  # Translate the flower at index 3
                        y_translation += 15

                    temp_surface.blit(
                        flower_image,
                        (
                            tube.centerx - flower_image.get_width() // 2 + x_offset_flower + x_translation,
                            tube.y + y_offset - 160 + more_y_offset + y_translation
                        )
                    )
                    y_offset -= flower_image.get_height() - 183

        # Display the "solved" message on temp_surface
        if solved:
            congrats_text = font.render("¡Ganaste!", True, BLACK)
            temp_surface.blit(
                congrats_text,
                (
                    screen_width // 2 - congrats_text.get_width() // 2,
                    screen_height // 2 - congrats_text.get_height() // 2
                )
            )

        # Draw Lives Display
        lives_position = (20, 20)  # Top-left corner
        if heart_image:
            # Display heart icons
            for life in range(vidas[0]):
                temp_surface.blit(heart_image, (lives_position[0] + life * (heart_image.get_width() - 30), lives_position[1]))
        else:
            # Fallback to text display
            lives_text = font.render(f"Vidas: {vidas[0]}", True, BLACK)
            temp_surface.blit(lives_text, lives_position)

        # Draw the Retry Button
        mouse_pos = pygame.mouse.get_pos()
        if retry_button_rect.collidepoint(mouse_pos):
            button_color = retry_button_hover_color
        else:
            button_color = retry_button_color

        # Draw the button on temp_surface
        pygame.draw.rect(temp_surface, button_color, retry_button_rect)
        retry_text = retry_button_font.render(retry_button_text, True, BLACK)
        retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
        temp_surface.blit(retry_text, retry_text_rect)

        # Apply shaking offset and blit temp_surface to the main screen
        screen.blit(temp_surface, (offset_x, offset_y))
        pygame.display.flip()
