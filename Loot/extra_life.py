from Loot.loot import Loot
from Support.settings import tile_size, scale
from jorcademy import *


class ExtraLife(Loot):

    def __init__(self, size, pos, surface, code, player, index):
        super().__init__(size, pos, surface, code, player, index)
        self.message = "+1 UP"
        self.moving = False
        self.speed = 2 * scale
        self.collect_sound = load_sound("assets/sounds/power_ups/1_up.ogg")
        self.image = load_image("power_ups/1up.png")
        self.image_scale = tile_size / 256

    def update(self, shift_x):
        super().update(shift_x)

        # Move mushroom
        if self.moving:
            self.direction.x = self.speed
            self.offset += self.direction.x
            self.apply_gravity()

        # Process effect of the loot
        if self.activated and not self.looted:
            if self.collision_with_player():
                self.process_loot()
                self.y = 800

    def process_loot(self):
        super().process_loot()
        play_sound(self.collect_sound, 2)
        self.player.lives += 1

    def rise_animation(self):
        super().rise_animation()
        if self.y <= self.orig_position[1] - tile_size:
            self.moving = True
