import string

from Support.input import return_key_pressed
from Support.settings import scale, screen_width, screen_height
from jorcademy import *


def show_controls_screen() -> string:
    backdrop((0, 34, 77,0.5))

    text("CONTROLS", int(scale * 50), (234, 209, 150),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")
    text("MOVE: ARROW KEYS/WAS", int(scale * 30), (234, 209, 150),
         screen_width / 2, screen_height / 2 - 50 * scale,
         "fonts/pixel.ttf")
    text("JUMP: SPACE", int(scale * 30), (234, 209, 150),
         screen_width / 2, screen_height / 2,
         "fonts/pixel.ttf")
    text("ATTACK: SHIFT", int(scale * 30), (234, 209, 150),
         screen_width / 2, screen_height / 2 + 50 * scale,
         "fonts/pixel.ttf")
    text("PAUSE: ESCAPE", int(scale * 30), (234, 209, 150),
         screen_width / 2, screen_height / 2 + 100 * scale,
         "fonts/pixel.ttf")
    text("PRESS ENTER TO START", int(scale * 30), (234, 209, 150),
         screen_width / 2, screen_height / 2 + 200 * scale,
         "fonts/pixel.ttf")

    # Go to game when enter is pressed
    if return_key_pressed():
        return "TRANSITION_FROM_MAIN_MENU"

    return "CONTROLS"
