import string
from Support.settings import screen_width, screen_height, scale
from Support.input import *
from UI.button import Button
from View.begin_screen import main_menu_music
# UI components
start_button = Button(
    pos=(screen_width/2, screen_height / 2 - 70 * scale),
    w=275, 
    h=50,
    content="START NEW GAME", 
    content_size=30, 
    content_color=(234, 209, 150),
    button_color=(125, 10, 10), 
    hover_color=(0, 34, 77),
    border=True, border_size=5, border_color=(200, 200, 200) )

settings_button = Button(
    pos=(screen_width/2, screen_height / 2 - 0 * scale ),
    w=275, 
    h=50,
    content="SETTINGS", 
    content_size=30,
    content_color=(234, 209, 150),
    button_color=(125, 10, 10), 
    hover_color=(0, 34, 77),
    border=True, border_size=5, border_color=(200, 200, 200) )
about_button = Button(
    pos=(screen_width/2, screen_height / 2 + 70*scale),
    w=275, 
    h=50,
    content="GAME STORY", 
    content_size=30, 
    content_color=(234, 209, 150),
    button_color=(125, 10, 10), 
    hover_color=(0, 34, 77),
    border=True, border_size=5, border_color=(200, 200, 200) )
controls_button = Button(
    pos=(screen_width/2, screen_height / 2 + 140 * scale),
    w=275, 
    h=50,
    content="CONTROL", 
    content_size=30, 
    content_color=(234, 209, 150),
    button_color=(125, 10, 10), 
    hover_color=(0, 34, 77),
    border=True, border_size=5, border_color=(200, 200, 200) )


menu_buttons = [start_button, settings_button, about_button,controls_button]
selected_index = None

# Music
# main_menu_music = load_sound("assets/music/main_menu.ogg")

# Images
menu_backdrop = None
logo = None

def decrease_selected_button_index():
    global selected_index
    if selected_index is None:
        selected_index = 0
    elif selected_index > 0:
        selected_index -= 1


def increase_selected_button_index():
    global selected_index
    if selected_index is None:
        selected_index = 0
    elif selected_index < len(menu_buttons) - 1:
        selected_index += 1

def show_main_menu_screen(active_level) -> string:
    global selected_index
    global main_menu_music
    # Stop music in active level
    active_level.level_music.fadeout(500)
    main_menu_music.set_volume(0.5 * settings.volume)
    # Play music
    # if not main_menu_music.get_num_channels() > 0:
    #     main_menu_music.play(-1)
    #     main_menu_music.set_volume(0.5 * settings.volume)

    # Draw menu
    backdrop((255, 255, 255))
    # image(menu_backdrop,
    #       screen_width / 2,
    #       screen_height / 2,
    #       1.0)

    # rect((234, 209, 150),screen_width / 2,0 ,screen_width,442)
    text("MAIN MENU", int(scale * 50), (125, 10, 10),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")



    # Determine selected button
    if selected_index is not None:
        for i in range(len(menu_buttons)):
            if i == selected_index:
                menu_buttons[i].selected = True
            else:
                menu_buttons[i].selected = False

    # Update start button
    start_button.update()
    start_button.draw()

    # Update settings button
    settings_button.update()
    settings_button.draw()

    # Update about button
    about_button.update()
    about_button.draw()

    # Update level button
    controls_button.update()
    controls_button.draw()
    # Check if user clicked on start new game
    if start_button.clicked():
        active_level.link.hard_reset()
        active_level.reset()
        return "CHOOSE_LEVEL"
        # return "STARTING_MESSAGES"

    # Check if user clicked on settings
    if settings_button.clicked():
        return "SETTINGS"
    elif about_button.clicked():
        return "ABOUT"
    elif controls_button.clicked():
        return "CONTROLS"
    if is_key_down("esc") :
        return "BEGIN_SCREEN"
    return "MAIN_MENU"
