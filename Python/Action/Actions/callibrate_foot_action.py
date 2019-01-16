from Action.action import Action
import subprocess


class CallibrateFootAction(Action):

    def initialize(self):
        self.set_image_path("Assets/Keys/callibrate_foot.png")
        return

    def on_pressed(self):
        self.set_image_path("Assets/Keys/callibrate_foot_pressed.png")
        subprocess.call(["C:/Program Files/AutoHotkey/AutoHotkey.exe", "C:/AHK/Functions/callibrate_foot.ahk"])

    def on_released(self):
        self.set_image_path("Assets/Keys/callibrate_foot.png")
