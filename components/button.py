import pygame

def draw_button(screen, text, x, y, width, height, color, hover_color, font, action=None):
    # Create a rect for the button
    button_rect = pygame.Rect(x, y, width, height)

    # Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Determine if the mouse is over the button
    is_hovered = button_rect.collidepoint(mouse_pos)

    # Static variable to track if the button was previously pressed
    if not hasattr(draw_button, "was_pressed"):
        draw_button.was_pressed = False

    # Draw the button with hover effect
    if is_hovered:
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    # Render and center the text on the button
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

    # Check if the mouse was released after being pressed
    if is_hovered:
        if mouse_click[0] and not draw_button.was_pressed:  # Mouse press detected
            draw_button.was_pressed = True
        elif not mouse_click[0] and draw_button.was_pressed:  # Mouse release detected
            draw_button.was_pressed = False
            if action:
                action()