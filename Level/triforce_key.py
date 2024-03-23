from Level.triforce import Triforce
from Support.settings import screen_width, screen_height, scale
from engine import *


class TriforceKey(Triforce):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h, player)
        self.x = screen_width / 2
        self.y = 0 - self.height * 2
        self.image = load_image("other/triforce.png")
        self.moving_allowed = False
        self.speed = 2 * scale
        self.final_y = screen_height / 2 + self.height

    def update(self, cam_pos, level_length):
        # Check whether the triforce key can be moved
        if self.moving_allowed and self.y < self.final_y:
            self.move_down()

        # If the player collides with the triforce, the end of the level is reached
        if self.collision(self.player):
            self.reached = True

    def move_down(self):
        self.y += self.speed

    def draw(self):
        image(self.image, self.x, self.y, 0.25 * scale, False, 0)

