import string
from Support.settings import screen_width, screen_height, scale
from Support.input import *
from UI.button import Button
from jorcademy import *

pause_button = Button(
    (screen_width / 2, screen_height / 3 + 50  ),
    300, 50,
    "GO TO MAIN MENU", 
    content_size=30,
    content_color=(234, 209, 150),
    button_color=(125, 10, 10), 
    hover_color=(0, 34, 77),
    border=False)

continue_button = Button(
    (screen_width / 2, screen_height / 3 + 120 + 30 ),
    300, 50,
    "CONTINUE",     
    content_size=30,
    content_color=(234, 209, 150),
    button_color=(125, 10, 10), 
    hover_color=(0, 34, 77),
    border=False)

restart_button = Button(
    (screen_width / 2, screen_height / 3 + 190 + 60 ),
    300, 50,
    "RESTART",     
    content_size=30,
    content_color=(234, 209, 150),
    button_color=(125, 10, 10), 
    hover_color=(0, 34, 77),
    border=False)

pause_screen_delay = 30
pause_screen_timer = 0


def show_paused_screen(active_level) -> string:
    global pause_screen_timer
    text("PAUSE", int(scale * 50),(255,255,255),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")


    # button generate
    pause_button.update()
    pause_button.draw()
    continue_button.update()
    continue_button.draw()
    restart_button.update()
    restart_button.draw()
    # Check if user clicked on start new game
    if pause_button.clicked():
        active_level.level_music.fadeout(500)
        return "MAIN_MENU"

    if (pause_key_pressed() or continue_button.clicked()) and pause_screen_timer >= pause_screen_delay:
        pause_screen_timer = 0
        return "GAME"

    pause_screen_timer += 1
    return "PAUSED"
