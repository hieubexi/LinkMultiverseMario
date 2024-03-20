import random

from GameObject.gameobject import GameObject
from Support.settings import screen_width, scale
from jorcademy import *


class Cloud(GameObject):

    def __init__(self, image, cam_pos):
        x = screen_width + cam_pos / 10
        y = random.randint(50, 150)
        pos = (x, y)
        self.image = image
        self.image_scale = random.randint(50, 200) / 100
        w = 64 * self.image_scale
        h = 37 * self.image_scale
        super().__init__(pos, w, h)
        self.speed = random.randint(1, 3) / 10 * scale

    def ready_to_remove(self):
        return self.x < -self.width / 2

    def correct_position_with_camera(self, cam_pos):
        self.x = self.orig_pos[0] - cam_pos / 10
        self.x += self.offset

    def update(self, cam_pos, level_length):
        self.correct_position_with_camera(cam_pos)
        self.offset -= self.speed

    def draw(self):
        image(self.image, self.x * scale, self.y * scale, self.image_scale)
