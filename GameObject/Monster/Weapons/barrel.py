from GameObject.Monster.monster import Monster
from Support.settings import scale
from engine import *


class Barrel(Monster):

    def __init__(self, pos, w, h, player, donkey_kong):
        super().__init__(pos, w, h, player, donkey_kong.level, donkey_kong.chunk)
        self.donkey_kong = donkey_kong
        self.sel_sprite_index = 0
        self.orig_cam_pos = donkey_kong.level.cam_pos
        self.sprite_set = [
            load_image("monsters/donkey_kong/barrel/barrel_1.png"),
            load_image("monsters/donkey_kong/barrel/barrel_2.png"),
            load_image("monsters/donkey_kong/barrel/barrel_3.png"),
            load_image("monsters/donkey_kong/barrel/barrel_4.png")
        ]
        self.walk_animation_delay = 5
        self.direction = pygame.Vector2(donkey_kong.get_direction(), 0)
        self.speed = 4 * scale
        self.offset = 0

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)
        self.offset += self.direction.x * self.speed
        self.x = self.orig_pos[0] - (self.donkey_kong.level.cam_pos - self.orig_cam_pos) + self.offset

    def update(self, cam_pos, level_length):
        self.handle_movement(cam_pos, level_length)
        self.timer += 1

    def draw(self):
        if self.timer % self.walk_animation_delay == 0:
            self.update_sprite_state()

        # Make sure the monster is drawn facing the right direction
        image(self.sprite_set[self.sel_sprite_index], self.x, self.y, 3 * scale)

    def update_sprite_state(self):
        if self.sel_sprite_index == len(self.sprite_set) - 1:
            self.sel_sprite_index = 0
        else:
            self.sel_sprite_index += 1

    def ready_to_remove(self):
        return self.killed

    def handle_left_side_collision_with_map(self, tile):
        if self.collision_left(tile):
            self.killed = True

    def handle_right_side_collision_with_map(self, tile):
        if self.collision_right(tile):
            self.killed = True
