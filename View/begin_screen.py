import string

from Support.input import skip_key_pressed
from Support.settings import scale, screen_width, screen_height
from UI.button import Button
from engine import *

quit_button = Button(
    (screen_width / 2, screen_height / 2 + 180 * scale),  # Adjust position as needed
    280, 50,  # Button size
    "QUIT", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)
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
    text("PRESS SPACE TO BEGIN",
         int(scale * 15),
         (255, 255, 255),
         screen_width / 2,
         screen_height - 30 * scale,
         "fonts/pixel.ttf")
    text("ESCAPE TO QUIT",
         int(scale * 15),
         (255, 255, 255),
         screen_width / 2,
         screen_height - 45 * scale,
         "fonts/pixel.ttf")
    # De-activate settings screen
    # quit_button.update()
    # quit_button.draw()
    if is_key_down("esc") or quit_button.clicked():
        pygame.quit()
    
    # Go to game when enter is pressed
    if skip_key_pressed():
        return "MAIN_MENU"

    return "BEGIN_SCREEN"
