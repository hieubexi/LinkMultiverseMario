from typing import Tuple

from Support import settings
from primitives import *

# Game settings
screen_size: tuple = (100, 100)
screen_title: str = "JorCademy Engine"
background_color: tuple = (0, 0, 0)
__draw_buffer: list = []

# Initialize audio component
pygame.mixer.init()

# Create type aliases
color = Tuple[int, int, int]

# ==== Keyboard input ====

__key_status = {}

# === Nintendo Switch controller input ===

__nintendo_switch_button_status = {
    0: False,  # A
    1: False,  # B
    2: False,  # X
    3: False,  # Y
    4: False,  # - (MINUS)
    5: False,  # HOME
    6: False,  # + (PLUS)
    9: False,  # PLUS
    11: False,  # D_UP
    12: False,  # D_DOWN
    13: False,  # D_LEFT
    14: False,  # D_RIGHT
}
__nintendo_switch_joystick = {}


# Get whether a specific key is down
def is_key_down(key: str) -> bool:
    if key in __key_status:
        return __key_status[key]
    else:
        return False


# Get whether a specific Switch button is down


# ==== Mouse input ====
__mouse_status = {}
__scroll_up: bool = False
__scroll_down: bool = False
mouse_position = pygame.Vector2(0, 0)


# Get whether a specific mouse button is down
def is_mouse_button_down(button: str) -> bool:
    if button in __mouse_status:
        return __mouse_status[button]
    else:
        return False


def is_scrolling_up() -> bool:
    return __scroll_up


# Get whether the player is scrolling down
def is_scrolling_down() -> bool:
    return __scroll_down


# Change screen size
def screen(width: int, height: int) -> None:
    global screen_size
    screen_size = (width, height)


# Change screen title
def title(t: str) -> None:
    global screen_title
    screen_title = t


# Change app icon
def icon(name: str) -> None:
    app_icon = pygame.image.load("./assets/" + name)
    pygame.display.set_icon(app_icon)


# Change screen background color
def backdrop(c: color) -> None:
    global background_color
    __draw_buffer.clear()
    background_color = c


# Draw a circle
def ellipse(c: color, x: float, y: float, w: float, h: float, rotation=0) -> None:
    e = Ellipse(c, x, y, w, h, rotation)
    __draw_buffer.append(e)


# Draw a rectangle
def rect(c: color, x: float, y: float, w: float, h: float, rotation=0) -> None:
    r = Rectangle(c, x, y, w, h, rotation)
    __draw_buffer.append(r)


# Draw a string of text
def text(content: str, size: int, c: color, x: float, y: float, font="Nunito", rotation=0) -> None:
    # Fetch font
    try:
        font = pygame.font.Font("./assets/" + font, size)
    except:
        font = pygame.font.SysFont(font, size)

    # Draw font
    text_surface = font.render(content, True, c)
    t = Text(content, text_surface, c, x, y, None, None, size, font, rotation)
    __draw_buffer.append(t)


# Load an image
def load_image(path: str) -> pygame.Surface:
    full_path = "assets/" + path
    try:
        return pygame.image.load(full_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image '{full_path}': {e}")


# Draw an image
def image(surface: pygame.Surface, x: float, y: float, scale: float, flipped=False, rotation=0) -> None:
    i = Image(surface, scale, x, y, flipped, rotation)
    __draw_buffer.append(i)


# Load new sound
def load_sound(path: str):
    sound = Exception
    try:
        sound = pygame.mixer.Sound(path)
    except:
        pass
        # print(f"Error: Audio {path} could not be loaded.")
    return sound


# Play audio
def play_sound(sound, p_volume=1.0):
    try:
        sound.set_volume(p_volume * settings.volume)
        if sound.get_num_channels() == 0:
            pygame.mixer.find_channel().play(sound)
    except:
        pass
        # print("Error: Audio could not be played.")


# Wait for new action
def sleep(msec: int):
    pygame.time.wait(msec)
