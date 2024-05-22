import pyxel
import config
import pause
import sound
from KoopaClass import *
from PlayerClass import *


state = config.STATE_FIRST_LAUNCH
player = Player()
koopas = []


def draw():
    if state == config.STATE_PLAY:
        tm = pyxel.tilemaps[0]
        pyxel.cls(config.COLOR_BG)
        pyxel.bltm(0, 0, tm, 0, 0, 1024, config.HEIGHT, config.COLKEY)
        player.drawSprite()
        for koopa in koopas:
            koopa.draw()

    elif state==config.STATE_GAMEOVER:
        tm = pyxel.tilemaps[1]
        pyxel.bltm(player.real_x2camera_x(0), 0, tm, config.WIDTH, 0, config.WIDTH, config.HEIGHT)
        pyxel.text(player.real_x2camera_x(config.WIDTH/2-18), config.HEIGHT/2-2, "GAME OVER", pyxel.COLOR_RED)
    else:
        if state==config.STATE_FIRST_LAUNCH:
            pyxel.cls(config.COLOR_BG_MENU)
        else:
            tm = pyxel.tilemaps[0]
            pyxel.cls(config.COLOR_BG)
            pyxel.bltm(0, 0, tm, 0, 0, config.WIDTH, config.HEIGHT, config.COLKEY)
            player.drawSprite()
            for koopa in koopas:
                koopa.draw()
        pause.draw_pause(player)


def update():
    global state
    # pyxel.title(f"{pyxel.mouse_x}, {pyxel.mouse_y}")
    if player.coords[1] > 128:
        state = config.STATE_GAMEOVER
    if pyxel.btn(config.KEY_PAUSE):
        state = config.STATE_PAUSE

    if state == config.STATE_PLAY:
        player.mouvement()
        player.focus()
        player.animation()
        for koopa in koopas:
            koopa.update()
            if koopa.colide_with_player(player):
                state = config.STATE_GAMEOVER
    elif state==config.STATE_GAMEOVER:
        pass
    else:
        state = pause.update_pause(state)

def main():
    pyxel.init(config.WIDTH, config.HEIGHT, config.TITLE, config.FPS)

    pyxel.load("4.pyxres")

    player.focus()

    sound.play_sound()

    for koopa in config.KOOPAS:
        koopas.append(Koopa(*koopa))

    pyxel.run(update, draw)


main()