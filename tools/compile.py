import os

this_dir = os.path.dirname(__file__)
os.system(f"pyxel package {this_dir}\\.. {this_dir}\\..\\main.py")

app = f"{this_dir}\\..\\run.pyxapp"
if os.path.exists(app):
    os.remove(app)
os.rename("ndc-2024.pyxapp", app)
