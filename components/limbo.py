import pygame, sys
from components.text_shadow import draw_text_with_shadow
from components.button import draw_button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)
TUBE_COLOR = (0, 0, 255)

BALL_RADIUS = 20
TUBE_WIDTH = 60
TUBE_HEIGHT = 20
FALL_SPEED = 5  # Speed at which the ball falls


def draw_translucent_rect(screen, color, rect, opacity):
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    surface.fill((*color, opacity)) 
    screen.blit(surface, rect.topleft)


def limbo(screen, switch_screen, font, screen_width, screen_height, actual, vidas):

    background = pygame.image.load('static/luna_bien.jpeg')  
    mariachi_img = pygame.image.load('static/mariachihum.png')  
    game_over_img = pygame.image.load('static/final.jpg')  
    cursor_img = pygame.transform.scale(mariachi_img, (40, 50))  

    background = pygame.transform.scale(background, (screen_width, screen_height))
    mariachi_img = pygame.transform.scale(mariachi_img, (60, 70)) 
    game_over_img = pygame.transform.scale(game_over_img, (screen_width, 200))  

    bar_width, bar_height = 500, 50
    bar_x, bar_y = (screen_width - bar_width) // 2, (screen_height - bar_height) // 2

    cursor_width, cursor_height = 40, 50 
    cursor_x = bar_x
    cursor_speed = 10  

    hit_zone_left = bar_x + bar_width // 4
    hit_zone_right = hit_zone_left + bar_width // 7

    red_bar_width = bar_width // 7
    red_bar_x = bar_x + bar_width // 4 

    font = pygame.font.SysFont(None, 40)
    font_large = pygame.font.SysFont(None, 80)

    hit = False
    lives = 3 
    game_over = False
    congratulations = False
    message = ""  



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not game_over:
                if hit_zone_left < cursor_x < hit_zone_right:
                    hit = True
                    congratulations = True  

                else:
                    hit = False
                    lives -= 1 
                    message = "¡Miss!" 

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (screen_width // 2 - 50 < mouse_x < screen_width // 2 + 50) and (screen_height // 2 + 40 < mouse_y < screen_height // 2 + 80):
                    print("Volver al menú") 
                    pygame.mouse.set_visible(True) 
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.cursors.compile(pygame.image.tostring(cursor_img, "RGBA"))))


        screen.blit(background, (0, 0))

        if not game_over:
            if not congratulations:
                draw_translucent_rect(screen, (255, 255, 255), pygame.Rect(bar_x, bar_y, bar_width, bar_height), 180)  
                
                draw_translucent_rect(screen, (255, 0, 0), pygame.Rect(red_bar_x, bar_y, red_bar_width, bar_height), 180) 
                
                screen.blit(mariachi_img, (cursor_x, bar_y))

                cursor_x += cursor_speed
                if cursor_x > bar_x + bar_width - cursor_width or cursor_x < bar_x:
                    cursor_speed *= -1

                if message:
                    message_color = (255, 255, 0) if message == "¡Fallaste!" else (255, 255, 255)  
                    draw_text_with_shadow(screen, message, font, message_color, (100, 100, 100), screen_width // 2 - 40, screen_height - 70)

                draw_text_with_shadow(screen, f"Lives: {lives}", font, (255, 255, 255), (100, 100, 100), 20, 20)

                if lives <= 0:
                    game_over = True
            else:
                actual[0] = "main_game"
                return
        else:
            screen.blit(game_over_img, (0, 0))
            draw_text_with_shadow(screen, "Game Over", font_large, (0, 255, 255), (0, 0, 0), screen_width // 2 - 150, screen_height // 2 - 40)
            draw_button(screen, "Menu", screen_width // 2 - 50, screen_height // 2 + 40, 100, 40, TUBE_COLOR, WHITE, font, action=lambda:menu(switch_screen))

        pygame.display.update()

        pygame.time.Clock().tick(60)

def menu(switch_screen):
    switch_screen("main_menu")