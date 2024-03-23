import math
from GameObject.Monster.monster import Monster
from Support.settings import scale, tile_size
from engine import *

# States
NOT_VULNERABLE_HORIZONTAL = 0
NOT_VULNERABLE_VERTICAL = 1
VULNERABLE = 2

# Player representations
PAC_MAN = 2


class Ghost(Monster):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            load_image("monsters/ghost/ghost_horizontal.png"),
            load_image("monsters/ghost/ghost_vertical.png"),
            load_image("monsters/ghost/ghost_vulnerable.png"),
            load_image("monsters/ghost/ghost_dead.png")
        ]
        self.y = pos[1] + tile_size / 2
        self.die_state_index = 3
        self.speed = 1.5 * scale
        self.direction = pygame.Vector2(-self.speed, 0)
        self.amplitude = 1 * scale
        self.frequency = 1 * scale
        self.eaten_sound = load_sound("assets/sounds/pac_man/eat_pac_man.ogg")

    def handle_collision_with_player(self, level):
        if self.killed:
            return

        # Process player damage & damage from player
        if self.collision(self.player):
            if self.player.representation == PAC_MAN:
                play_sound(self.eaten_sound, 0.4)
                self.die()
            elif not self.player.killed:
                self.player.die(level)

    def handle_movement(self, cam_pos, level_length):
        if self.moving:
            self.offset += self.direction.x * self.speed
            current_time = pygame.time.get_ticks()
            time_in_seconds = current_time / 1000
            sine_wave = math.sin(2 * math.pi * self.frequency * time_in_seconds)
            self.y += self.amplitude * sine_wave

    def determine_sel_sprite_index(self):
        if self.killed:
            self.show_die_animation()
            return

        self.state = NOT_VULNERABLE_HORIZONTAL

        if self.player.representation == PAC_MAN:
            self.state = VULNERABLE
        elif self.player.y < (self.y - self.height / 2) and \
                self.player.x + self.player.width / 2 > self.x - self.width / 2 and \
                self.player.x - self.player.width / 2 < self.x + self.width / 2:
            self.state = NOT_VULNERABLE_VERTICAL

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.determine_sel_sprite_index()

    def draw(self):
        # Make sure the monster is drawn facing the right direction
        if self.direction.x > 0:
            image(self.sprite_set[self.state], self.x, self.y, 1 * scale)
        else:
            image(self.sprite_set[self.state], self.x, self.y, 1 * scale, True)
