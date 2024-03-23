from GameObject.gameobject import GameObject
from Level.Tiles.tile_data import *
from Support.settings import tile_size, screen_height, screen_width
from engine import *


class Tile:

    def __init__(self, color, pos, index):
        self.color = color
        self.orig_position = pos
        self.x = pos[0]
        self.y = pos[1]
        self.index = index
        self.width = tile_size
        self.height = tile_size

    def is_out_of_frame(self):
        return \
            self.x < 0 - self.width and \
            (self.y < 0 - self.width or self.y > screen_height + self.height)

    def in_frame(self):
        return self.x + self.width > 0 and self.x - self.width < screen_width

    # Update the state of the tile
    def update(self, shift_x):
        self.x = self.orig_position[0] - shift_x

    # Draw the tile
    def draw(self):
        rect(self.color, self.x, self.y, tile_size, tile_size)


class StaticTile(Tile):

    def __init__(self, size, pos, surface, code, index):
        super().__init__(size, pos, index)
        self.image = surface
        self.code = code

    def draw(self):
        image(self.image, self.x, self.y, self.image.get_width() / tile_size)


class MovingTile(Tile, GameObject):

    def __init__(self, size, pos, surface, code, index):
        super().__init__(size, pos, index)
        self.tiles = None
        self.image = surface
        self.code = code
        self.speed = 1
        self.offset = 0
        self.gravity = 0.2
        self.direction = pygame.Vector2(0, 0)

    def draw(self):
        image(self.image, self.x, self.y, self.image.get_width() / tile_size)

    # Applying gravity
    def apply_gravity(self):
        if self.direction.y < 5:
            self.direction.y += self.gravity
        self.y += self.direction.y

    # Update the state of the tile
    def update(self, shift_x):
        super().update(shift_x)
        self.x += self.offset

    def collision(self, tiles):
        for i, tile in enumerate(tiles):

            if tile == self:
                continue

            # No collision when tile is part of backdrop
            if tile.code in BACKDROP_TILES:
                continue

                # Handle collision on left side of Link
            if self.collision_left(tile):
                if self.direction.x < 0:
                    self.speed *= -1
                    self.x = tile.x + tile.width / 2 + self.width / 2

            # Handle collision on right side of Link
            elif self.collision_right(tile):
                if self.direction.x > 0:
                    self.speed *= -1
                    self.x = tile.x - tile.width / 2 - self.width / 2

            # Handle collision on bottom side of tile
            if self.collision_bottom(tile):
                if self.direction.y > 0:
                    self.y = tile.y - tile.height / 2 - self.height / 2
                    self.direction.y = 0


class BreakableTile(StaticTile):

    def __init__(self, size, pos, surface, alt_surface, code, index):
        super().__init__(size, pos, surface, code, index)
        self.alt_surface = alt_surface
        self.break_sound = load_sound("assets/sounds/block_break.ogg")

    def break_tile(self, sky_tile_code):
        self.image = self.alt_surface
        self.code = sky_tile_code
        play_sound(self.break_sound, 1.5)


class MysteryBox(StaticTile):

    def __init__(self, size, pos, surface, alt_surface, code, loot, index):
        super().__init__(size, pos, surface, code, index)
        self.loot = loot
        self.alt_surface = alt_surface
        self.emptied = False

    def give_loot(self, level):
        if self.emptied:
            return

        if self.image != self.alt_surface:
            self.image = self.alt_surface

            self.loot.show(level)
            try:
                pass
            except:
                pass

        self.emptied = True
        return self.loot
