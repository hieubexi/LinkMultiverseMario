from GameObject.Monster.ganondorf import Ganondorf
from Level.boss_level import BossLevel
from Level.endscene import EndScene
from Level.level import Level
import Support.settings 
import View.choose_level
# Support
from Support.settings import screen_width, screen_height
from Support.input import *
import Support.input as inp

# Screens
from View import main_menu_screen
from View.controls_screen import show_controls_screen
from View.game_over_screen import show_game_over_screen
from View.main_menu_screen import show_main_menu_screen
from View.pause_screen import show_paused_screen
from View.settings_screen import show_settings_screen

from View.About import show_about_screen
from View.choose_level import show_level_screen
# from View.choose_level import choose
from View.starting_messages_screen import show_starting_messages
from View.transition_screen import get_next_level_index, show_transition_screen
# from Support.settings  import active_level_index
from jorcademy import *

current_screen = "MAIN_MENU"
transition_screens = [
    "TRANSITION_FROM_MAIN_MENU",
    "TRANSITION",
    "CONTROLS",
    "STARTING_MESSAGES"
]

# Levels
levels = []
# active_level_index = first_level
# Transition properties
last_recorded_score = 0
Support.settings.initLevel()
# View.choose_level.get_level()
active_level_index = Support.settings.active_level
# Additional timers
pause_cooldown = 30
pause_timer = 0


# Update game timers
def update_timers() -> None:
    global pause_timer

    # Update pause timer
    if pause_timer > 0:
        pause_timer -= 1


# Activate next level
def activate_next_level() -> None:
    global active_level_index
    global last_recorded_score
    stored_link = levels[active_level_index].link
    active_level_index = get_next_level_index(levels[active_level_index], levels)

    # Initialize new level
    levels[active_level_index].init_link(stored_link)
    levels[active_level_index].clouds_enabled = settings.clouds
    levels[active_level_index].reset()


def process_transition_game() -> None:
    global current_screen, active_level_index

    # Show starting message when transitioning from main menu
    if current_screen == "STARTING_MESSAGES":
        current_screen = show_starting_messages()
        return

    # Show controls screen
    if current_screen == "CONTROLS":
        current_screen = show_controls_screen()
        return

    # Check if transitioning to main menu from EndScene
    if type(levels[active_level_index]) == EndScene and \
            levels[active_level_index].transition_requested():
        current_screen = "MAIN_MENU"
        return

    # Show transition screen
    if (current_screen == "TRANSITION" or
            current_screen == "TRANSITION_FROM_MAIN_MENU" or
            levels[active_level_index].transition_requested()):

        if levels[active_level_index].link.is_game_over():
            current_screen = "GAME_OVER"
            return

        if levels[active_level_index].transition_requested():
            current_screen = "TRANSITION"
        current_screen = show_transition_screen(levels[active_level_index], levels, current_screen)

        # Activate correct level after transition
        if current_screen == "GAME":
            if type(levels[active_level_index]) == Level or \
                    type(levels[active_level_index]) == BossLevel:
                if levels[active_level_index].end_game_triforce.reached:
                    activate_next_level()
                else:
                    levels[active_level_index].reset()


def load_levels(game_screen) -> None:
    global levels

    levels = [
        Level("1_1",
              25,
              "assets/music/1-1.ogg",
              (147, 187, 236)),
        Level("1_2",
              25,
              "assets/music/1-2.ogg",
              (147, 187, 236)),
        Level("1_3",
              25,
              "assets/music/1-3.ogg",
              (147, 187, 236)),
        Level("1_4",
              25,
              "assets/music/1-4.ogg",
              (147, 187, 236)),
        Level("1_5",
              10,
              "assets/music/1-5.ogg",
              (0, 0, 0), False),
        BossLevel("BOSS",
                  1,
                  "assets/music/boss.ogg",
                  (0, 0, 0), Ganondorf),
        EndScene("END",
                 1,
                 "assets/music/outro_song.ogg",
                 (147, 187, 236))
    ]

    # Setup levels
    for level in levels:
        if level.clouds_enabled and not settings.clouds:
            level.clouds_enabled = False
        level.setup(game_screen)


def setup() -> None:
    global levels

    # Screen properties
    title("Link!! Multiverse Mario")
    screen(screen_width, screen_height)
    icon("link/link_idle.png")
    
    # NOTE: setting up level happened in main.py


def update() -> None:
    global active_level_index, \
        pause_timer, \
        last_recorded_score, \
        current_screen
    # active_level_index = select_level()
    last_recorded_score = levels[active_level_index].link.coins

    # Click delay
    if not inp.clickable:
        inp.click_timer += 1
        if inp.click_timer >= inp.click_delay:
            inp.clickable = True
            inp.click_timer = 0

    # Show settings screen
    if current_screen == "SETTINGS":
        current_screen = show_settings_screen(main_menu_screen.main_menu_music)
        return
    
    # Show settings screen
    if current_screen == "ABOUT":
        current_screen = show_about_screen(main_menu_screen.main_menu_music)
        return
    # Show choose level screen
    if current_screen == "CHOOSE_LEVEL":
        current_screen = show_level_screen(main_menu_screen.main_menu_music)
        active_level_index = Support.settings.active_level
        return
    # Show main menu screen
    if current_screen == "MAIN_MENU":
        levels[active_level_index].level_music.fadeout(500)
        levels[active_level_index].level_music.stop()
        current_screen = show_main_menu_screen(levels[active_level_index])
        # active_level_index = 0
        return
    else:
        main_menu_screen.main_menu_music.fadeout(500)

    # Check if game is over
    if levels[active_level_index].link.is_game_over() or current_screen == "GAME_OVER":
        current_screen = show_game_over_screen(levels[active_level_index], last_recorded_score)
        return

    # Check if level is over
    if levels[active_level_index].transition_requested() or current_screen in transition_screens:
        process_transition_game()
        return

    # Draw levels
    levels[active_level_index].draw()

    # Check if game paused needs to be toggled
    if current_screen == "GAME":
        if pause_key_pressed() and pause_timer == 0:
            current_screen = "PAUSED"
            pause_timer = 10
    else:
        current_screen = show_paused_screen(levels[active_level_index])
        return

    # Update timers
    update_timers()
    print(active_level_index)
    # Update levels
    levels[active_level_index].update()
