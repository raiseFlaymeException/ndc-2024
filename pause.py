import pyxel
import config
import sprites.PlayerClass
import sound


def draw_pause(player: sprites.PlayerClass) -> None:
    """dessine l'ecran de pause

    doit etre appeler dans draw

    Args:
        player (sprite.PlayerClass): le joueur qui permet de recentrer la
        camera
    """
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
def button_colide_with_mouse(b: tuple[int]) -> bool:
    """verifie si un bouton touche la souris

    verifie si le bouton b touche la souris

    Args:
        b (tuple[int]): le bouton a verifier

    Returns:
        (bool): True si le bouton touche la souris sinon False
    """
    return b[0] < pyxel.mouse_x + 1 and \
        b[0] + b[2] > pyxel.mouse_x and \
        b[1] < pyxel.mouse_y + 1 and \
        b[1] + b[3] > pyxel.mouse_y


def update_pause(state: int, sounds: sound.Sound) -> int:
    """update l'ecran de pause

    update l'ecran de pause en fonction de l'etat et coupe le son

    Args:
        state (int): l'etat du jeu
        sounds (sound.Sound): les sons (pour eteindre ceux ci)

    Returns:
        (int): le nouvelle etat du jeu
    """
    pyxel.mouse(True)
    if (button_colide_with_mouse(config.BUTTON_PLAY) and
            pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)):
        state = config.STATE_PLAY
        sounds.play_sound()
    elif pyxel.btn(config.KEY_PAUSE):
        state = config.STATE_PLAY_DISABLE_PAUSE
        sounds.play_sound()

    return state
