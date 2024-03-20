from Loot.loot import Loot
from Support.settings import scale
from jorcademy import *


class Cherry(Loot):

    def __init__(self, size, pos, surface, code, player, index):
        super().__init__(size, pos, surface, code, player, index)
        self.coins = 50
        self.message = "+50 COINS"
        self.triggered_representation = "PAC_MAN"
        self.collect_sound = load_sound("assets/sounds/power_ups/power_up.ogg")
        self.image = load_image("power_ups/cherry.png")
        self.image_scale = scale

    def update(self, shift_x):
        super().update(shift_x)

        # Process effect of the loot
        if self.activated and not self.looted:
            if self.collision_with_player():
                self.make_text_anomaly()
                self.process_loot()
                self.y = 800

    def process_loot(self):
        super().process_loot()
        play_sound(self.collect_sound, 1)
        self.player.trigger_new_representation(self.triggered_representation)

