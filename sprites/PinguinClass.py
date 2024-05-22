import pyxel

import config

COL = config.COLISION_LIST
COL_SPE = config.COLISION_LIST_SPE


class Pinguin:
    def __init__(self, x1, y, x2):
        self.x1 = x1
        self.x2 = x2
        self.x = x1
        self.y = y
        self.dir = 0
        self.anim = 0

    def update(self):
        if pyxel.frame_count % config.PINGUIN_SPEED_DIV == 0:
            if self.dir == 0:
                for _ in range(config.PINGUIN_SPEED):
                    if self.x == self.x2:
                        self.dir = 1
                        return
                    self.x += 1
            else:
                for _ in range(config.PINGUIN_SPEED):
                    if self.x == self.x1:
                        self.dir = 0
                        return
                    self.x -= 1
            self.anim = (self.anim+1) % 2

    def colide_with_player(self, player):
        return player.coords[0] < self.x + 8 and \
            player.coords[0] + player.width > self.x and \
            player.coords[1] < self.y + 8 and \
            player.coords[1] + player.height > self.y

    def draw(self):
        img_pinguin = pyxel.images[0]
        pyxel.blt(self.x, self.y, img_pinguin, config.PINGUIN_IMG_OFFSET_X +
                  self.anim*8, config.PINGUIN_IMG_OFFSET_Y+self.dir*8, 8, 8,
                  config.COLKEY)
