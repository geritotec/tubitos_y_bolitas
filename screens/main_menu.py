import pygame

from components.button import draw_button

# Define button sizes and colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20



def main_menu(screen, switch_screen, font):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    button_x = (screen_width - BUTTON_WIDTH) // 2
    button_y = screen_height // 3

    draw_button(screen, 'Jugar', button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: switch_screen('game_mode_selection'))
    draw_button(screen, 'Ajustes', button_x, button_y + BUTTON_HEIGHT + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: switch_screen('settings'))
    draw_button(screen, 'Salir', button_x, button_y + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=pygame.quit)
