from Environment.text_anomaly import TextAnomaly
from GameObject.Link.Weapons.master_sword import MasterSword
from GameObject.Link.fire_mario import FireMario
from GameObject.Link.pac_man import PacMan
from GameObject.gameobject import GameObject
from Level.Tiles.tile_data import *
from Loot.loot import Loot
from Support.settings import screen_width, screen_height, scale, tile_size
from Support.input import *
from jorcademy import *

# States for Link
IDLE = 0
ATTACK = 1
WALKING_1 = 2
WALKING_2 = 3
WALKING_3 = 4
WALKING_4 = 5
WALKING_5 = 6
WALKING_6 = 7
WALKING_7 = 8
WALKING_8 = 9
WALKING_9 = 10
WALKING_10 = 11
JUMPING = 12
DEAD = 13

# Representations for Link
LINK = 0
FIRE_MARIO = 1
PAC_MAN = 2


class Link(GameObject):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.lives = 3
        self.coins = 0  # NOTE: maybe change coins into rupees
        self.orig_speed = 6
        self.speed = 6
        self.facing_left = False
        self.is_grounded = True
        self.walk_animation_delay = 3
        self.state = IDLE
        self.representation = LINK
        self.attack_cooldown = 50
        self.active_cooldown = 0
        self.master_sword = MasterSword((self.x, self.y), 45 * scale, 33 * scale, self)
        self.visible = True
        self.fire_mario = FireMario((self.x, self.y), 32 * scale, 64 * scale, self)
        self.pac_man = PacMan((self.x, self.y), 48 * scale, 48 * scale, self)
        self.representation_change_timer = 0
        self.representation_change_delay = 1000
        self.killed = False
        self.max_speed = 0.8 * scale
        self.at_game_end = False
        self.coins_earned_current_level = 0
        self.die_state_index = DEAD
        self.sprites = [
            load_image('link/link_idle.png'),
            load_image('link/link_fight.png'),
            load_image('link/link_walking_1.png'),
            load_image('link/link_walking_2.png'),
            load_image('link/link_walking_3.png'),
            load_image('link/link_walking_4.png'),
            load_image('link/link_walking_5.png'),
            load_image('link/link_walking_6.png'),
            load_image('link/link_walking_7.png'),
            load_image('link/link_walking_8.png'),
            load_image('link/link_walking_9.png'),
            load_image('link/link_walking_10.png'),
            load_image('link/link_jumping.png'),
            load_image("link/link_dead.png")
        ]

        # Jumping
        self.jumping_locked = False
        self.max_jump_speed = -5 * scale
        self.min_jump_speed = -12 * scale
        self.jump_offset = 0

        # Power-up indicators
        self.fire_mario_indicator = load_image("power_ups/power_up_indicator_mario.png")
        self.pac_man_indicator = load_image("power_ups/power_up_indicator_pac_man.png")

        # Sprite data
        self.sprite_scale = 1.28 * scale

        # Dimensions
        self.die_height = 16 * scale

        # Load sounds
        self.jump_sound = load_sound('assets/sounds/link/jump.ogg')
        self.one_up_sound = load_sound("assets/sounds/power_ups/1_up.ogg")
        self.death_sound = load_sound("assets/sounds/link/link_death_sound.ogg")

    def collision_top(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 - 7.5 * scale) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2 + 7.5 * scale) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y - self.height / 2 - 10 * scale) <= (other.y + other.height / 2) and \
                     (self.y - self.height / 2 + 10 * scale) >= (other.y - other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def handle_collision(self, tile, index, level):
        # Ignore loot for terrain collision
        if issubclass(type(tile), Loot):
            return

        # Handle collision on left side of object
        if self.collision_left(tile):
            if self.direction.x < 0:
                self.x = tile.x + tile.width / 2 + self.width / 2

        # Handle collision on right side of object
        elif self.collision_right(tile):
            if self.direction.x > 0:
                self.x = tile.x - tile.width / 2 - self.width / 2

        # Handle collision on bottom side of object
        if self.collision_bottom(tile):
            if self.direction.y > 0:
                self.y = tile.y - tile.height / 2 - self.height / 2
                self.direction.y = 0

        # Handle collision on top side of object
        elif self.collision_top(tile):
            if self.direction.y < 0:
                self.y = tile.y + tile.height / 2 + self.height / 2
                self.direction.y = 0
                self.jumping_locked = True


                # Handle collision with mystery box
                if tile.code == MYSTERY_BOX:
                    if not tile.emptied:
                        loot = tile.give_loot(level)
                        level.get_current_chunk().tiles.insert(loot.index, loot)
                elif tile.code in BREAKABLE:
                    tile.break_tile(level.get_right_sky_tile())

        # Handle collision of linked objects
        self.fire_mario.handle_collision(tile, index, level)

    def show_power_up_indicator(self):
        if self.representation != LINK:
            timer = self.representation_change_delay - self.representation_change_timer

            # Get sprite for power up indicator
            if self.representation == FIRE_MARIO:
                sprite = self.fire_mario_indicator
            else:
                sprite = self.pac_man_indicator

            # Show power up indicator
            image(sprite, 45 * scale, 60 * scale, 0.66 * scale)

            # Show timer
            text(f"{timer}",
                 int(25 * scale),
                 (255, 255, 255),
                 85 * scale, 58 * scale,
                 "fonts/pixel.ttf")

    def handle_movement(self, cam_pos, level_length, at_level_end=False):
        super().handle_movement(cam_pos, level_length)
        if (self.x < screen_width / 2 or cam_pos >= (level_length - screen_width)
                and self.x > 30):
            self.x += self.direction.x * self.speed

        # Update jumping lock
        if self.is_grounded:
            self.jumping_locked = False

        # Prevent movement if at end of level
        if at_level_end or self.speed == 0:
            self.state = IDLE
            return

        # Update horizontal direction and position of Link
        min_x = 75
        if move_right_key_pressed() and not move_left_key_pressed():
            self.move_right()
        elif move_left_key_pressed() and not move_right_key_pressed() and self.x > min_x:
            self.move_left()
        elif self.is_grounded:
            self.state = IDLE

        # Make sure jumping direction cannot change negatively midair
        if not self.is_grounded and not jump_key_pressed():
            self.jumping_locked = True

        # Update the vertical position of Link
        if jump_key_pressed():
            if not self.jumping_locked:
                self.jump()

    def move_right(self):
        self.facing_left = False

        # Clamp direction
        if self.direction.x < 0:
            self.direction.x = 0

        # Handle animation
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_10:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

        # Update coordinates
        if abs(self.direction.x) < self.max_speed and not attack_key_pressed():
            self.direction.x += 0.25 * scale

    # Move left
    def move_left(self):
        self.facing_left = True

        # Clamp direction
        if self.direction.x > 0:
            self.direction.x = 0

        # Handle animation
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_10:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

        # Update coordinates
        if abs(self.direction.x) < self.max_speed and self.x > 30 and not attack_key_pressed():
            self.direction.x -= 0.25 * scale

        if self.x > 30:
            self.x += self.direction.x

    def activate_attack_cooldown(self):
        self.state = IDLE
        self.active_cooldown = self.attack_cooldown

    # Attack action
    def attack(self):
        if self.active_cooldown <= 0 and self.visible:
            self.master_sword.attack()
            self.state = ATTACK
        else:
            self.state = IDLE

    def jump(self, enemy_killed=False):
        self.state = JUMPING

        if self.direction.y <= self.min_jump_speed:
            self.jumping_locked = True
            return

        # Play jump sound
        if self.is_grounded:
            self.jump_offset = 0
            if not enemy_killed and self.representation == LINK:
                play_sound(self.jump_sound, 0.8)
            elif not enemy_killed and self.representation == FIRE_MARIO:
                play_sound(self.fire_mario.jump_sound, 1.5)

        self.jump_offset += -2 * scale
        self.direction.y = self.max_jump_speed + self.jump_offset
        self.is_grounded = False

    def kill_jump(self):
        jump_boost = 2.3
        self.direction.y = self.max_jump_speed * jump_boost

    def switch_representation_jump(self):
        jump_boost = 1.5
        self.direction.y = self.max_jump_speed * jump_boost

    def trigger_new_representation(self, representation):
        if representation == "FIRE_MARIO":
            self.representation = FIRE_MARIO
        elif representation == "PAC_MAN":
            self.representation = PAC_MAN

    def change_velocity(self):
        if abs(self.direction.x) < 0.1:
            self.direction.x = 0
            return

        # Make player slow down
        if self.direction.x < 0:
            self.direction.x += 0.1
        elif self.direction.x > 0:
            self.direction.x -= 0.1

    def make_text_anomaly(self, level, message):
        anomaly_pos = (self.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, message, 20, (255, 255, 255))
        level.get_current_chunk().update_text_anomalies(new_text_anomaly)

    def handle_1up_with_coins(self, level):
        level_up_coin_threshold = 1000
        if self.coins + self.coins_earned_current_level >= level_up_coin_threshold:
            self.coins = 0
            self.coins_earned_current_level = 0
            self.lives += 1
            self.make_text_anomaly(level, "+1 UP")
            play_sound(self.one_up_sound, 0.5)

    def is_game_over(self):
        return self.killed and \
            self.lives == 0 and \
            self.die_animation_timer >= self.die_animation_delay

    def update(self, cam_pos, level, at_level_end=False):
        # Update state of linked representations
        self.handle_representation()
        self.fire_mario.update(cam_pos, level.level_length)
        self.pac_man.update(cam_pos, level.level_length)

        # Handle Link DEAD state
        if self.killed:
            if self.visible:
                self.play_death_sound()

            self.height = self.die_height * self.sprite_scale
            self.apply_gravity()
            self.show_die_animation()
            return

        # Update position
        self.handle_movement(cam_pos, level.level_length, at_level_end)
        self.change_velocity()

        # Die when out of screen
        if self.y > screen_height:
            self.die()

        # Update lives with respect to coins
        self.handle_1up_with_coins(level)

        # Start attack
        if attack_key_pressed() and self.is_grounded:
            self.attack()

        # Update weapon attack cooldown
        if self.active_cooldown > 0:
            self.active_cooldown -= 1

        # Update state of linked objects
        self.master_sword.update(cam_pos, level.level_length)

    def activate_main_representation(self):
        if self.representation == LINK:
            return

        self.switch_representation_jump()
        self.representation = LINK
        self.height = self.orig_height
        self.representation_change_timer = 0

        # Disable other representations
        self.fire_mario.visible = False
        self.pac_man.visible = False

    def activate_alt_representation(self, representation):
        self.visible = False
        self.representation_change_timer += 1

        # Activate alt representation
        if representation == FIRE_MARIO:
            self.fire_mario.visible = True
            self.height = self.fire_mario.height
            self.pac_man.visible = False
        elif representation == PAC_MAN:
            self.height = self.pac_man.height
            self.fire_mario.visible = False
            self.pac_man.visible = True

    def handle_representation(self):
        # Check if representation should change
        if self.representation_change_timer >= self.representation_change_delay:
            self.activate_main_representation()

        # == Determine which representation to show

        # Link
        if self.representation == LINK:
            self.representation_change_timer = 0
            self.visible = True

        # Fire Mario
        elif self.representation == FIRE_MARIO:
            self.reset_representation_timer(self.fire_mario)
            self.activate_alt_representation(FIRE_MARIO)

        # Pac-Man
        elif self.representation == PAC_MAN:
            self.reset_representation_timer(self.pac_man)
            self.activate_alt_representation(PAC_MAN)

        # Other
        else:
            self.visible = True
            self.representation_change_timer += 1

    def reset_representation_timer(self, representation_object):
        if not representation_object.visible:
            self.switch_representation_jump()
            self.representation_change_timer = 0

    # Draw Link
    def draw(self):
        sprite = self.sprites[self.state]

        # Only draw when visible
        if self.visible:
            image(sprite, self.x, self.y, self.sprite_scale, self.facing_left)
            self.master_sword.draw()

        # Draw alternative representations
        self.show_power_up_indicator()
        self.fire_mario.draw()
        self.pac_man.draw()

    def die(self, level=None):
        if not self.at_game_end:
            # self.lives -= 1
            # self.killed = True
            pass

    def soft_reset(self):
        self.gravity = 0.8 * scale
        self.die_animation_timer = 0
        self.speed = self.orig_speed
        self.killed = False
        self.coins_earned_current_level = 0
        self.activate_main_representation()
        self.height = self.orig_height
        self.at_game_end = False
        self.x = 100
        self.y = screen_height - 2 * tile_size - self.height

    def hard_reset(self):
        self.coins = 0
        self.lives = 3
        self.soft_reset()
