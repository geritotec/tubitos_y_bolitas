import pygame
from components.button import draw_button

# Define button sizes and colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

def settings(screen, switch_screen, font):
    screen.fill((0, 0, 0))
    draw_button(screen, "Volver", 220, 290, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: switch_screen('main_menu'))
def save_settings():
    pass