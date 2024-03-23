from Support.settings import tile_size, scale
from engine import text


class TextAnomaly:

    def __init__(self, pos, content, size, color):
        self.content = content
        self.x = pos[0]
        self.y = pos[1]
        self.timer = 1
        self.disappear_delay = 50
        self.visible = True
        self.size = size
        self.color = color
        self.speed = 0.5 * scale

    def update(self):
        if self.timer % self.disappear_delay == 0:
            self.visible = False

        self.y -= self.speed
        self.timer += 1

    def draw(self):
        if self.visible:
            text(str(self.content),
                 int(self.size * scale),
                 self.color,
                 self.x,
                 self.y - tile_size,
                 "fonts/pixel.ttf")
