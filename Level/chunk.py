from Level.Tiles.tile_data import BACKDROP_TILES
from Loot.loot import Loot


class Chunk:

    def __init__(self, chunk_start, chunk_end, index):
        self.start = chunk_start
        self.end = chunk_end  # Chunk end is exclusive
        self.tiles = []
        self.monsters = []
        self.text_anomalies = []
        self.index = index

    # Update text anomaly buffer
    def update_text_anomalies(self, new_anomaly=None):
        # Add new anomaly to buffer
        if new_anomaly is not None:
            self.text_anomalies.append(new_anomaly)

        # Remove inactive text anomalies from buffer
        for msg in self.text_anomalies:
            if not msg.visible:
                self.text_anomalies.remove(msg)
                continue

            msg.update()

    def update_monsters(self, cam_pos, level_length):
        for monster in self.monsters:
            if monster.ready_to_remove():
                self.monsters.remove(monster)
            else:
                monster.update(cam_pos, level_length)

    def update_tiles(self, cam_pos):
        for tile in self.tiles:
            if tile.is_out_of_frame():
                self.tiles.remove(tile)
                continue

            tile.update(cam_pos)

    def update(self, cam_pos, level_length):
        self.update_monsters(cam_pos, level_length)
        self.update_tiles(cam_pos)
        self.update_text_anomalies()
