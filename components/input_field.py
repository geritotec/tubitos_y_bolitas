import pygame

def draw_input(screen, text_var, x, y, width, height, color, border_color, focused_border_color, font):
    # Create a rect for the input field
    input_rect = pygame.Rect(x, y, width, height)

    # Get the current mouse position and clicks
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Determine if the mouse is over the input field
    is_hovered = input_rect.collidepoint(mouse_pos)

    # Static variables to track focus and key states
    if not hasattr(draw_input, "was_focused"):
        draw_input.was_focused = False
    if not hasattr(draw_input, "key_states"):
        draw_input.key_states = {}

    # Change the border color based on focus state
    current_border_color = focused_border_color if draw_input.was_focused else border_color

    # Draw the input field with border
    pygame.draw.rect(screen, color, input_rect)
    pygame.draw.rect(screen, current_border_color, input_rect, 2)

    # Render and center the text inside the input field
    text_surf = font.render(text_var[0], True, (255, 255, 255))
    text_rect = text_surf.get_rect(topleft=(x + 5, y + (height - text_surf.get_height()) // 2))
    screen.blit(text_surf, text_rect)

    # Focus management
    if mouse_click[0]:  # Mouse press detected
        if is_hovered:
            draw_input.was_focused = True
        else:
            draw_input.was_focused = False

    # Handle input when the field is focused
    if draw_input.was_focused:
        keys = pygame.key.get_pressed()

        # Loop through all possible keys and check their state
        for key in range(len(keys)):
            if keys[key]:
                if key not in draw_input.key_states or not draw_input.key_states[key]:  # Detect key press
                    draw_input.key_states[key] = True
            else:
                if key in draw_input.key_states and draw_input.key_states[key]:  # Detect key release
                    draw_input.key_states[key] = False

                    # Handle key releases here
                    if key == pygame.K_BACKSPACE:
                        text_var[0] = text_var[0][:-1]  # Remove last character
                    elif key == pygame.K_RETURN:
                        pass  # Optionally handle Enter key
                    elif key == pygame.K_ESCAPE:
                        pass  # Optionally handle Escape key
                    elif key == pygame.K_TAB:
                        pass  # Optionally handle Tab key
                    elif key == pygame.K_SPACE:
                        pass
                    else:
                        char = pygame.key.name(key)
                        if char.isalnum():  # Only add valid alphanumeric characters
                            text_var[0] += char

