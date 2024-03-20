from Loot.loot import Loot
from Support.settings import tile_size, scale
from jorcademy import *


class Coin(Loot):

    def __init__(self, size, pos, surface, code, player, index):
        super().__init__(size, pos, surface, code, player, index)
        self.timer = 0
        self.disappear_delay = 20
        self.message = "+100 COINS"
        self.coins = 100
        self.collect_sound = load_sound("assets/sounds/power_ups/coin.ogg")
        self.image = load_image("power_ups/coin.png")
        self.image_scale = scale

    def show(self, level):
        super().show(level)
        self.make_text_anomaly()

        # Process effect of the loot
        if not self.looted:
            self.process_loot()

    def process_loot(self):
        play_sound(self.collect_sound, 0.7)
        super().process_loot()

    def update(self, shift_x):
        super().update(shift_x)

        # Make coin disappear after a while
        if self.activated and self.y <= self.orig_position[1] - tile_size:
            self.timer += 1
            if self.timer % self.disappear_delay == 0:
                self.y = 800
