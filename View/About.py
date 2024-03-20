import string
from Support.input import *
from Support.settings import screen_width, screen_height, scale
from UI.button import Button
from UI.slider import Slider
from jorcademy import *


to_main_menu_button = Button(
    (screen_width / 2, screen_height / 2 + 180 * scale),  # Adjust position as needed
    280, 50,  # Button size
    "BACK TO MAIN MENU", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)


# Setting components
setting_components = [to_main_menu_button]
setting_component_index = None
switching_delay = 30
switching_timer = 0


def show_about_screen(main_menu_music) -> string:
    global view_displayed_prev_frame, \
        setting_components, \
        setting_component_index, \
        switching_timer

    # Show backdrop
    backdrop((255, 255, 255))

    # Show title
    text("ABOUT", int(scale * 50), (0, 0, 0),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")

    starting_messages = [
        "Link!! Multiverse Mario",
        "Game Development - Semester 232",
        "Nguyen Huu Hieu",
        "Name",
        "Name"
    ]


    # Show correct message
    # text(starting_messages[0],
    #      int(scale * 20),
    #      (0, 0, 0),
    #      screen_width / 2,
    #      250,
    #      "fonts/pixel.ttf")
    # text(starting_messages[1],
    #      int(scale * 20),
    #      (0, 0, 0),
    #      screen_width / 2,
    #      350,
    #      "fonts/pixel.ttf")
    for i in range(0, len(starting_messages)):
        text(starting_messages[i],
         int(scale * 20),
         (0, 0, 0),
         screen_width / 2,
         250 + 70 * i,
         "fonts/pixel.ttf")
    # Show to main menu button
    to_main_menu_button.draw()
    to_main_menu_button.update()


    # Go to main menu when button is clicked
    if to_main_menu_button.clicked():
        view_displayed_prev_frame = False
        return "MAIN_MENU"

    # De-activate settings screen
    if is_key_down("esc"):
        view_displayed_prev_frame = False
        return "MAIN_MENU"

    return "ABOUT"
