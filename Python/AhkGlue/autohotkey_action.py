from Action.CustomActions.custom_action import CustomAction
import os
import subprocess
from do_threaded import do_threaded

from watchdog.observers import Observer
from watchdog.events import FileModifiedEvent


class AutoHotkeyAction(CustomAction):

    def __init__(self, deck, action_id):

        f = open("AhkGlue/fileglue.ahk","r")
        gluetext = f.read()
        f.close()
        action_path = os.path.abspath('AhkGlue/CustomActions/{}/Action.ahk'.format(action_id))
        gluetext = gluetext.replace("${ActionPath}", action_path)

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

        class FileMessageHandler(FileModifiedEvent):

            def __init__(self, file_name, file_path, callback):
                self.file_path = file_path
                self.callback = callback
                super(FileMessageHandler, self).__init__(file_name)
                return

            def dispatch(self, event):
                if os.path.getsize(self.file_path) > 0:
                    f = open(self.file_path, "r")
                    msg = f.read()
                    f.close()
                    f = open(self.file_path, "w")
                    f.write("")
                    f.close()
                    self.callback(msg)
                return

        def on_msg_receive(msg):
            print("Received From Autohotkey: {}".format(msg))
            #self.deck.set_key_image_path()
            path = self.action_folder + "\\" + msg
            print(path)
            self.set_image_path(path)
            return

        event_handler = FileMessageHandler("image.pipe", self.action_folder + "\\image.pipe", on_msg_receive)
        observer = Observer()
        observer.schedule(event_handler, self.action_folder)
        observer.start()
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
        f = open(self.action_folder + "/events.pipe", "w")
        f.write("on_released")
        f.close()
        return

    def on_exit(self):
        self.proc.terminate()
        return



