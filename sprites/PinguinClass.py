import pyxel

import config
import sprites.PlayerClass

COL = config.COLISION_LIST
COL_SPE = config.COLISION_LIST_SPE


class Pinguin:
    """
    l'ennemi pinguin
    """

    def __init__(self, x1: int, y: int, x2: int) -> None:
        """initialize le pinguin

        le pinguin va de (x1, y) a (x2, y) puis refais le chemin inverse

        Args:
            x1 (int): la coordonnee x de la position de depart du pinguin
            y (int): la coordonne y du pinguin
            x2 (int): la coordonnee x de la position de fin du pinguin
        """
        self.x1 = x1
        self.x2 = x2
        self.x = x1
        self.y = y
        self.dir = 0
        self.anim = 0

    def update(self) -> None:
        """update le pinguin

        fait avancer le pinguin vers (x1, y) ou (x2, y) en fonction de self.dir
        """
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

    def colide_with_player(self, player: sprites.PlayerClass) -> bool:
        """verifie si le pinguin touche le joueur

        verifie si le rectangle du joueur est dans le rectangle du pinguin
        (voir shema de button_colide_with_mouse dans pause.py)

        Args:
            player (sprites.PlayerClass): le joueur a verifier

        Returns:
            (bool): True si le pinguin touche le joueur sinon False
        """
        return player.coords[0] < self.x + 8 and \
            player.coords[0] + player.width > self.x and \
            player.coords[1] < self.y + 8 and \
            player.coords[1] + player.height > self.y

    def draw(self) -> None:
        """dessine le pinguin sur l'ecran"""
        img_pinguin = pyxel.images[0]
        pyxel.blt(self.x, self.y, img_pinguin, config.PINGUIN_IMG_OFFSET_X +
                  self.anim*8, config.PINGUIN_IMG_OFFSET_Y+self.dir*8, 8, 8,
                  config.COLKEY)
