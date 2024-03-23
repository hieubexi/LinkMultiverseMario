import string

from Support.input import skip_key_pressed
from Support.settings import scale, screen_width, screen_height
from UI.button import Button
from engine import *

quit_button = Button(
    (screen_width / 2, screen_height- 20 * scale),  # Adjust position as needed
    80, 25,  # Button size
    "QUIT", 20, (234, 209, 150),
    (125, 10, 10), (0, 34, 77),
    True, 5, (200, 200, 200))# Rounded corners, border size, border color




menu_backdrop = None
main_menu_music = load_sound("assets/music/main_menu.ogg")
def load_main_menu_images():
    global menu_backdrop, logo
    menu_backdrop = load_image("other/bg_1.png")

def show_begin_screen() -> string:
    backdrop((255,255,255))
    if not main_menu_music.get_num_channels() > 0:
        main_menu_music.play(-1)
        main_menu_music.set_volume(0.5 * settings.volume)
#     text("PRESS SPACE TO START", int(scale * 30), (0, 0, 0),
#          screen_width / 2, screen_height / 2 + 200 * scale,
#          "fonts/pixel.ttf")
    image(menu_backdrop,
          screen_width / 2,
          screen_height / 2,
          1.0)
    text("Press SPACE to begin",
         int(scale * 15),
         (255, 255, 255),
         screen_width / 2,
         screen_height  - 40* scale ,
         "fonts/pixel.ttf")
    text("\'Q\' to Quit game",
         int(scale * 15),
         (255, 255, 255),
         screen_width / 2,
         screen_height  - 20* scale ,
         "fonts/pixel.ttf")

    # De-activate settings screen
    # quit_button.update()
    # quit_button.draw()
    # if quit_button.clicked():
    if is_key_down("q"):        
        pygame.quit()
    
    # Go to game when enter is pressed
    if skip_key_pressed():
        return "MAIN_MENU"

    return "BEGIN_SCREEN"
