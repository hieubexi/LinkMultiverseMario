import string
from Support.input import *
from Support.settings import screen_width, screen_height, scale
from UI.button import Button
from UI.slider import Slider
from engine import *


to_main_menu_button = Button(
    (screen_width / 2, screen_height / 2 + 180 * scale),  # Adjust position as needed
    280, 50,  # Button size
    "BACK TO MAIN MENU", 25, (234, 209, 150),  # Text, font size, text color
    (125, 10, 10),(0, 34, 77),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)


# Setting components
setting_components = [to_main_menu_button]
setting_component_index = None
switching_delay = 30
switching_timer = 0

to_subtitles_delay = 200
to_subtitles_timer = 0

        # Start subtitles
start_subtitles_delay = 600
start_subtitles_timer = 0

        # Switch subtitles
switch_subtitles_delay = 100
switch_subtitles_timer = 0

subtitles_index = 0
def show_subtitles():
    global switch_subtitles_delay
    global to_subtitles_delay 
    global to_subtitles_timer 
    global subtitles_index
            # Start subtitles
    global start_subtitles_delay 
    global start_subtitles_timer 

            # Switch subtitles
    global switch_subtitles_delay 
    global switch_subtitles_timer 
    subtitles = [
        # Ending messages for the game
        ["LINK!!! MULTIVERSE MARIO"],
        ["GAME DEVELOPMENT - SEMESTER 232"],
        ["A GAME BY NGUYEN HUU HIEU"],
        ["THANKS TO MY TEAM:", "THAI TANG HUY - 2013329", "HO TRONG PHUC - 2014159"],
    ]
    # Subtitle properties
    font_size = int(scale * 25)
    text_color = (0, 0, 0)
    text_font = "fonts/pixel.ttf"
    # Calculate starting Y position of the subtitles
    total_subtitles_height = len(subtitles[subtitles_index]) * font_size * scale
    starting_y = (screen_height - total_subtitles_height) / 2  # Calculate starting Y position
    # Draw subtitles
    for i, item in enumerate(subtitles[subtitles_index]):
        text(item,
             font_size,
             text_color,
             screen_width / 2,
             starting_y + i * font_size * scale,
             text_font)
    # Update timer
    switch_subtitles_timer += 1
    # Switch to next subtitle
    if switch_subtitles_timer >= switch_subtitles_delay:
        if subtitles_index >= len(subtitles) - 1:
            subtitles_shown = True
            return
        # Reset timer & change index
        subtitles_index += 1
        switch_subtitles_timer = 0
        
def show_about_screen(main_menu_music) -> string:
    global view_displayed_prev_frame, \
        setting_components, \
        setting_component_index, \
        switching_timer
    main_menu_music.set_volume(0.5 * settings.volume)
    # Show backdrop
    backdrop((255, 255, 255))
    if not skip_key_pressed():
        skip_allowed = True
    # Show title
    text("GAME STORY", int(scale * 50), (125, 10, 10),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")

    starting_messages = [
       "In a world of chaos, Mario is an notorious drunkard".upper(),
       "He doesn't care about the princess.".upper(),
       "When the The Princess has been captured by an awful monster".upper(),
        "Mario only goes to drink instead of rescuing her".upper(),
       "Link - who lost in this world ,fall in love with The Princess".upper(),
       "Thus, Link sets off on a quest to rescue her".upper(),
       "With the powers of Fire Mario and Pacman and himself.".upper(),
       "Kill them all, and save your love...".upper()
    ]

    for i in range(0, len(starting_messages)):
        text(starting_messages[i],
         int( 25) ,
         (0, 34, 77),
         screen_width / 2,
         250 + 40* i,
         "fonts/pixel.ttf")
    
    # show_subtitles()
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
