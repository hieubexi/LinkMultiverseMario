from GameObject.Monster.monster import Monster
from Support.settings import scale
from jorcademy import *


class Bokoblin(Monster):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            load_image("monsters/bokoblin/bokoblin_1.png"),
            load_image("monsters/bokoblin/bokoblin_2.png"),
            load_image("monsters/bokoblin/bokoblin_dead.png")
        ]
        self.y = self.y - 10 * scale
        self.speed = 1
        self.direction = pygame.Vector2(-self.speed, 0)
        self.die_state_index = 2

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)
        if self.moving:
            self.offset += self.direction.x * self.speed

    def draw(self):
        self.update_sprite_state()

        # Make sure the monster is drawn facing the right direction
        if self.direction.x > 0:
            image(self.sprite_set[self.state], self.x, self.y, 3 * scale)
        else:
            image(self.sprite_set[self.state], self.x, self.y, 3 * scale, True)

    def update_sprite_state(self):
        if self.killed:
            self.y = self.die_y + self.height / 2 - 3 * scale
            self.show_die_animation()
            return

        # Update walking animation
        if self.timer % self.walk_animation_delay == 0:
            if self.state < len(self.sprite_set) - 2:
                self.state += 1
            else:
                self.state = 0
