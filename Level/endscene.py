from GameObject.gameobject import GameObject
from Level.level import Level
from Level.triforce_key import TriforceKey
from Support.settings import screen_width, screen_height, tile_size, scale
from engine import *


class EndScene(Level):

    def __init__(self, level_name, chunk_amount, level_music_path, level_backdrop_color):
        super().__init__(level_name, chunk_amount, level_music_path, level_backdrop_color)
        self.subtitles_shown = False
        self.zelda = GameObject(
            (screen_width / 2 + 100 * scale, screen_height - tile_size * 2 - 97 * 0.7 / 2 * scale),
            46 * 0.7 * scale,
            97 * 0.7 * scale)
        self.end_reached = False
        self.heart = GameObject((screen_width / 2, 0 - 50 * scale), 50 * scale, 50 * scale)

        # Transition to subtitles
        self.to_subtitles_delay = 200
        self.to_subtitles_timer = 0

        # Start subtitles
        self.start_subtitles_delay = 600
        self.start_subtitles_timer = 0

        # Switch subtitles
        self.switch_subtitles_delay = 150
        self.switch_subtitles_timer = 0

        # Music
        self.level_music = load_sound(level_music_path)
        self.level_music_started = False

        # Images
        self.heart_image = load_image("other/heart.png")
        self.zelda_image = load_image("zelda/zelda.png")

        # Subtitles index
        self.subtitles_index = 0

    def setup(self, game_screen):
        super().setup(game_screen)
        self.end_game_triforce = TriforceKey((screen_width / 2, 0), 50 * scale, 50 * scale, self.link)
        self.link.at_game_end = True

    def reset(self):
        super().reset()
        self.zelda = GameObject(
            (screen_width / 2 + 100 * scale, screen_height - tile_size * 2 - 97 * 0.7 / 2),
            46 * 0.7 * scale,
            97 * 0.7 * scale)
        self.heart = GameObject((screen_width / 2, 0 - 50), 50, 50)
        self.link.speed = 4 * scale
        self.subtitles_shown = False
        self.end_reached = False
        self.to_subtitles_timer = 0
        self.start_subtitles_timer = 0
        self.switch_subtitles_timer = 0
        self.subtitles_index = 0
        self.link.at_game_end = True

    def transition_requested(self):
        return self.subtitles_shown

    # Make sure the player doesn't move too far to the right
    def stop_moving_link_when_needed(self):
        if self.link.x >= screen_width / 2 - 100 * scale:
            self.link.gravity = 0
            self.link.speed = 0
            self.end_reached = True

    def move_world_down(self):
        # Move sprites
        self.link.y += 2 * scale
        self.zelda.y += 2 * scale
        self.heart.y += 2 * scale

        # Move tiles
        for chunk in self.chunks:
            for tile in chunk.tiles:
                tile.y += 2 * scale

    def show_heart(self):
        if self.heart.y <= screen_height / 2:
            self.heart.y += 3 * scale
        else:
            self.to_subtitles_timer += 1

    def show_subtitles(self):
        subtitles = [
            # Ending messages for the game
            ["LINK!!! MULTIVERSE MARIO HAS COME TO AN END"],
            ["THANK YOU FOR PLAYING"],
            ["A GAME BY NGUYEN HUU HIEU"],
            ["THANKS TO MY TEAM:", "THAI TANG HUY - 2013329", "HO TRONG PHUC - 2014159"],
        ]

        # Subtitle properties
        font_size = int(scale * 25)
        text_color = (255, 255, 255)
        text_font = "fonts/pixel.ttf"

        # Calculate starting Y position of the subtitles
        total_subtitles_height = len(subtitles[self.subtitles_index]) * font_size * scale
        starting_y = (screen_height - total_subtitles_height) / 2  # Calculate starting Y position

        # Draw subtitles
        for i, item in enumerate(subtitles[self.subtitles_index]):
            text(item,
                 font_size,
                 text_color,
                 screen_width / 2,
                 starting_y + i * font_size * scale,
                 text_font)

        # Update timer
        self.switch_subtitles_timer += 1

        # Switch to next subtitle
        if self.switch_subtitles_timer >= self.switch_subtitles_delay:
            if self.subtitles_index >= len(subtitles) - 1:
                self.subtitles_shown = True
                return

            # Reset timer & change index
            self.subtitles_index += 1
            self.switch_subtitles_timer = 0

    def update(self):
        # Update chunks
        chunks_to_update = self.get_chunks_in_range()
        for chunk in chunks_to_update:
            chunk.update(self.cam_pos, self.level_length)

        # Update player
        self.stop_moving_link_when_needed()
        self.link.update(self.cam_pos, self, False)

        # Update environment
        self.update_environmental_objects(self.cam_pos, self.level_length)

        # Move the map down when needed
        if self.to_subtitles_timer >= self.to_subtitles_delay:
            self.move_world_down()

        # Show the heart when needed
        if self.end_reached:
            self.show_heart()

        # Show subtitles when needed
        self.start_subtitles_timer += 1
        if self.start_subtitles_timer >= self.start_subtitles_delay:
            self.show_subtitles()
            return

        # Play music
        if not self.level_music.get_num_channels() > 0:
            self.level_music.play(-1)
            self.level_music.set_volume(0.25 * settings.volume)

        # Collision
        self.handle_collision()

    def draw(self):

        # == Background
        backdrop(self.backdrop_color)

        # Draw environment
        self.draw_environment()

        # == Player
        self.link.draw()

        # Zelda
        image(self.zelda_image, self.zelda.x, self.zelda.y, 0.7 * scale, True, 0)

        # Heart
        if self.end_reached:
            image(self.heart_image, self.heart.x, self.heart.y, 0.2 * scale, True, 0)

        # Coin amount
        text(f"COINS: {str(self.link.coins)}",
             int(scale * 25),
             (255, 255, 255),
             100 * scale,
             25 * scale,
             "fonts/pixel.ttf")

        # Lives amount
        text(f"LIVES: {str(self.link.lives)}",
             int(scale * 25),
             (255, 255, 255),
             screen_width / 2,
             25 * scale,
             "fonts/pixel.ttf")

        # World number
        text(f"WORLD: {str(self.level_name)}",
             int(scale * 25),
             (255, 255, 255),
             screen_width / 2 + 300 * scale,
             25 * scale,
             "fonts/pixel.ttf")
