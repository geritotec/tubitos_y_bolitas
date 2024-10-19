import pygame

from components.button import draw_button

WHITE = (255, 255, 255)
DARK_GRAY = (100, 100, 100)
GRAY = (200, 200, 200)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

def game_mode_selection(screen, switch_screen, font):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    button_y = screen_height // 3
    total_width = (3 * BUTTON_WIDTH) + (2 * BUTTON_MARGIN)
    button_x = (screen_width - total_width) // 2

    draw_button(screen, 'Normal', button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: start_basic_mode(switch_screen))
    draw_button(screen, 'Dia de muertos', button_x + BUTTON_WIDTH + BUTTON_MARGIN, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: start_time_limit_mode(switch_screen))
    draw_button(screen, 'Multijugador', button_x + 2 * (BUTTON_WIDTH + BUTTON_MARGIN), button_y, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: start_multiplayer_mode(switch_screen))


def start_basic_mode(switch_screen):
    switch_screen("select_difficulty_basic")

def start_time_limit_mode(switch_screen):
    switch_screen("select_difficulty_reto")

def start_multiplayer_mode(switch_screen):
    switch_screen("room_selection")
