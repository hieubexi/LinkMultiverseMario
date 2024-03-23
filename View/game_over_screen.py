import string
from Support.settings import scale, screen_width, screen_height
from engine import *

# Game over screen properties
game_over_timer = 0
game_over_delay = 300


# Show game over screen
def show_game_over_screen(active_level, last_recorded_score) -> string:
    global game_over_timer
    active_level.level_music.fadeout(500)
    backdrop((0, 0, 0))

    # Display properties on screen
    text("GAME OVER", int(scale * 50), (255, 255, 255),
         screen_width / 2, screen_height / 2 - 30 * scale, "fonts/pixel.ttf")
    text(f"SCORE: {last_recorded_score}", int(20 * scale), (255, 255, 255), screen_width / 2,
         screen_height / 2 + 20 * scale, "fonts/pixel.ttf")

    if game_over_timer >= game_over_delay:
        game_over_timer = 0
        return "MAIN_MENU"

    game_over_timer += 1

    return "GAME_OVER"
