import random

# Environment
from Environment.cloud import Cloud

# GameObject
from GameObject.Link.link import Link
from GameObject.Monster.bokoblin import Bokoblin
from GameObject.Monster.donkey_kong import DonkeyKong
from GameObject.Monster.ganondorf import Ganondorf
from GameObject.Monster.ghost import Ghost

# Level helpers
from Level.Tiles.tile import StaticTile, MysteryBox, MovingTile, BreakableTile
from Level.Tiles.tile_data import *
from Level.chunk import Chunk
from Level.triforce import Triforce

# Loot
from Loot.cherry import Cherry
from Loot.coin import Coin
from Loot.extra_life import ExtraLife
from Loot.fire_flower import FireFlower
from Loot.loot import Loot

# Support
from Support.settings import tile_size, screen_width, screen_height, scale
from Support.support import import_level_data, import_tile_set
from Support.input import *
from engine import *


class Level:

    def __init__(self,
                 level_name,
                 chunk_amount,
                 level_music_path,
                 level_backdrop_color=(0, 0, 0),
                 clouds_enabled=True):
        # Properties
        self.level_length = None
        self.level_data = None
        self.screen = None
        self.level_name = level_name
        self.cam_pos = 0
        self.link = Link((100, screen_height / 2), 32 * scale, 64 * scale)
        self.backdrop_color = level_backdrop_color
        self.end_game_triforce = None
        self.chunk_amount = chunk_amount
        self.chunk_size = None

        # Clouds
        self.cloud_image = load_image("other/cloud.png")
        self.clouds_enabled = clouds_enabled
        self.clouds_amount = 10

        # Collections
        self.chunks = []
        self.environment = []

        # Music
        self.level_music = load_sound(level_music_path)
        self.level_music_started = False

    def get_right_sky_tile(self):
        if self.backdrop_color == (0, 0, 0):
            return CASTLE_WALL
        else:
            return SKY_TILE

    def init_tile(self, tile, tile_set, pos, i, j, chunk):

        # Initialize player
        if tile == PLAYER_TILE:
            sel_tile = tile_set[0]
            chunk.tiles.append(StaticTile(tile_size, pos, sel_tile, tile, len(chunk.tiles)))
            self.link.x = pos[0]
            self.link.y = pos[1]

        # Initialize mystery boxes
        elif tile == MYSTERY_BOX:
            # Setup loot
            loot_code = self.level_data[j + 1][i]
            loot = self.init_loot(loot_code, tile_set, pos, len(chunk.tiles))

            # Setup tile
            self.level_data[j + 1][i] = self.get_right_sky_tile()
            sel_tile = tile_set[int(tile)]
            alt_tile = tile_set[int(EMPTY_BOX)]
            chunk.tiles.append(MysteryBox(tile_size, pos, sel_tile, alt_tile, tile, loot, len(chunk.tiles)))

        # Initialize monsters
        elif tile in MONSTERS:
            self.init_monster(tile, pos, chunk)

            # Make sky tile
            sel_tile = tile_set[int(self.get_right_sky_tile())]
            chunk.tiles.append(StaticTile(tile_size, pos, sel_tile, self.get_right_sky_tile(), len(chunk.tiles)))

        # Initialize breakable tiles
        elif tile in BREAKABLE:
            sel_tile = tile_set[int(tile)]
            alt_tile = tile_set[int(self.get_right_sky_tile())]
            chunk.tiles.append(BreakableTile(tile_size, pos, sel_tile, alt_tile, tile, len(chunk.tiles)))

        # Initialize end of game
        elif tile == END_OF_GAME:
            # Make end-of-game
            self.end_game_triforce = Triforce((pos[0], 230 * scale), 481 * scale, 371 * scale, self.link)

            # Make sky tile
            sel_tile = tile_set[int(self.get_right_sky_tile())]
            chunk.tiles.append(StaticTile(tile_size, pos, sel_tile, self.get_right_sky_tile(), len(chunk.tiles)))

        # Initialize normal static tiles
        else:
            sel_tile = tile_set[int(tile)]
            chunk.tiles.append(StaticTile(tile_size, pos, sel_tile, tile, len(chunk.tiles)))

    def init_link(self, new_link):
        self.link = new_link

    def transition_requested(self):
        return self.link.die_animation_timer >= self.link.die_animation_delay or \
            self.end_game_triforce.reached

    def init_chunks(self):
        self.chunk_size = round(self.level_length / self.chunk_amount)

        for i in range(self.chunk_amount):
            chunk_end = (i + 1) * self.chunk_size

            # Make sure last chunk is not too long
            if chunk_end > self.level_length:
                chunk_end = self.level_length

            # Make chunk
            self.chunks.append(Chunk(i * self.chunk_size, chunk_end, i))

    # Determine chunk the player is currently in
    def get_current_chunk(self):
        for chunk in self.chunks:
            if chunk.start <= self.link.x + self.cam_pos <= chunk.end:
                return chunk

    # Determine the chunks to draw
    def get_chunks_in_range(self):
        chunks_to_draw = []

        # Determine the chunks to draw
        for i, chunk in enumerate(self.chunks):
            if chunk.start < self.link.x + self.cam_pos + screen_width and \
                    not chunk.end < self.link.x + self.cam_pos - screen_width:
                chunks_to_draw.append(chunk)

        return chunks_to_draw

    # Initialize level
    def setup(self, game_screen):
        self.screen = game_screen
        self.level_data = import_level_data(f"Maps/level_{self.level_name}.csv")
        self.level_length = len(self.level_data[0] * tile_size)
        self.init_chunks()
        self.environment = []
        self.init_environmental_objects(self.cam_pos)
        tile_set = import_tile_set("Maps/tileset.png")

        # Initial y-coordinate of tile
        y = tile_size / 2

        # Read tiles into tiles list
        for j, row in enumerate(self.level_data):

            # Initial x-coordinate of tile
            x = tile_size / 2

            # Current chunk index
            current_chunk_index = 0
            tile_index = 0

            for i, tile in enumerate(row):
                pos = (x, y)

                if x > self.chunks[current_chunk_index].end:
                    current_chunk_index += 1
                    tile_index = 0

                # Treat different tiles correctly
                if tile == SKY_TILE or tile == CASTLE_WALL:
                    pass

                # Treat different tiles correctly
                self.init_tile(tile, tile_set, pos, i, j, self.chunks[current_chunk_index])

                # Update tile x-coordinate & tile index
                x += tile_size
                tile_index += 1

            # Update tile y-coordinate
            y += tile_size

    # Make new monster object and add it to the list of monsters
    def init_monster(self, tile_code, pos, chunk):
        if tile_code == BOKOBLIN:
            chunk.monsters.append(Bokoblin(pos, 16 * 3 * scale, 16 * 3 * scale, self.link, self, chunk))
        elif tile_code == GHOST:
            chunk.monsters.append(Ghost(pos, 48 * scale, 48 * scale, self.link, self, chunk))
        elif tile_code == DONKEY_KONG:
            chunk.monsters.append(DonkeyKong(pos, 46 * 3 * scale, 32 * 3 * scale, self.link, self, chunk))
        elif tile_code == GANONDORF:
            chunk.monsters.append(Ganondorf(pos, 46 * 1.5 * scale, 65 * 1.5 * scale, self.link, self, chunk))

    # Make loot object to be added to the world
    def init_loot(self, loot_code, tile_set, pos, tile_index):
        loot_tile = tile_set[int(loot_code)]

        # Determine loot type
        if loot_code == COIN:
            loot = Coin(tile_size, pos, loot_tile, loot_code, self.link, tile_index)
        elif loot_code == EXTRA_LIFE:
            loot = ExtraLife(tile_size, pos, loot_tile, loot_code, self.link, tile_index)
        elif loot_code == FIRE_MARIO:
            loot = FireFlower(tile_size, pos, loot_tile, loot_code, self.link, tile_index)
        elif loot_code == PAC_MAN:
            loot = Cherry(tile_size, pos, loot_tile, loot_code, self.link, tile_index)
        else:
            loot = Coin(tile_size, pos, loot_tile, loot_code, self.link, tile_index)

        return loot

    # Update the camera position
    def world_shift(self):
        if self.link.killed:
            return

        if (self.link.x >= screen_width / 2 and
                not move_left_key_pressed() and not
                self.link.direction.x <= 0):
            self.cam_pos += self.link.direction.x * self.link.speed

    # Handle collision
    def handle_collision(self):
        chunks_to_draw = self.get_chunks_in_range()

        # Gather all tiles to check for collision
        tiles_to_check = []
        for chunk in chunks_to_draw:
            tiles_to_check.extend(chunk.tiles)

        # Sort list so that tiles with parent type Loot are checked first
        tiles_to_check.sort(key=lambda x: issubclass(type(x), Loot), reverse=True)

        # Check for collision
        link_is_grounded = False

        for i, tile in enumerate(tiles_to_check):

            # No collision when tile is part of backdrop
            if tile.code in BACKDROP_TILES:
                continue

            # Moving tiles collision
            if issubclass(type(tile), MovingTile):
                tile.collision(tiles_to_check)

            # Monsters collision
            for chunk in chunks_to_draw:
                for monster in chunk.monsters:
                    monster.handle_collision(tile, i, self)

            # Link collision
            self.link.handle_collision(tile, i, self)
            if not link_is_grounded:
                if self.link.collision_bottom(tile):
                    link_is_grounded = True

        # Update link's grounded state
        self.link.is_grounded = link_is_grounded

    # Check whether shift of the tiles should be prevented
    def prevent_tile_shift(self):
        return (self.cam_pos <= 0 and self.link.direction.x < 0) or \
            (self.cam_pos >= (self.level_length - screen_width) and
             self.link.direction.x > 0)

    def reset(self):
        # Properties
        self.cam_pos = 0
        self.clouds_enabled = settings.clouds

        # Reset link for new level
        self.link.soft_reset()

        # Collections
        self.chunks = []

        # Execute setup again to reset map
        self.setup(self.screen)

    def init_environmental_objects(self, cam_pos):
        if not self.clouds_enabled:
            self.clouds_amount = 0

        # Add clouds in current view
        for i in range(self.clouds_amount):
            cloud = Cloud(self.cloud_image, cam_pos)
            cloud.orig_pos = (random.randint(0, screen_width + 100),
                              random.randint(0, 100))
            self.environment.append(cloud)

    def update_environmental_objects(self, cam_pos, level_length):
        clouds_amount = 0

        # Remove/update clouds
        for obj in self.environment:
            if obj.ready_to_remove():
                self.environment.remove(obj)
            else:
                if type(obj) == Cloud:
                    clouds_amount += 1
                obj.update(cam_pos, level_length)

        # Add clouds when needed
        if clouds_amount < self.clouds_amount:
            self.environment.append(Cloud(self.cloud_image, cam_pos))

    # Update the state of the level
    def update(self):
        # Stop music if game is over
        if self.transition_requested():
            self.level_music.fadeout(500)

        # Reset the game when the level endpoint is reached
        if self.end_game_triforce.reached:
            self.reset()

        # Update chunks to draw
        chunks_to_draw = self.get_chunks_in_range()
        for chunk in chunks_to_draw:
            chunk.update(self.cam_pos, self.level_length)

        # == Player
        self.link.update(self.cam_pos, self, self.end_game_triforce.reached)

        # Manage world shift
        if not self.prevent_tile_shift():
            self.world_shift()

        # Other
        self.end_game_triforce.update(self.cam_pos, self.level_length)
        self.update_environmental_objects(self.cam_pos, self.level_length)

        # Play music
        if not self.level_music.get_num_channels() > 0:
            self.level_music.play(-1)
            self.level_music.set_volume(0.25 * settings.volume)

        # Fade out music when transition is requested
        if self.transition_requested():
            self.level_music.fadeout(500)

        # Collision
        self.handle_collision()

    def draw_environmental_objects(self):
        for obj in self.environment:
            if obj.in_frame():
                obj.draw()

    def draw_tiles(self, chunks_to_draw):
        backdrop_tiles = []
        loot_tiles = []
        other_tiles = []

        # Gather all tiles to draw
        for chunk in chunks_to_draw:
            for tile in chunk.tiles:
                if tile.code in BACKDROP_TILES:
                    backdrop_tiles.append(tile)
                elif isinstance(tile, Loot):
                    loot_tiles.append(tile)
                else:
                    other_tiles.append(tile)

        # Draw backdrop tiles first
        for tile in backdrop_tiles:
            tile.draw()

        self.draw_environmental_objects()

        # Draw loot
        for tile in loot_tiles:
            tile.draw()

        # Draw other tiles
        for tile in other_tiles:
            tile.draw()

    @staticmethod
    def draw_monsters(chunks_to_draw):
        # Gather all monsters to draw in a list
        monsters_to_draw = []
        for chunk in chunks_to_draw:
            monsters_to_draw.extend(chunk.monsters)

        # Draw monsters
        for monster in monsters_to_draw:
            monster.draw()

    @staticmethod
    def draw_text_anomalies(chunks_to_draw):
        # Gather all text anomalies to draw in a list
        text_anomalies_to_draw = []
        for chunk in chunks_to_draw:
            text_anomalies_to_draw.extend(chunk.text_anomalies)

        # Draw text anomalies
        for text_anomaly in text_anomalies_to_draw:
            text_anomaly.draw()

    def draw_environment(self):
        chunks_to_draw = self.get_chunks_in_range()
        self.draw_tiles(chunks_to_draw)
        self.draw_monsters(chunks_to_draw)
        self.draw_text_anomalies(chunks_to_draw)

    # Draw the state of the level
    def draw(self):

        # == Backdrop
        backdrop(self.backdrop_color)

        # Draw environment
        self.draw_environment()

        # Draw end game triforce
        self.end_game_triforce.draw()

        # == Player
        self.link.draw()

        # Coin amount
        text(f"COINS: {str(self.link.coins + self.link.coins_earned_current_level)}",
             int(scale * 25),
             (255, 255, 255),
             (100 * scale),
             (25 * scale),
             "fonts/pixel.ttf")

        # Lives amount
        text(f"LIVES: {str(self.link.lives)}",
             int(scale * 25),
             (255, 255, 255),
             screen_width / 2 + 10 * scale,
             25 * scale,
             "fonts/pixel.ttf")

        # World number
        text(f"WORLD: {str(self.level_name)}",
             int(scale * 25),
             (255, 255, 255),
             screen_width / 2 + 300 * scale,
             25 * scale,
             "fonts/pixel.ttf")
