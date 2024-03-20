from GameObject.gameobject import GameObject
from Support.settings import scale
from jorcademy import *


class Triforce(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.image = load_image("other/triforce.png")
        self.player = player
        self.reached = False

    def handle_movement(self, cam_pos, level_length):
        pass

    def process_earned_player_coins(self):
        self.player.coins += self.player.coins_earned_current_level

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.correct_position_with_camera(cam_pos)

        # If the player collides with the triforce, it is looted
        if self.player.x >= self.x:
            self.process_earned_player_coins()
            self.reached = True

    def draw(self):
        image(self.image, self.x, self.y, 0.5 * scale, False, 0)
