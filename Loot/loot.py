from Environment.text_anomaly import TextAnomaly
from Level.Tiles.tile import MovingTile
from Support.settings import tile_size
from jorcademy import *


class Loot(MovingTile):

    def __init__(self, size, pos, surface, code, player, index):
        super().__init__(size, pos, surface, code, index)
        self.activated = False
        self.speed = 2
        self.player = player
        self.looted = False
        self.level = None
        self.coins = 0
        self.message = "SAMPLE_MESSAGE"
        self.triggered_representation = "SAMPLE_TRIGGERED_REPRESENTATION"
        self.image_scale = 1

    def show(self, level):
        self.correct_position_with_camera(level.cam_pos)
        self.activated = True
        self.direction.y = -self.speed
        self.level = level

    def make_text_anomaly(self):
        anomaly_pos = (self.level.link.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, self.message, 20, (255, 255, 255))
        self.level.get_current_chunk().update_text_anomalies(new_text_anomaly)

    def correct_position_with_camera(self, cam_pos):
        self.x = self.orig_position[0] - cam_pos
        self.x += self.offset

    def rise_animation(self):
        if self.activated and self.y > self.orig_position[1] - tile_size:
            self.y += self.direction.y
        else:
            self.direction.y = 0

    def collision_with_player(self):
        return self.player.collision(self)

    def process_loot(self):
        self.player.coins_earned_current_level += self.coins
        self.make_text_anomaly()
        self.looted = True

    def update(self, shift_x):
        super().update(shift_x)
        self.rise_animation()

    def draw(self):
        image(self.image, self.x, self.y, self.image_scale)
