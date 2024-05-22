from math import copysign

import pyxel

import config

COL = config.COLISION_LIST
COL_DOWN = config.COLISION_LIST_ONLY_DOWN
COL_SPE = config.COLISION_LIST_SPE


class Player():
    def __init__(self):
        self.coords = [0, 0]
        self.animeFrame = 1
        self.width = 6
        self.height = 7
        self.direction = config.DIR_PLAYER_EAST
        self.speed = 1
        self.isInAir = True
        self.jumpHeight = 0
        self.jumpState = 0
        self.jumpBoost = 1

    def animation(self):
        # jump animation
        if self.animeFrame > 0:
            self.animeFrame = ((self.animeFrame + 1) % 5) + 1
            self.jumpState += 1
        if not self.isInAir:  # si on touche le sol l'animation s'arrète
            self.animeFrame = 0
            self.jumpState = 0

    def _update_keys(self):
        for _ in range(self.speed):
            if pyxel.btn(config.KEY_LEFT) and self.canGoLeft():
                self.coords[0] -= 1
                self.direction = config.DIR_PLAYER_WEST
            if pyxel.btn(config.KEY_RIGHT) and self.canGoRight():
                self.coords[0] += 1
                self.direction = config.DIR_PLAYER_EAST
            if pyxel.btn(config.KEY_JUMP) and self.canGoUp() and \
                    not self.isInAir:
                self.coords[1] -= 1
                self.isInAir = True
                self.animeFrame = 1
                self.jumpState = 1
            for _ in range(((abs(self.jumpHeight)))*self.jumpBoost):
                if self.jumpHeight < 0:
                    if self.canGoUp():
                        self.coords[1] += 1*copysign(1, self.jumpHeight)
                else:
                    if self.canGoDown():
                        self.coords[1] += 1*copysign(1, self.jumpHeight)
            if self.canGoDown():
                self.isInAir = True
            else:
                self.jumpHeight = 0

    def _execute_jump(self):
        if self.isInAir:
            if self.canGoUp():
                if self.jumpState == 1:
                    self.jumpHeight = -3
                elif self.jumpState == 2:
                    self.jumpHeight = -5
                elif self.jumpState == 3:
                    self.jumpHeight = -7
                elif self.jumpState == 4:
                    self.jumpHeight = -3
                elif self.jumpState == 5:
                    self.jumpHeight = -1
                elif self.canGoDown():
                    self.jumpBoost = 1
                    self.jumpHeight = +2
            elif self.canGoDown():
                self.jumpHeight = +2

        # implementation des jump pad
        if self.canGoDown(COL_SPE):
            self.jumpBoost = 2
        elif self.canGoDown(COL+COL_DOWN):
            self.jumpBoost = 1

    def move(self):
        # touches
        self._update_keys()
        # le jump
        self._execute_jump()

    def canGoDown(self, colision_list=None):
        if colision_list is None:
            colision_list = COL + COL_DOWN + COL_SPE
        # on vérifie les collision seulement si le joueur est sur une tile
        # (ses pieds touchent les pixels les plus hauts de la tile)
        if ((self.coords[1]+self.height) % 8) != 0:
            return True
        # fonction du turfu
        # (la division par 8 sert à faire la conversion des coordonée du
        # joueur au coordonnées des tiles)
        # on check le pixel à en bas à droite et à gauche
        tilemap = pyxel.tilemaps[0]
        return not any(map(lambda x: x in colision_list,
                           [
                               tilemap.pget((self.coords[0])//8,
                                            (self.coords[1]+self.height)//8),
                               tilemap.pget((self.coords[0]+self.width-1)//8,
                                            (self.coords[1]+self.height)//8)
                           ]
                           ))

    def canGoUp(self, colision_list=None):
        if colision_list is None:
            colision_list = COL + COL_DOWN + COL_SPE
        # TODO: bouger ce truc en dehors de la fonction
        if self.canGoDown():
            self.isInAir = True
        else:
            self.isInAir = False

        # fonction du turfu
        # on check le pixel à haut à droite et à gauche
        tilemap = pyxel.tilemaps[0]
        return not any(map(lambda x: x in COL + COL_SPE,
                           [
                               tilemap.pget((self.coords[0])//8,
                                            (self.coords[1]-1)//8),
                               tilemap.pget((self.coords[0]+self.width-1)//8,
                                            (self.coords[1]-1)//8)
                           ]
                           ))

    def canGoLeft(self, colision_list=None):
        if colision_list is None:
            colision_list = COL + COL_DOWN + COL_SPE
        # fonction du turfu
        # on check le pixel à gauche en haut et en bas
        tilemap = pyxel.tilemaps[0]
        return not any(map(lambda x: x in COL + COL_SPE,
                           [
                               tilemap.pget((self.coords[0]-1)//8,
                                            (self.coords[1])//8),
                               tilemap.pget((self.coords[0]-1)//8,
                                            (self.coords[1]+self.height-1)//8)
                           ]
                           ))

    def canGoRight(self, colision_list=None):
        if colision_list is None:
            colision_list = COL + COL_DOWN + COL_SPE
        # fonction du turfu
        # on check le pixel à droite en haut et en bas
        tilemap = pyxel.tilemaps[0]
        return not any(map(lambda x: x in COL + COL_SPE,
                           [
                               tilemap.pget((self.coords[0]+self.width)//8,
                                            (self.coords[1])//8),
                               tilemap.pget((self.coords[0]+self.width)//8,
                                            (self.coords[1]+self.height-1)//8)
                           ]
                           ))

    def focus(self):
        pyxel.camera(self.coords[0]-64+(self.width//2), 0)

    def drawSprite(self):
        if self.direction == config.DIR_PLAYER_EAST:
            v = 17
        else:
            v = 17 + 8
        pyxel.blt(self.coords[0], self.coords[1], 0, 1+8 *
                  self.animeFrame, v, self.width, self.height, config.COLKEY)

    def real_x2camera_x(self, x):
        return self.coords[0]-64+(self.width//2)+x
