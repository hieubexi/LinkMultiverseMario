import pygame

from Support.settings import screen_width, screen_height, scale
from jorcademy import *


class GameObject:

    def __init__(self, pos, w, h):
        self.die_state_index = 0
        self.die_animation_timer = 0
        self.is_grounded = False
        self.x = pos[0]
        self.y = pos[1] - 10 * scale
        self.orig_pos = pos
        self.offset = 0
        self.width = w
        self.direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.gravity = 1 * scale
        self.walk_animation_delay = 5
        self.timer = 0
        self.visible = False
        self.state = 0
        self.die_y = 0
        self.health = 1

        # Sprite data
        self.sprite_scale = 1

        # Height
        self.height = h
        self.orig_height = h
        self.die_height = h

        # Die animation
        self.die_animation_delay = 80
        self.die_animation_timer = 0
        self.die_state_index = 0
        self.death_sound = None

        # Speed
        self.jump_speed = -10 * scale
        self.speed = 4 * scale

    def out_of_screen(self):
        return (self.x + self.width < 0 or self.x - self.width > screen_width) or \
               (self.y - self.height < 0 or self.y - self.height > screen_height)

    def show_health_indicator(self):
        text(str(self.health),
             20,
             (255, 255, 255),
             self.x + self.width / 2,
             self.y - self.height / 2,
             "fonts/pixel.ttf")

    def play_death_sound(self):
        if not self.death_sound.get_num_channels() > 0:
            play_sound(self.death_sound)

    def correct_position_with_camera(self, cam_pos):
        self.x = self.orig_pos[0] - cam_pos
        self.x += self.offset

    def update(self, cam_pos, level_length):
        self.handle_movement(cam_pos, level_length)

    def show_die_animation(self):
        self.die_animation_timer += 1
        self.state = self.die_state_index

    def handle_movement(self, cam_pos, level_length):
        self.apply_gravity()
        if self.timer == 100000:
            self.timer = 0

    def draw(self):
        rect((255, 50, 50), self.x, self.y, self.width, self.height)

    def in_frame(self):
        return self.x + self.width > 0 and self.x - self.width < screen_width

    def collision(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2) >= (other.y - other.height / 2) and \
                     (self.y - self.height / 2) <= (other.y + other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def collision_top(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 - 5 * scale) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2 + 5 * scale) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y - self.height / 2 - 10 * scale) <= (other.y + other.height / 2) and \
                     (self.y - self.height / 2 + 10 * scale) >= (other.y - other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def collision_bottom(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 - 5 * scale) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2 + 5 * scale) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2 - 10 * scale) <= \
                     (other.y - other.height / 2) <= \
                     (self.y + self.height / 2 + 10 * scale)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def in_y_range_horizontal_collision(self, other):
        return (self.y + self.height / 2 - 5 * scale) >= \
               (other.y - other.height / 2) and \
               (self.y - self.height / 2 + 5 * scale) <= \
               (other.y + other.height / 2)

    def collision_left(self, other):
        in_x_range = (other.x + other.width / 2) >= (self.x - self.width / 2) >= (other.x - other.width / 2)
        return in_x_range and self.in_y_range_horizontal_collision(other)

    def collision_right(self, other):
        in_x_range = (other.x - other.width / 2) <= (self.x + self.width / 2) <= (other.x + other.width / 2)
        return in_x_range and self.in_y_range_horizontal_collision(other)

    def jump(self, speed):
        if self.is_grounded:
            self.direction.y = speed
            self.is_grounded = False

    # Applying gravity
    def apply_gravity(self):
        if self.direction.y < 15:
            self.direction.y += self.gravity
        self.y += self.direction.y
