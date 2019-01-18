from Action.CustomActions.custom_action import CustomAction
import os
import subprocess
from do_threaded import do_threaded

class AutoHotkeyAction(CustomAction):

    def __init__(self, deck, action_id):

        f = open("AhkGlue/fileglue.ahk","r")
        gluetext = f.read()
        f.close()
        action_path = os.path.abspath('AhkGlue/CustomActions/{}/Action.ahk'.format(action_id))
        gluetext = gluetext.replace("${ActionPath}",action_path)

        self.action_folder = os.path.abspath('AhkGlue/CustomActions/{}/'.format(action_id))
        gluepath = self.action_folder+"/glue.ahk"
        f = open(gluepath,"w")
        f.write(gluetext)
        f.close()

        self.proc = subprocess.Popen("AhkGlue/AutoHotkey/AutoHotkeyU64.exe {}".format(gluepath))
        do_threaded(self.image_listener)

        super().__init__(deck)
        return

    def image_listener(self):
        while (True):
            # TODO
            pass

        return

    def initialize(self):
        # TODO wait for file empty
        f = open(self.action_folder + "/events.pipe", "w")
        f.write("initialize")
        f.close()
        return

    def on_pressed(self):
        f = open(self.action_folder + "/events.pipe", "w")
        f.write("on_pressed")
        f.close()
        return

    def on_released(self):
        return

    def on_exit(self):
        self.proc.terminate()
        return



