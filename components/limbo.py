import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)
TUBE_COLOR = (0, 0, 255)

BALL_RADIUS = 20
TUBE_WIDTH = 60
TUBE_HEIGHT = 20
FALL_SPEED = 5  # Speed at which the ball falls

def limbo(screen, font, goBack, tubitos):
    screen_width, screen_height = screen.get_size()

    # Initial positions
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_moving_left = False
    ball_falling = False

    tube_x = (screen_width - TUBE_WIDTH) // 2
    tube_y = screen_height - 100

    def move_ball():
        nonlocal ball_x, ball_moving_left
        if ball_moving_left:
            ball_x -= 5
            if ball_x - BALL_RADIUS <= 0:
                ball_moving_left = False
        else:
            ball_x += 5
            if ball_x + BALL_RADIUS >= screen_width:
                ball_moving_left = True

    def trigger_ball_fall():
        nonlocal ball_falling
        ball_falling = True

    def check_win_or_lose():
        nonlocal ball_y
        # Check if the ball has reached the tube level
        if ball_y + BALL_RADIUS >= tube_y:
            if tube_x <= ball_x <= tube_x + TUBE_WIDTH:
                won_text = font.render("Ganaste, tendrás otra oportunidad", True, BLACK)
                screen.blit(won_text, (screen_width // 2 - won_text.get_width() // 2, 35))
            else:
                lost_text = font.render("Perdiste", True, BLACK)
                screen.blit(lost_text, (screen_width // 2 - lost_text.get_width() // 2, 35))

    # Event loop and ball movement logic
    running = True
    while running:
        screen.fill(WHITE)

        # Drawing "Limbo" text at the top
        limbo_text = font.render("Limbo", True, BLACK)
        screen.blit(limbo_text, (screen_width // 2 - limbo_text.get_width() // 2, 20))

        # Move the ball if it's not falling
        if not ball_falling:
            move_ball()

        # Draw the moving ball
        pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)

        # Ball falling logic
        if ball_falling:
            ball_y += FALL_SPEED
            if ball_y + BALL_RADIUS >= screen_height:  # Ball hits the bottom
                check_win_or_lose()

        # Draw the tube
        pygame.draw.rect(screen, TUBE_COLOR, (tube_x, tube_y, TUBE_WIDTH, TUBE_HEIGHT))

        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press space to drop the ball
                    trigger_ball_fall()

        # Frame rate control
        pygame.time.Clock().tick(60)

