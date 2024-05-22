import pyxel
import json


class Sound:
    def __init__(self, filepath):
        with open(filepath, "r") as f:
            self.sounds = json.load(f)

    def play_sound(self):
        for i, s in enumerate(self.sounds):
            pyxel.sounds[i].set(*s)
            pyxel.play(i, i, loop=True)
