import pyxel
import json


class Sound:
    """
    Une classe qui s'occupe des sons du jeu
    """

    def __init__(self, filepath: str) -> None:
        """init la classe Sound

        init la classe en ouvant filepath et en mettant les cursors à 0

        Args:
            filepath (str): le fichier json avec les infos sur la musique
        """
        with open(filepath, "r") as f:
            self.sounds = json.load(f)
        self.cursors = [0 for _ in self.sounds]

    def pause_sound(self) -> None:
        """met en pause le son qui est en cours

        met en pause le son et stock le curseur pour plus tard
        (voir play_sound)
        """
        cursors = []
        for i in range(len(self.sounds)):
            cur_pos = pyxel.play_pos(i)
            if cur_pos is None:  # la musique ne joue pas
                return
            cursors.append(cur_pos[1])
        # doit etre apres car si cur_pos est None
        # suprime l'ancienne valeur alors qu'il faut pas
        self.cursors = cursors
        pyxel.stop()

    def play_sound(self) -> None:
        """joue un son en boucle jusqu'a pause_sound

        commence le son ou il a ete mis en pause (voir pause_sound)
        """
        for i, s in enumerate(self.sounds):
            pyxel.sounds[i].set(*s)
            pyxel.play(i, i, tick=self.cursors[i], loop=True)
