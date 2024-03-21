import string
from Support.settings import scale, screen_width, screen_height
from Support.input import *
from jorcademy import *

switch_starting_message_timer = 0
starting_message_delay = 300
starting_message_index = 0
skip_allowed = True


def show_starting_messages() -> string:
    global switch_starting_message_timer, \
        starting_message_index, \
        skip_allowed

    # Starting messages to show
    starting_messages = [
        "The Princess has been captured by an awful monster".upper(),
        "As an honorable knight, it is your duty to save her".upper(),
        "The retro-verse is full of dangerous creatures".upper(),
        "Be careful. And good luck".upper()
    ]

    # Draw backdrop
    backdrop((255, 255, 255))

    # Toggle skip allowed
    if not skip_key_pressed():
        skip_allowed = True

    # Show correct message
    text(starting_messages[starting_message_index],
         int(scale * 20),
         (0, 0, 0),
         screen_width / 2,
         screen_height / 2,
         "fonts/pixel.ttf")

    # Show skip option
    text("PRESS SPACE TO SKIP",
         int(scale * 15),
         (150, 150, 150),
         screen_width / 2,
         screen_height - 30 * scale,
         "fonts/pixel.ttf")

    # Update timer
    switch_starting_message_timer += 1

    # Switch to next message
    if (switch_starting_message_timer >= starting_message_delay or
            skip_key_pressed() and
            skip_allowed):
        skip_allowed = False
        if starting_message_index >= len(starting_messages) - 1:
            starting_message_index = 0
            return "CONTROLS"

        # Reset timer & change index
        starting_message_index += 1
        switch_starting_message_timer = 0

    return "STARTING_MESSAGES"
