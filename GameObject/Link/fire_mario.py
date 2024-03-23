from GameObject.Link.Weapons.fireball import FireBall
from GameObject.gameobject import GameObject
from Support.settings import screen_width, scale
from Support.input import *
from engine import *

# States for FireMario
IDLE = 0
JUMPING = 1
WALKING_1 = 2
WALKING_2 = 3
WALKING_3 = 4
ATTACK = 5
DEAD = 6


class FireMario(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.MAX_FIREBALLS = 5
        self.player = player
        self.sprites = [
            load_image('fire_mario/fire_mario_idle.png'),
            load_image('fire_mario/fire_mario_jumping.png'),
            load_image('fire_mario/fire_mario_walking_1.png'),
            load_image('fire_mario/fire_mario_walking_2.png'),
            load_image('fire_mario/fire_mario_walking_3.png'),
            load_image('fire_mario/fire_mario_attack.png'),
            load_image("fire_mario/fire_mario_dead.png")
        ]
        self.attack_cooldown = 50
        self.active_cooldown = 0
        self.state = IDLE
        self.facing_left = self.player.facing_left
        self.is_grounded = False
        self.visible = False
        self.attack_cooldown = 20
        self.active_cooldown = 0
        self.fireball_thrown = False
        self.fireballs = []

        # Sprite data
        self.sprite_scale = 2

        # Sounds
        self.fire_sound = load_sound('assets/sounds/fire_mario/fireball.ogg')
        self.jump_sound = load_sound('assets/sounds/fire_mario/mario_jump.ogg')
        self.death_sound = load_sound('assets/sounds/fire_mario/fire_mario_death.ogg')

    def handle_movement(self, cam_pos, level_length):
        if self.active_cooldown > 0:
            self.active_cooldown -= 1

        # Update horizontal direction and position of Link
        if move_right_key_pressed() and not attack_key_pressed():
            self.move_right(cam_pos, level_length)
        elif move_left_key_pressed() and not attack_key_pressed():
            self.move_left()
        elif self.is_grounded and not self.active_cooldown > 0:
            self.direction.x = 0
            self.state = IDLE

        # Update the vertical position of Link
        if jump_key_pressed():
            self.jump(self.player.max_jump_speed)

    def handle_collision(self, tile, index, level):
        if self.visible:
            for fireball in self.fireballs:
                fireball.handle_collision(tile, index, level)

    # Move right
    def move_right(self, cam_pos, level_length):
        self.facing_left = False

        # Handle animation
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_3:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

        # Update coordinates
        self.direction.x = self.speed
        if self.x < screen_width / 2 or cam_pos >= (level_length - screen_width):
            self.x += self.direction.x

    # Move left
    def move_left(self):
        self.facing_left = True

        # Handle animation
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_3:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

    def activate_attack_cooldown(self):
        self.active_cooldown = self.attack_cooldown

    # Attack action
    def attack(self):
        if self.active_cooldown <= 0 and self.visible:
            self.state = ATTACK

            # Create fireball
            if len(self.fireballs) < self.MAX_FIREBALLS:
                self.fireballs.append(FireBall((self.x, self.y), 16 * scale, 16 * scale, self.player))

            play_sound(self.fire_sound, 2)
            self.activate_attack_cooldown()

    # Let character jump
    def jump(self, speed):
        self.timer = 0
        self.state = JUMPING
        if self.is_grounded:
            self.direction.y = speed
            self.is_grounded = False

    # Update FireMario
    def update(self, cam_pos, level_length):
        if self.player.killed and self.visible:
            self.play_death_sound()
            self.y = self.player.y
            self.state = DEAD
            return

        super().update(cam_pos, level_length)

        # Update fireballs
        for fireball in self.fireballs:
            if fireball.killed:
                self.fireballs.remove(fireball)
            fireball.update(cam_pos, level_length)

        # Start attack
        if attack_key_pressed() and \
           self.active_cooldown <= 0:
            self.attack()

        # Update weapon attack cooldown
        if self.active_cooldown > 0:
            self.active_cooldown -= 1

        # Derive properties from player
        self.facing_left = self.player.facing_left
        self.is_grounded = self.player.is_grounded
        self.x = self.player.x
        self.y = self.player.y

    # Draw FireMario
    def draw(self):
        sprite = self.sprites[self.state]

        if self.visible:
            image(sprite, self.x, self.y, self.sprite_scale * scale, self.facing_left)

        # Draw linked objects
        for fireball in self.fireballs:
            fireball.draw()
