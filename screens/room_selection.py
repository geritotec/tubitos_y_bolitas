import pygame
import socketio  # Import SocketIO client
from components.button import draw_button
from components.input_field import draw_input
from utilities.mover_bolita import mover_bolita

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0,0,0)
DARK_GRAY = (100, 100, 100)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
BALL_RADIUS = 15
TUBE_WIDTH, TUBE_HEIGHT = 40, 180
TUBE_MARGIN = 15

input_text = [""]
sio = socketio.Client()
game_state_dict = {}
selected_tube = None
difficulty = 1

def connect_socket():
    try:
        sio.connect('http://10.49.187.179:5000')
        print('Connecting to server...')
        join_room()
    except Exception as e:
        print(f"Connection error: {e}")

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def game_state(data):
    global game_state_dict
    game_state_dict = data

def set_difficulty(difficulty):
    create_level(difficulty)

def create_level(difficulty):
    if sio.connected:
        sio.emit("create_level", {"difficulty": difficulty, "room_id": input_text[0]})
    else:
        print("SocketIO is not connected.")

def room_selection(screen, switch_screen, font):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    button_y = screen_height // 3
    total_width = (3 * BUTTON_WIDTH) + (2 * BUTTON_MARGIN)
    button_x = (screen_width - total_width) // 2

    if not sio.connected:
        screen.fill((0, 0, 0))
        draw_input(screen, input_text, 220, 210, BUTTON_WIDTH, BUTTON_HEIGHT, (0, 0, 0), WHITE, (255, 99, 71), font)
        draw_button(screen, "Enter", 220, 290, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=connect_socket)
    elif sio.connected and not game_state_dict:
        draw_button(screen, 'Easy', button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: set_difficulty(1))
        draw_button(screen, 'Normal', button_x + BUTTON_WIDTH + BUTTON_MARGIN, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: set_difficulty(2))
        draw_button(screen, 'Hard', button_x + 2 * (BUTTON_WIDTH + BUTTON_MARGIN), button_y, BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, GRAY, font, action=lambda: set_difficulty(3))
    elif sio.connected and game_state_dict:
        render_game(screen, font)


def join_room():
    room_id = input_text[0]
    if room_id:
        if sio.connected:
            sio.emit("join_game", {"room_id": room_id})
        else:
            print("SocketIO is not connected.")

def render_game(screen, font):
    screen.fill(WHITE)
    
    tubitos = game_state_dict.get("tubitos", [])
    if not tubitos:
        return

    screen_width, screen_height = pygame.display.get_surface().get_size()
    tubes = [pygame.Rect(TUBE_MARGIN + i * (TUBE_WIDTH + TUBE_MARGIN), screen_height // 2 - TUBE_HEIGHT // 2, TUBE_WIDTH, TUBE_HEIGHT) for i in range(len(tubitos))]
    
    color_map = {
        "rosa": (255, 192, 203),
        "amarillo": (255, 255, 0),
        "aqua": (0, 255, 255),
        "naranja": (255, 165, 0),
        "morado": (128, 0, 128),
        "checker_blanco": (200, 200, 200),
        "checker_aqua": (0, 200, 255),
        "checker_rosa": (255, 182, 193),
        "checker_naranja": (255, 140, 0)
    }

    for i, tube in enumerate(tubes):
        pygame.draw.rect(screen, GRAY, tube, 2)
        y_offset = TUBE_HEIGHT - BALL_RADIUS * 2
        for ball_color in tubitos[i]:
            if ball_color != "nada":
                color = color_map.get(ball_color, BLACK)
                pygame.draw.circle(screen, color, (tube.centerx, tube.y + y_offset), BALL_RADIUS)
                y_offset -= BALL_RADIUS * 2 + 10

    if game_state_dict.get("solved", "false") == "true":
        congrats_text = font.render("You Won!", True, BLACK)
        screen.blit(congrats_text, (screen_width // 2 - congrats_text.get_width() // 2, screen_height // 2 - congrats_text.get_height() // 2))

    pygame.display.flip()

    handle_mouse_input()  # Handle mouse input here

def handle_mouse_input():
    global selected_tube

    # Static variable to track if the mouse button was previously pressed
    if not hasattr(handle_mouse_input, "was_pressed"):
        handle_mouse_input.was_pressed = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if game_state_dict.get("solved", "false") == "false":
        # Check for mouse press
        if mouse_click[0] and not handle_mouse_input.was_pressed:  # Mouse press detected
            handle_mouse_input.was_pressed = True
            tubes = [pygame.Rect(TUBE_MARGIN + i * (TUBE_WIDTH + TUBE_MARGIN), pygame.display.get_surface().get_height() // 2 - TUBE_HEIGHT // 2, TUBE_WIDTH, TUBE_HEIGHT) for i in range(len(game_state_dict.get("tubitos", [])))]
            for i, tube in enumerate(tubes):
                if tube.collidepoint(mouse_pos):
                    print(f"Click detected on tube {i}")
                    if selected_tube is None:
                        if any(ball != "nada" for ball in game_state_dict["tubitos"][i]):
                            selected_tube = i
                    else:
                        if mover_bolita(game_state_dict["tubitos"], selected_tube, i):
                            print(f"Emitting move for tube {i}")
                            sio.emit("mover_volita", {"room_id": input_text[0], "source_index": selected_tube, "destination_index": i})
                            if check_solved():
                                sio.emit("solved", {"room_id": input_text[0]})
                        selected_tube = None

        # Check for mouse release
        elif not mouse_click[0] and handle_mouse_input.was_pressed:  # Mouse release detected
            handle_mouse_input.was_pressed = False


def check_solved():
    for tube in game_state_dict.get("tubitos", []):
        if len(set(tube)) != 1 and tube.count("nada") != 4:
            return False
    return True

