import pyxel
import config
import pause
import sound

from sprites.PinguinClass import Pinguin
from sprites.PlayerClass import Player

# TODO: utiliser une meilleur maniere de gerer les etats

state = config.STATE_FIRST_LAUNCH
player = Player()
pinguins = []
sounds = sound.Sound("sounds.json")


def restart():
    global state
    state = config.STATE_PLAY
    player.__init__()


def draw_game():
    tm = pyxel.tilemaps[0]
    pyxel.cls(config.COLOR_BG)
    pyxel.bltm(0, 0, tm, 0, 0, 5000, config.HEIGHT, config.COLKEY)
    player.drawSprite()
    for pinguin in pinguins:
        pinguin.draw()


def draw():
    if state in (config.STATE_PLAY, config.STATE_PLAY_DISABLE_PAUSE):
        # modifier cette fonction quand on doit changer la maniere dont le jeu
        # est dessiner
        draw_game()

    elif state == config.STATE_GAMEOVER:
        tm = pyxel.tilemaps[1]
        pyxel.bltm(player.real_x2camera_x(0), 0, tm,
                   config.WIDTH, 0, config.WIDTH, config.HEIGHT)
        pyxel.text(player.real_x2camera_x(config.WIDTH/2-18),
                   config.HEIGHT/2-2, "GAME OVER", pyxel.COLOR_RED)
        pyxel.text(player.real_x2camera_x(config.WIDTH/2-13),
                   config.HEIGHT/2+30, "RESTART", pyxel.COLOR_RED)
        if pause.button_colide_with_mouse((48, 88, 80, 104)) and \
                pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            restart()
    else:
        if state == config.STATE_FIRST_LAUNCH:
            pyxel.cls(config.COLOR_BG_MENU)
        else:
            draw_game()
        pause.draw_pause(player)


def update():
    global state

    if player.coords[1] > 128:
        state = config.STATE_GAMEOVER

    if pyxel.btnr(config.KEY_PAUSE):
        # cette partie de code empeche la pause de reaparaitre quand on relache
        # pause
        if state == config.STATE_PLAY_DISABLE_PAUSE:
            state = config.STATE_PLAY
        else:
            state = config.STATE_PAUSE
            sounds.pause_sound()

    if state in (config.STATE_PLAY, config.STATE_PLAY_DISABLE_PAUSE):
        player.move()
        player.focus()
        player.animation()
        for pinguin in pinguins:
            pinguin.update()
            if pinguin.colide_with_player(player):
                state = config.STATE_GAMEOVER
    elif state in (config.STATE_PAUSE, config.STATE_FIRST_LAUNCH):
        state = pause.update_pause(state, sounds)


def main():
    pyxel.init(config.WIDTH, config.HEIGHT, config.TITLE, config.FPS)

    pyxel.load("res.pyxres")

    player.focus()

    sounds.play_sound()

    for pinguin in config.PINGUINS:
        pinguins.append(Pinguin(*pinguin))

    pyxel.run(update, draw)


if __name__ == "__main__":
    main()
