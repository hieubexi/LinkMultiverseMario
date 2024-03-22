import string
from Support.input import *
import Support.settings 
from Support.settings import screen_width, screen_height, scale
from UI.button import Button

from jorcademy import *
to_main_menu_button = Button(
    (screen_width / 2, screen_height / 2.2 + 220 * scale),  # Adjust position as needed
    280, 50,  # Button size
    "BACK TO MAIN MENU", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)
world_1_1 = Button(
    (screen_width / 4, 168 + 70),  # Adjust position as needed
    280, 50,  # Button size
    "WORLD 1_1", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)
world_1_2 = Button(
    ( 3* screen_width / 4, 168 + 70),  # Adjust position as needed
    280, 50,  # Button size
    "WORLD 1_2", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)
world_1_3 = Button(
    (screen_width / 4, 168 + 70*3),  # Adjust position as needed
    280, 50,  # Button size
    "WORLD 1_3", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)
world_1_4= Button(
    (3* screen_width / 4, 168 + 70*3),  # Adjust position as needed
    280, 50,  # Button size
    "WORLD 1_4", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)
world_1_5 = Button(
    (screen_width / 4, 168 + 70*5),  # Adjust position as needed
    280, 50,  # Button size
    "WORLD 1_5", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)

world_boss = Button(
    (3*screen_width / 4, 168 + 70*5),  # Adjust position as needed
    280, 50,  # Button size
    "THE BOSS", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)
view_displayed_prev_frame = False

# Setting components
level_components = [world_1_1,world_1_2 ,world_1_3,world_1_4,world_1_5,world_boss, to_main_menu_button]
level_component_index = None
switching_delay = 30    
switching_timer = 0



def increase_selected_component_index():
    global level_component_index
    if level_component_index is None:
        level_component_index = 0
    else:
        if level_component_index == len(level_components) - 1:
            level_component_index = 0
        else:
            level_component_index += 1



def decrease_selected_component_index():
    global level_component_index
    if level_component_index is None:
        level_component_index = len(level_components) - 1
    else:
        if level_component_index == 0:
            level_component_index = len(level_components) - 1
        else:
            level_component_index -= 1


def show_level_screen(main_menu_music) -> string:
    global view_displayed_prev_frame, \
        level_components, \
        level_component_index, \
        switching_timer, \
        choose

    # Show backdrop
    backdrop((255, 255, 255))

    # Manage selected component
    for i in range(len(level_components)):
        if level_component_index == i:
            level_components[i].selected = True
        else:
            level_components[i].selected = False

    # Show title
    text("CHOOSE WORLD", int(scale * 50), (0, 0, 0),
         screen_width / 2, screen_height / 2.2 - 150 * scale,
         "fonts/pixel.ttf")


    # Show to main menu button
    to_main_menu_button.draw()
    to_main_menu_button.update()
    # draw world 1
    world_1_1.draw()
    world_1_1.update()
    # draw world 2
    world_1_2.draw()
    world_1_2.update()
    # draw world 3
    world_1_3.draw()
    world_1_3.update()
    # draw world 4
    world_1_4.draw()
    world_1_4.update()
    # draw world 5
    world_1_5.draw()
    world_1_5.update()
    # draw world boss
    world_boss.draw()
    world_boss.update()

    # Go to main menu when button is clicked
    if to_main_menu_button.clicked():
        view_displayed_prev_frame = False
        return "MAIN_MENU"
    if world_1_1.clicked():
        Support.settings.active_level = 0
        return "STARTING_MESSAGES"
    elif world_1_2.clicked():
        Support.settings.active_level = 1
        return "STARTING_MESSAGES"
    elif world_1_3.clicked():
        Support.settings.active_level = 2
        return "STARTING_MESSAGES"
    elif world_1_4.clicked():
        Support.settings.active_level = 3
        return "STARTING_MESSAGES"
    elif world_1_5.clicked():
        Support.settings.active_level = 4
        return "STARTING_MESSAGES"
    elif world_boss.clicked():
        Support.settings.active_level = 5
        return "STARTING_MESSAGES"
    # De-activate settings screen
    if is_key_down("esc"):
        view_displayed_prev_frame = False
        return "MAIN_MENU"

    return "CHOOSE_LEVEL"
