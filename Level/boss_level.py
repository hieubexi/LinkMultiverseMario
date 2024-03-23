from Level.level import Level
from Level.triforce_key import TriforceKey
from Support.settings import screen_width, scale
from engine import *


class BossLevel(Level):

    def __init__(self, level_name, chunk_amount, level_music_path, level_backdrop_color, boss_type):
        super().__init__(level_name, chunk_amount, level_backdrop_color, (0, 0, 0), False)
        self.end_game_triforce = None
        self.boss_type = boss_type
        self.boss = None
        self.die_sound_played = False
        self.boss_die_sound = load_sound("assets/sounds/monsters/ganondorf/ganondorf_die.ogg")

        # Music
        self.level_music = load_sound(level_music_path)
        self.level_music_started = False

    def setup(self, game_screen):
        super().setup(game_screen)
        self.end_game_triforce = TriforceKey((screen_width / 2, 0), 50, 50, self.link)

        # Move Link
        self.link.x += 30 * scale

        # Record the boss
        for chunk in self.chunks:
            for monster in chunk.monsters:
                if type(monster) == self.boss_type:
                    self.boss = monster

    def reset(self):
        super().reset()
        self.link.at_game_end = False
        self.end_game_triforce.moving_allowed = False

    def update(self):
        # Stop music if game is over
        if self.transition_requested() or self.boss.killed:
            self.level_music.fadeout(500)

        # Update chunks in range
        chunks_to_update = self.get_chunks_in_range()
        for chunk in chunks_to_update:
            chunk.update(self.cam_pos, self.level_length)

        # Update player
        self.link.update(self.cam_pos, self, False)

        # Update endgame triforce
        if self.boss.killed:

            # Play boss kill sound
            if not self.die_sound_played:
                play_sound(self.boss_die_sound, 0.5)
                self.die_sound_played = True

            self.end_game_triforce.moving_allowed = True
        self.end_game_triforce.update(self.cam_pos, self.level_length)

        # Play music
        if not self.level_music.get_num_channels() > 0 and not self.boss.killed:
            self.level_music.play(-1)
            self.level_music.set_volume(0.25 * settings.volume)

        # Collision
        self.handle_collision()

    def draw(self):

        # == Background
        backdrop(self.backdrop_color)

        # == Chunks
        self.draw_environment()

        # Draw triforce key
        self.end_game_triforce.draw()

        # == Player
        self.link.draw()

        # Coin amount
        text(f"COINS: {str(self.link.coins)}",
             int(25 * scale),
             (255, 255, 255),
             100 + 55 * scale,
             25 + 25 * scale,
             "fonts/pixel.ttf")

        # Lives amount
        text(f"LIVES: {str(self.link.lives)}",
             int(25 * scale),
             (255, 255, 255),
             screen_width / 2 + 10 * scale,
             25 + 25 * scale,
             "fonts/pixel.ttf")

        # World number
        text(f"WORLD: {str(self.level_name)}",
             int(25 * scale),
             (255, 255, 255),
             screen_width / 2 + 300 * scale - 70 * scale,
             25 + 25 * scale,
             "fonts/pixel.ttf")
