import pygame


def draw_text_with_shadow(screen, text, font, color, shadow_color, x, y):
    shadow_offset = 2
    shadow = font.render(text, True, shadow_color)
    screen.blit(shadow, (x + shadow_offset, y + shadow_offset))
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
