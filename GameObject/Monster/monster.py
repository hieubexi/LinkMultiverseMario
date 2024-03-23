import random

from Environment.text_anomaly import TextAnomaly
from GameObject.gameobject import GameObject
from Support.settings import screen_width, screen_height, tile_size
from engine import *


class Monster(GameObject):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h)
        self.chunk = chunk
        self.orig_pos = pos
        self.sprite_set = []
        self.timer = 0
        self.walk_animation_delay = 10
        self.state = 0
        self.offset = 0
        self.moving = False
        self.player = player
        self.message = "+20 COINS"
        self.level = level
        self.killed = False
        self.loot = 20
        self.health = 1

        # Jump delay
        self.jump_timer = 0
        self.min_jump_delay = 60 * 1
        self.max_jump_delay = 60 * 4
        self.random_jump_delay = random.randint(self.min_jump_delay, self.max_jump_delay)

        # Attack delay
        self.invincible_timer = 0
        self.invincible_delay = 1000
        self.attack_timer = 0
        self.min_attack_delay = 60 * 5
        self.max_attack_delay = 60 * 10
        self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)

        # Sounds
        self.hit_by_player_sound = load_sound("assets/sounds/monsters/enemy_jump.ogg")
        self.hit_by_sword_sound = load_sound("assets/sounds/link/punch.ogg")
        self.hit_by_fireball_sound = load_sound("assets/sounds/fire_mario/fireball_hit.ogg")

    def is_out_of_frame(self):
        if self.moving:
            return \
                    self.x < 0 - self.width or \
                    (self.y < 0 - self.width or self.y > screen_height + self.height)

    def ready_to_remove(self):
        return self.is_out_of_frame() or \
            self.die_animation_timer >= self.die_animation_delay

    def make_text_anomaly(self):
        anomaly_pos = (self.level.link.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, self.message, 20, (255, 255, 255))
        self.level.get_current_chunk().update_text_anomalies(new_text_anomaly)

    def die(self):
        if not self.killed:
            self.die_y = self.y
            self.make_text_anomaly()
            self.player.coins_earned_current_level += self.loot

        self.killed = True

    def handle_collision_with_sword(self):
        if self.player.master_sword.collision(self) and \
                self.player.master_sword.visible and \
                self.invincible_timer <= 0:
            self.health -= 1
            self.invincible_timer = self.invincible_delay

    def handle_collision_with_fireball(self):
        for fireball in self.player.fire_mario.fireballs:
            if ((self.collision(fireball) and
                 self.invincible_timer <= 0) and
                    not self.killed):
                play_sound(self.hit_by_fireball_sound, 1.5)
                self.health -= 1
                self.invincible_timer = self.invincible_delay
                fireball.killed = True

    def handle_damage_from_player_body_collision(self):
        if self.collision_top(self.player) and self.player.collision_bottom(self):

            # Kill monster
            if not self.killed and self.invincible_timer <= 0:
                play_sound(self.hit_by_player_sound, 0.5)
                self.invincible_timer = self.invincible_delay
                self.health -= 1

                # Make player jump when landing on top of monster
                self.player.is_grounded = True
                self.player.kill_jump()

    def handle_player_damage_from_player_body_collision(self, level):
        if self.player.collision_bottom(self) and self.collision_top(self.player):
            return

        if self.collision(self.player) and not self.killed:
            if not self.player.killed:
                self.player.die(level)

    def handle_collision_with_player(self, level):
        self.invincible_timer -= 1

        # Handle collision with player and linked objects
        self.handle_collision_with_fireball()
        self.handle_collision_with_sword()
        self.handle_damage_from_player_body_collision()
        self.handle_player_damage_from_player_body_collision(level)

        # Make sure to die if health is 0
        if self.health <= 0:
            self.die()

    def handle_left_side_collision_with_map(self, tile):
        if self.collision_left(tile):
            if self.direction.x < 0:
                self.direction.x *= -1

    def handle_right_side_collision_with_map(self, tile):
        if self.collision_right(tile):
            if self.direction.x > 0:
                self.direction.x *= -1

    def handle_top_side_collision_with_map(self, tile):
        if self.collision_top(tile):
            if self.direction.y < 0:
                self.y = tile.y + tile.height / 2 + self.height / 2
                self.direction.y = 0

    def handle_bottom_side_collision_with_map(self, tile):
        if self.collision_bottom(tile):  # Bottom
            if self.direction.y > 0:
                self.y = tile.y - tile.height / 2 - self.height / 2
                self.direction.y = 0

            self.is_grounded = True

    def handle_collision(self, tile, _, level):
        self.handle_left_side_collision_with_map(tile)
        self.handle_right_side_collision_with_map(tile)
        self.handle_top_side_collision_with_map(tile)
        self.handle_bottom_side_collision_with_map(tile)
        self.handle_collision_with_player(level)

    def init_new_attack_delay(self):
        self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)

    def init_new_jump_delay(self):
        self.random_jump_delay = random.randint(self.min_jump_delay, self.max_jump_delay)

    def init_new_jump_speed(self):
        self.jump_speed = random.randint(-13, -5)

    def get_distance_from_player(self):
        return abs(self.player.x - self.x)

    def move_horizontally(self):
        self.offset += self.direction.x * self.speed

    def update(self, cam_pos, level_length):
        if not self.killed:
            super().update(cam_pos, level_length)

        self.correct_position_with_camera(cam_pos)
        self.timer += 1

        if self.get_distance_from_player() < screen_width:
            self.moving = True
