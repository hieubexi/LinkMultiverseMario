from Support.settings import scale, screen_height, screen_width
from engine import *

# Transition properties
transition_time = 60 * 3
transition_timer = transition_time

# Images
link_image = None


def load_transition_screen_images() -> None:
    global link_image
    link_image = load_image('link/link_idle.png')


# Get next level index
def get_next_level_index(active_level, levels) -> int:
    active_level_index = levels.index(active_level)
    if active_level_index == (len(levels) - 1):
        return 0
    else:
        return active_level_index + 1


# Get name of the current level (might be different from active level)
def get_current_level_name(current_screen, active_level, levels) -> int:
    if active_level.link.killed or current_screen == "TRANSITION_FROM_MAIN_MENU":
        return active_level.level_name
        # return levels[get_next_level_index(active_level, levels)].level_name
    else:
        return levels[get_next_level_index(active_level, levels)].level_name


def show_transition_screen(active_level, levels, current_screen):
    global transition_timer, transition_time

    # Stop music from current level
    try:
        active_level.level_music.fadeout(500)
    except:
        print("No music to fade out")

    # Set backdrop to black
    backdrop((0, 0, 0))
    if get_current_level_name(current_screen, active_level, levels) == "END":
        text("C'mon, You finished your quest",
            int(40 ),
            (255, 255, 255),
            screen_width / 2 ,
            screen_height / 2 - 220,
            "fonts/pixel.ttf")
        text("Give you Princess a kiss",
            int(40 ),
            (255, 255, 255),
            screen_width / 2 ,
            screen_height / 2 - 150,
            "fonts/pixel.ttf")
        image(link_image, screen_width / 2, screen_height / 2, 2 * scale)
        
    # Display properties on screen
    else:
        text(f"x{active_level.link.lives}",
            int(40 * scale),
            (255, 255, 255),
            screen_width / 2 + 30 * scale,
            screen_height / 2,
            "fonts/pixel.ttf")
        text(f"WORLD {get_current_level_name(current_screen, active_level, levels)}",
            int(30 * scale),
            (255, 255, 255),
            screen_width / 2,
            30 * scale,
            "fonts/pixel.ttf")
        image(link_image, screen_width / 2 - 40 * scale, screen_height / 2, 2 * scale)

    # Reset level if timer is over
    if transition_timer <= 0:
        transition_timer = transition_time
        return "GAME"

    transition_timer -= 1
    return current_screen
