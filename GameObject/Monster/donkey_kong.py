from GameObject.Monster.Weapons.barrel import Barrel
from GameObject.Monster.monster import Monster
from Support.settings import scale
from engine import *

# Donkey Kong states
IDLE_1 = 0
IDLE_2 = 1
ATTACK = 2


class DonkeyKong(Monster):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            load_image("monsters/donkey_kong/donkey_idle_1.png"),
            load_image("monsters/donkey_kong/donkey_idle_2.png"),
            load_image("monsters/donkey_kong/donkey_throw.png"),
            load_image("monsters/donkey_kong/donkey_kong_dead.png")
        ]
        self.state = IDLE_1
        self.die_state_index = 3
        self.speed = 1 * scale
        self.health = 3
        self.direction = pygame.Vector2(-self.speed, 0)
        self.jump_speed = -16 * scale
        self.walk_animation_delay = 15
        self.y -= 1 * scale

        # Jump delay
        self.min_jump_delay = 60 * 1
        self.max_jump_delay = 60 * 3

        # Attack delay
        self.min_attack_delay = 60 * 3
        self.max_attack_delay = 60 * 6

    def jump(self, speed):
        self.jump_timer = 0
        super().jump(speed)

    def attack(self):
        self.state = ATTACK

        # Add new barrel to the chunk's monster list
        barrel = Barrel((self.x, self.y), 36 * scale, 30 * scale, self.player, self)
        self.level.chunks[self.chunk.index].monsters.append(barrel)

        # Reset attack timer
        self.init_new_attack_delay()
        self.attack_timer = 0

    def get_direction(self):
        if self.player.x <= self.x:
            return -1
        else:
            return 1

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.handle_movement(cam_pos, level_length)

        # Stop monster action when dead
        if self.killed:
            return

        # Make the monster jump when the timer is up
        if self.is_grounded and self.jump_timer >= self.random_jump_delay:
            self.jump(self.jump_speed)
            self.init_new_jump_delay()
            self.init_new_jump_speed()

        # Attack randomly
        if self.attack_timer >= self.random_attack_delay:
            self.attack()

        # Update the jump timer
        if self.is_grounded:
            self.jump_timer += 1

        # Update attack timer
        self.attack_timer += 1

    def draw(self):
        self.update_sprite_state()

        # Make sure the monster is drawn facing the right direction
        image(self.sprite_set[self.state], self.x, self.y, 3 * scale, self.player.x >= self.x)
        self.show_health_indicator()

    def update_sprite_state(self):
        if self.killed:
            self.show_die_animation()
            return

        # Update jump animation
        if self.timer % self.walk_animation_delay == 0:
            if self.state != ATTACK:
                if self.state < IDLE_2:
                    self.state += 1
                else:
                    self.state = IDLE_1
            else:
                attack_animation_delay = 15
                if self.timer % attack_animation_delay == 0:
                    self.state = IDLE_1
