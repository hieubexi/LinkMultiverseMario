import random

from GameObject.Monster.Weapons.enemy_fireball import EnemyFireBall
from GameObject.Monster.monster import Monster
from Support.settings import scale, volume
from jorcademy import *

# Ganondorf states
IDLE = 0
WALKING_1 = 1
WALKING_2 = 2
WALKING_3 = 3
WALKING_4 = 4
WALKING_5 = 5
WALKING_6 = 6
SHORT_RANGE_ATTACK_1 = 7
SHORT_RANGE_ATTACK_2 = 8
SHORT_RANGE_ATTACK_3 = 9
LONG_RANGE_ATTACK = 10
DEAD = 11


class Ganondorf(Monster):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            load_image("monsters/ganondorf/ganondorf_idle_1.png"),
            load_image("monsters/ganondorf/ganondorf_walking_1.png"),
            load_image("monsters/ganondorf/ganondorf_walking_2.png"),
            load_image("monsters/ganondorf/ganondorf_walking_3.png"),
            load_image("monsters/ganondorf/ganondorf_walking_4.png"),
            load_image("monsters/ganondorf/ganondorf_walking_5.png"),
            load_image("monsters/ganondorf/ganondorf_walking_6.png"),
            load_image("monsters/ganondorf/ganondorf_short_attack_1.png"),
            load_image("monsters/ganondorf/ganondorf_short_attack_2.png"),
            load_image("monsters/ganondorf/ganondorf_short_attack_3.png"),
            load_image("monsters/ganondorf/ganondorf_long_attack.png"),
            load_image("monsters/ganondorf/ganondorf_dead.png")
        ]
        self.die_state_index = DEAD
        self.state = IDLE
        self.orig_speed = 2 * scale
        self.speed = self.orig_speed
        self.health = 5
        self.rotation = 0
        self.jump_speed = -10 * scale

        # Idle delay
        self.idle_timer = 0
        self.random_idle_delay = random.randint(150, 600)

        # Dodge delay
        self.dodge_timer = 0
        self.random_dodge_delay = random.randint(100, 150)

        # Jump delay
        self.min_jump_delay = 60 * 1
        self.max_jump_delay = 60 * 4

        # Walking delay
        self.walk_animation_delay = 10
        self.walk_animation_timer = 0
        self.walking_timer = 0
        self.random_walking_delay = random.randint(100, 150)

        # Short range attack
        self.short_range_attack_activated = False
        self.short_range_attack_speed = 4 * scale
        self.short_range_attack_timer = 0
        self.short_range_attack_delay = 50
        self.short_range_attack_activation_distance = 200
        self.short_range_attack_animation_delay = 50 / 3
        self.short_range_attack_animation_timer = 0

        # Long range attack
        self.long_range_attack_activated = False
        self.long_range_attack_speed = 3 * scale
        self.long_range_attack_timer = 0
        self.long_range_attack_delay = 50
        self.long_range_attack_activation_distance = 200
        self.long_range_attack_animation_delay = 50 / 3
        self.long_range_attack_animation_timer = 0

        # Attack delay
        self.invincible_delay = 1000
        self.attack_timer = 0
        self.min_attack_delay = 60 * 3
        self.max_attack_delay = 60 * 6
        self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)

        # Sounds
        self.long_range_attack_sound = load_sound("assets/sounds/monsters/ganondorf/ganondorf_long_range_attack.ogg")
        self.short_range_attack_sound = load_sound("assets/sounds/monsters/ganondorf/ganondorf_short_range_attack.ogg")
        self.hit_by_player_sound = load_sound("assets/sounds/monsters/ganondorf/ganondorf_damage.ogg")
        self.die_sound = load_sound("assets/sounds/monsters/ganondorf/ganondorf_die.ogg")

    def update_sprite_state(self):
        # Dead
        if self.killed:
            self.show_die_animation()
            return

        # Idle
        if self.state == IDLE:
            return

        # Short range attack
        elif self.short_range_attack_activated:

            # Activate first short range attack state by default
            if self.state < SHORT_RANGE_ATTACK_1 or self.state > SHORT_RANGE_ATTACK_3:
                self.state = SHORT_RANGE_ATTACK_1

            # Change state
            if self.short_range_attack_timer >= self.short_range_attack_animation_delay:
                self.short_range_attack_animation_timer = 0

                # Activate next frame
                if self.state < SHORT_RANGE_ATTACK_3:
                    self.state += 1

            # Update timer
            self.short_range_attack_animation_timer += 1

        # Long range attack
        elif self.long_range_attack_activated:
            pass

        # Walking
        else:
            # Increase timers
            self.walk_animation_timer += 1

            # Switch states
            if self.walk_animation_timer >= self.walk_animation_delay:
                self.walk_animation_timer = 0
                self.state += 1
                if self.state > WALKING_6:
                    self.state = WALKING_1

    def face_towards_player(self):
        if self.player.x > self.x:
            self.direction.x = 1
        else:
            self.direction.x = -1

    def face_random_direction(self):
        if random.randint(0, 1) == 0:
            self.direction.x = 1
        else:
            self.direction.x = -1

    def get_direction(self):
        # Get the difference between the monster and the player positions
        x_diff = self.player.x - self.x
        y_diff = self.player.y - self.y

        # Form vector
        vec = pygame.Vector2(x_diff, y_diff)
        vec.normalize_ip()

        return vec

    def init_new_walking_delay(self):
        self.random_walking_delay = random.randint(150, 600)

    def init_idle_delay(self):
        self.random_idle_delay = random.randint(100, 150)

    def jump(self, speed):
        self.jump_timer = 0
        super().jump(speed)

    def init_new_jump_speed(self):
        self.jump_speed = random.randint(-18, -12)

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)

        # Stop monster action when it is killed
        if self.killed:
            play_sound(self.die_sound)
            self.y = self.die_y + self.height / 2 - 10 * scale
            self.rotation = -60
            return

        # Perform short range attack if needed
        if self.get_distance_from_player() < self.short_range_attack_activation_distance and \
                self.attack_timer >= self.random_attack_delay:
            self.perform_short_range_attack()
            return
        # Perform long range attack
        elif self.attack_timer >= self.random_attack_delay:
            self.perform_long_range_attack()
            return

        # Update attack cooldown timer
        self.attack_timer += 1

        # Update the jump timer
        if self.is_grounded:
            self.jump_timer += 1

        # Movement behavior based on state
        if self.state == IDLE:
            self.process_idle_state()
        else:
            self.process_walk_state()

    def process_idle_state(self):
        # Start walking randomly
        if self.idle_timer >= self.random_idle_delay:
            self.idle_timer = 0
            self.state = WALKING_1
            self.init_idle_delay()

        # Stop moving
        self.speed = 0

        # Update timer
        self.idle_timer += 1

    def process_walk_state(self):
        # Make the player walk randomly
        if self.walking_timer >= self.random_walking_delay:
            self.walking_timer = 0
            self.state = IDLE
            self.init_new_walking_delay()
            self.face_random_direction()

        # Make the monster jump randomly
        if self.is_grounded and self.jump_timer >= self.random_jump_delay:
            self.jump(self.jump_speed)
            self.init_new_jump_delay()
            self.init_new_jump_speed()

        # Move monster
        self.speed = self.orig_speed
        self.move_horizontally()

        # Update walking timer
        self.walking_timer += 1
        self.jump_timer += 1

    def perform_short_range_attack(self):
        # Check if the timer is up
        if self.short_range_attack_timer >= self.short_range_attack_delay:

            self.short_range_attack_timer = 0

            # Reset state
            self.state = IDLE
            self.short_range_attack_activated = False

            # Reset attack delay
            self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)
            self.attack_timer = 0
            self.short_range_attack_animation_timer = 0

            # Reset speed
            self.speed = self.orig_speed
            return

        if not self.health <= 0:
            play_sound(self.short_range_attack_sound, 0.5)

        self.short_range_attack_activated = True
        if self.state == IDLE:
            self.state = SHORT_RANGE_ATTACK_1

        # Change movement speed
        self.speed = self.short_range_attack_speed

        # Move monster
        self.face_towards_player()
        self.move_horizontally()

        # Update timer
        self.short_range_attack_timer += 1

    def face_against_player(self):
        if self.player.x > self.x:
            self.direction.x = -1
        else:
            self.direction.x = 1

    def perform_long_range_attack(self):
        # Check if the timer is up
        if self.long_range_attack_timer >= self.long_range_attack_delay:
            # Reset timer
            self.long_range_attack_timer = 0

            # Reset state
            self.state = IDLE
            self.long_range_attack_activated = False

            # Reset attack delay
            self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)
            self.attack_timer = 0

            # Reset speed
            self.speed = self.orig_speed
            return

        self.face_towards_player()

        # Play attack sound
        if not self.health <= 0:
            play_sound(self.long_range_attack_sound, 0.5)

        # Activate long range attack state
        self.long_range_attack_activated = True
        self.state = LONG_RANGE_ATTACK

        # Make monster stand still
        self.speed = 0

        # Shoot fireball
        if len(self.chunk.monsters) < 10:
            self.chunk.monsters.append(
                EnemyFireBall((self.x, self.y), 16, 16, self, self.player, self.get_direction()))

        # Update timer
        self.long_range_attack_timer += 1

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.handle_movement(cam_pos, level_length)
        self.update_sprite_state()

    def draw(self):
        image(self.sprite_set[self.state], self.x, self.y, 1.5 * scale, self.direction.x > 0, self.rotation)
        self.show_health_indicator()
