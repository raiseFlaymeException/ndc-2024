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
        self.jumpState = 0
        self.jumpHeight = config.PLAYER_JUMP_LIST[self.jumpState]
        self.jumpBoost = 1

    def animation(self):
        # jump animation
        if self.animeFrame > 0 and ((pyxel.frame_count % 2) == 0):
            self.animeFrame = ((self.animeFrame + 1) % 5) + 1
            self.jumpState += 1
        if not self.isInAir:  # si on touche le sol l'animation s'arrète
            self.animeFrame = 0
            self.jumpState = 0

    def _update_keys(self):
        for _ in range(self.speed):
            if pyxel.btn(config.KEY_LEFT) and self.dontCollideLeft():
                self.coords[0] -= 1
                self.direction = config.DIR_PLAYER_WEST
            if pyxel.btn(config.KEY_RIGHT) and self.dontCollideRight():
                self.coords[0] += 1
                self.direction = config.DIR_PLAYER_EAST
            if pyxel.btn(config.KEY_JUMP) and self.dontCollideUp() and \
                    not self.isInAir:
                self.coords[1] -= 1
                self.isInAir = True
                self.animeFrame = 1
                self.jumpState = 1
            for _ in range(((abs(self.jumpHeight)))*self.jumpBoost):
                if self.jumpHeight < 0:
                    if self.dontCollideUp():
                        self.coords[1] += 1*copysign(1, self.jumpHeight)
                    else:
                        self.jumpState = 5
                else:
                    if self.dontCollideDown():
                        self.coords[1] += 1*copysign(1, self.jumpHeight)
            if self.dontCollideDown():
                self.isInAir = True
                if self.jumpState == 0:
                    self.jumpState = 5
            else:
                self.jumpState = 0
                self.jumpHeight = config.PLAYER_JUMP_LIST[self.jumpState]

    def _execute_jump(self):
        if self.isInAir:
            if self.dontCollideUp():
                if self.jumpState < 5:
                    self.jumpHeight = config.PLAYER_JUMP_LIST[self.jumpState]
                else:
                    self.jumpHeight = config.PLAYER_JUMP_LIST[-1] # indice -1 = vitesse de chute finale
            elif self.dontCollideDown():
                self.jumpHeight = config.PLAYER_JUMP_LIST[-1]

        # implementation des jump pad
        # doit etre sur une tile
        if ((self.coords[1]+self.height) % 8) == 0:
            # si on peut pas aller en bas sa veut dire qu'il n'a pas de pad
            if not(self.dontCollideDown(COL_SPE)): # not(don't collide with) => collide with
                self.jumpBoost = 2
            else:
                self.jumpBoost = 1

    def move(self):
        # touches
        self._update_keys()
        # le jump
        self._execute_jump()
        # detection dans les airs
        if self.dontCollideDown():
            self.isInAir = True
        else:
            self.isInAir = False


    def dontCollideDown(self, colision_list=COL + COL_DOWN + COL_SPE):
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

    def dontCollideUp(self, colision_list=COL + COL_SPE):
        # fonction du turfu
        # on check le pixel à haut à droite et à gauche
        tilemap = pyxel.tilemaps[0]
        return not any(map(lambda x: x in colision_list,
                           [
                               tilemap.pget((self.coords[0])//8,
                                            (self.coords[1]-1)//8),
                               tilemap.pget((self.coords[0]+self.width-1)//8,
                                            (self.coords[1]-1)//8)
                           ]
                           ))

    def dontCollideLeft(self, colision_list=COL + COL_SPE):
        # fonction du turfu
        # on check le pixel à gauche en haut et en bas
        tilemap = pyxel.tilemaps[0]
        return not any(map(lambda x: x in colision_list,
                           [
                               tilemap.pget((self.coords[0]-1)//8,
                                            (self.coords[1])//8),
                               tilemap.pget((self.coords[0]-1)//8,
                                            (self.coords[1]+self.height-1)//8)
                           ]
                           ))

    def dontCollideRight(self, colision_list=COL + COL_SPE):
        # fonction du turfu
        # on check le pixel à droite en haut et en bas
        tilemap = pyxel.tilemaps[0]
        return not any(map(lambda x: x in colision_list,
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
