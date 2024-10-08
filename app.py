import pygame
from screens.basic_easy_mode import basic_easy_mode
from screens.basic_hard_mode import basic_hard_mode
from screens.basic_normal_mode import basic_normal_mode
from screens.main_menu import main_menu
from screens.reto_hard_mode import reto_hard_mode
from screens.reto_normal_mode import reto_normal_mode
from screens.select_difficulty_basic import select_difficulty_basic
from screens.select_difficulty_reto import select_difficulty_reto
from screens.settings import settings
from screens.game_mode_selection import game_mode_selection
from screens.reto_easy_mode import reto_easy_mode
#from screens.room_selection import room_selection

pygame.init()
original_width, original_height = 2, 1

# Scaled-up window size
scale_factor = 500  # You can adjust this for your needs
scaled_width, scaled_height = original_width * scale_factor, original_height * scale_factor

# Create the window at the scaled-up size
screen = pygame.display.set_mode((scaled_width, scaled_height))

# Create a smaller surface for pixel art resolution
pixel_art_surface = pygame.Surface((original_width, original_height))
# Load the font once
try:
    custom_font = pygame.font.Font('./public/fonts/pixelart.ttf', 18)
except FileNotFoundError:
    print("Custom font not found. Using default font.")
    custom_font = pygame.font.Font(None, 18)  # Fallback to default font

# Initialize clock for FPS control
clock = pygame.time.Clock()

running = True
current_screen = 'main_menu'

def switch_screen(screen_name):
    global current_screen
    current_screen = screen_name

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear the screen with black

    # Draw the current screen
    if current_screen == 'main_menu':
        main_menu(screen, switch_screen, custom_font)
    elif current_screen == 'settings':
        settings(screen, switch_screen, custom_font)
    elif current_screen == 'game_mode_selection':
        game_mode_selection(screen, switch_screen, custom_font)
    elif current_screen == "select_difficulty_basic":
        select_difficulty_basic(screen, switch_screen, custom_font)
    elif current_screen == "basic_easy_mode":
        basic_easy_mode(screen, switch_screen, custom_font)
    elif current_screen == "basic_normal_mode":
        basic_normal_mode(screen, switch_screen, custom_font)
    elif current_screen == "basic_hard_mode":
        basic_hard_mode(screen, switch_screen, custom_font)
    #elif current_screen == "room_selection":
    #    room_selection(screen, switch_screen, custom_font)
    elif current_screen == "reto_easy_mode":
        reto_easy_mode(screen, switch_screen, custom_font)
    elif current_screen == "select_difficulty_reto":
        select_difficulty_reto(screen, switch_screen, custom_font)
    elif current_screen == "reto_normal_mode":
        reto_normal_mode(screen, switch_screen, custom_font)
    elif current_screen == "reto_hard_mode":
        reto_hard_mode(screen, switch_screen, custom_font)
    

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
