import pyxel
from config import *

def draw_pause(player):
    tm_pause = pyxel.tilemaps[1] # la tilemap pause

    pyxel.bltm(player.real_x2camera_x(0), 0, tm_pause, 0, 0, WIDTH, HEIGHT, COLKEY)

    pyxel.text(player.real_x2camera_x(WIDTH/2-20), 25, TITLE, COLOR_PLAY)

    pyxel.text(player.real_x2camera_x(TEXT_PAUSE_PLAY_X_OFF), TEXT_PAUSE_PLAY_Y_OFF, "PLAY", COLOR_PLAY)



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
    if button_colide_with_mouse(BUTTON_PLAY) and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
        state = STATE_PLAY
    return state