from config import COLISION_LIST as COL
from config import COLISION_LIST_ONLY_DOWN as COL_DOWN
from config import COLISION_LIST_SPE as COL_SPE
from config import KEY_JUMP, KEY_LEFT, KEY_RIGHT, COLKEY
import pyxel
from math import copysign

class Player():
    def __init__(self):
        self.coords = [0,0]
        self.animeFrame = 1
        self.width = 6
        self.height = 7
        self.direction = "east"
        self.speed = 1
        self.isInAir = True
        self.jumpHeight = 0
        self.jumpState = 0
        self.jumpBoost = 1
    def animation(self):
        # jump animation
        if self.animeFrame > 0:
            self.animeFrame = ((self.animeFrame + 1) % 5) +1
            self.jumpState += 1
        if not(self.isInAir): # si on touche le sol l'animation s'arrète
            self.animeFrame = 0
            self.jumpState = 0
    def mouvement(self):
        # touches
        for _ in range(self.speed):
            if pyxel.btn(KEY_LEFT) and self.canGoLeft():
                self.coords[0] -= 1
                self.direction = "west"
            if pyxel.btn(KEY_RIGHT) and self.canGoRight():
                self.coords[0] += 1
                self.direction = "east"
            if pyxel.btn(KEY_JUMP) and self.canGoUp() and not(self.isInAir):
                self.coords[1] -= 1
                self.isInAir = True
                self.animeFrame = 1
                self.jumpState = 1
                print("jump")
            for _ in range(((abs(self.jumpHeight)))*self.jumpBoost):
                if self.jumpHeight < 0:
                    if self.canGoUp():
                        self.coords[1] += 1*copysign(1,self.jumpHeight)
                else:
                    if self.canGoDown():
                        self.coords[1] += 1*copysign(1,self.jumpHeight)
            if self.canGoDown():
                self.isInAir = True
            else:
                self.jumpHeight = 0
        # le jump
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
        if (((self.coords[1]+self.height)%8) == 0) and any(map(lambda x: x in COL_SPE, # implementation des jump pad
            [pyxel.tilemaps[0].pget((self.coords[0])//8,(self.coords[1]+self.height)//8), # on check le pixel en dessous à gauche
            pyxel.tilemaps[0].pget((self.coords[0]+self.width-1)//8,(self.coords[1]+self.height)//8)] # on check le pixel en dessous à droite
            )):
            self.jumpBoost = 2
        elif (((self.coords[1]+self.height)%8) == 0) and any(map(lambda x: x in COL+COL_DOWN, # implementation des jump pad
            [pyxel.tilemaps[0].pget((self.coords[0])//8,(self.coords[1]+self.height)//8), # on check le pixel en dessous à gauche
            pyxel.tilemaps[0].pget((self.coords[0]+self.width-1)//8,(self.coords[1]+self.height)//8)] # on check le pixel en dessous à droite
            )):
            self.jumpBoost = 1
    def canGoDown(self):
        if ((self.coords[1]+self.height)%8) == 0: # on vérifie les collision seulement si le joueur est sur une tile (ses pieds touchent les pixels les plus hauts de la tile)
            return not(any(map(lambda x: x in COL+COL_DOWN+COL_SPE, # fonction du turfu (la division par 8 sert à faire la conversion des coordonée du joueur au coordonnées des tiles)
            [pyxel.tilemaps[0].pget((self.coords[0])//8,(self.coords[1]+self.height)//8), # on check le pixel en dessous à gauche
            pyxel.tilemaps[0].pget((self.coords[0]+self.width-1)//8,(self.coords[1]+self.height)//8)] # on check le pixel en dessous à droite
            )))
        else:
            return True
            
    def canGoUp(self):
        if self.canGoDown():
            self.isInAir = True
        else:
            self.isInAir = False
        return not(any(map(lambda x: x in COL+COL_SPE, # fonction du turfu
            [pyxel.tilemaps[0].pget((self.coords[0])//8,(self.coords[1]-1)//8), # on check le pixel au dessus à gauche
            pyxel.tilemaps[0].pget((self.coords[0]+self.width-1)//8,(self.coords[1]-1)//8)] # on check le pixel au dessus à droite
            )))
    def canGoLeft(self):
        return not(any(map(lambda x: x in COL+COL_SPE, # fonction du turfu
            [pyxel.tilemaps[0].pget((self.coords[0]-1)//8,(self.coords[1])//8), # on check le pixel à gauche en haut
            pyxel.tilemaps[0].pget((self.coords[0]-1)//8,(self.coords[1]+self.height-1)//8)] # on check le pixel à gauche en bas
            )))
    def canGoRight(self):
        return not(any(map(lambda x: x in COL+COL_SPE, # fonction du turfu
            [pyxel.tilemaps[0].pget((self.coords[0]+self.width)//8,(self.coords[1])//8), # on check le pixel à droite en haut
            pyxel.tilemaps[0].pget((self.coords[0]+self.width)//8,(self.coords[1]+self.height-1)//8)] # on check le pixel à droite en bas
            )))
    def focus(self):
        pyxel.camera(self.coords[0]-64+(self.width//2),0)
    def drawSprite(self):
        if self.direction == "east":
            v = 17
        else:
            v = 17 + 8
        pyxel.blt(self.coords[0], self.coords[1], 0, 1+8*self.animeFrame, v, self.width, self.height, COLKEY)

    
    def real_x2camera_x(self, x):
        return self.coords[0]-64+(self.width//2)+x