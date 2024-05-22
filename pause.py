import pyxel
import config


def draw_pause(player):
    tm_pause = pyxel.tilemaps[1]  # la tilemap pause

    pyxel.bltm(player.real_x2camera_x(0), 0,
               tm_pause, 0, 0, config.WIDTH, config.HEIGHT, config.COLKEY)

    pyxel.text(player.real_x2camera_x(config.WIDTH/2-20),
               25, config.TITLE, config.COLOR_PLAY)

    pyxel.text(player.real_x2camera_x(config.TEXT_PAUSE_PLAY_X_OFF),
               config.TEXT_PAUSE_PLAY_Y_OFF, "PLAY", config.COLOR_PLAY)


# shema du funcionnement de button_colide_with_mouse:
# mouse_x + taille mouse_x (X) > à button x ([)
# [ X
# mouse_x (X) < à button x (.) + button width (])
# . X ]
# mouse_y + taille mouse_y (Y) > à button y ([)
# [ Y
# mouse_y (Y) < à button y (.) + button width (])
# . Y ]
def button_colide_with_mouse(b):
    return b[0] < pyxel.mouse_x + 1 and \
        b[0] + b[2] > pyxel.mouse_x and \
        b[1] < pyxel.mouse_y + 1 and \
        b[1] + b[3] > pyxel.mouse_y


def update_pause(state):
    pyxel.mouse(True)
    if button_colide_with_mouse(config.BUTTON_PLAY) and \
            pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
        state = config.STATE_PLAY
    return state
