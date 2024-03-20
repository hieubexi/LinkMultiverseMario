from GameObject.gameobject import GameObject
from Support.settings import scale
from jorcademy import *


class FireBall(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.bounce = False
        self.start_bouncing_y = 0
        self.bounce_offset_y = 10 * scale
        self.killed = None
        self.visible = False
        self.player = player
        self.sprite = load_image("fire_mario/fireball.png")
        self.speed = 8 * scale
        self.amplitude = 5 * scale
        self.frequency = 0.1 * scale

        # Direction of the fireball
        if self.player.facing_left:
            self.direction.x = -1
        else:
            self.direction.x = 1

    def handle_movement(self, cam_pos, level_length):
        self.x += self.direction.x * self.speed

        # Handle bouncing
        if self.bounce:
            self.y -= 4 * scale
        else:
            self.y += 4 * scale

        if self.y < self.start_bouncing_y - self.bounce_offset_y:
            self.bounce = False

    def handle_collision(self, tile, _, __):
        if self.collision_left(tile) or self.collision_right(tile):
            self.killed = True
        if self.collision_bottom(tile) and not self.bounce:
            self.bounce = True
            self.start_bouncing_y = self.y

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)

        # Check if fireball is out of screen
        if self.out_of_screen():
            self.killed = True

    def draw(self):
        image(self.sprite, self.x, self.y + 8 * scale, 0.16 * scale, False, 0)
