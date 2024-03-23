import string

from Support.input import return_key_pressed
from Support.settings import scale, screen_width, screen_height
from UI.button import Button
from engine import *

to_main_menu_button = Button(
    (screen_width / 2, screen_height / 2 + 180 * scale),  # Adjust position as needed
    280, 50,  # Button size
    "BACK TO MAIN MENU", 25, (234, 209, 150),  # Text, font size, text color
    (125, 10, 10),(0, 34, 77),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)


def show_controls_screen(main_menu_music) -> string:
     backdrop((255,255,255))
     main_menu_music.set_volume(0.5 * settings.volume)

     text("CONTROLS", int(scale * 50), (125, 10, 10),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")
     text("MOVE: ARROW KEYS/WAS", int(scale * 30), (0, 34, 77),
         screen_width / 2, screen_height / 2 - 80 * scale,
         "fonts/pixel.ttf")
     text("JUMP: SPACE", int(scale * 30), (0, 34, 77),
         screen_width / 2, screen_height / 2 - 30 * scale,
         "fonts/pixel.ttf")
     text("ATTACK: SHIFT", int(scale * 30), (0, 34, 77),
         screen_width / 2, screen_height / 2 + 20 * scale,
         "fonts/pixel.ttf")
     text("PAUSE: ESCAPE", int(scale * 30), (0, 34, 77),
         screen_width / 2, screen_height / 2 + 70 * scale,
         "fonts/pixel.ttf")
#     text("PRESS ENTER TO START", int(scale * 30), (0, 0, 0),
#          screen_width / 2, screen_height / 2 + 200 * scale,
#          "fonts/pixel.ttf")
    
     to_main_menu_button.update()
     to_main_menu_button.draw()
     if to_main_menu_button.clicked():
        view_displayed_prev_frame = False
        return "MAIN_MENU"

    # De-activate settings screen
     if is_key_down("esc"):
          view_displayed_prev_frame = False
          return "MAIN_MENU"
    # Go to game when enter is pressed
     if return_key_pressed():
          return "TRANSITION_FROM_MAIN_MENU"

     return "CONTROLS"
