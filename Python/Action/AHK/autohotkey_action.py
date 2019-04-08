from threading import Lock

from Action.action import Action
import os
import subprocess
from Util.do_threaded import do_threaded

import time


class AutoHotkeyAction(Action):

    def __init__(self, deck, action_id):

        self.events_lock = Lock()
        
        event_names = ["initialize","on_visible","on_invisible","on_pressed","on_hold_down","on_released","on_update_sec","on_update","on_exit"]

        f = open("Action/AHK/ahkglue.ahk","r")
        gluetext = f.read()
        f.close()
        action_path = os.path.abspath('Action/CustomActions/{}/AutoHotkeyAction.ahk'.format(action_id))
        gluetext = gluetext.replace("${ActionPath}", action_path)

        f = open(action_path, "r")
        action_text = f.read()
        unused_func = "\n"
        for e in event_names:
            if not "{}(){{".format(e) in action_text:
                unused_func += "{}(){{\nreturn\n}}\n".format(e)
        gluetext = gluetext.replace("${DefinitionOfUnusedFunctions}", unused_func)

        self.action_folder = os.path.abspath('Action/CustomActions/{}/'.format(action_id))
        gluepath = self.action_folder+"/glue.ahk"
        f = open(gluepath,"w")
        f.write(gluetext)
        f.close()

        f = open(self.action_folder + "\\events.pipe", "w")
        f.write("")
        f.close()

        f = open(self.action_folder + "\\image.pipe", "w")
        f.write("")
        f.close()

        self.proc = subprocess.Popen("Action/AHK/AutoHotkeyU64.exe {}".format(gluepath))
        do_threaded(self.image_listener)

        super().__init__(deck)
        return

    def image_listener(self):

        # class FileMessageHandler(FileModifiedEvent):
        #
        #     def __init__(self, file_name, file_path, callback):
        #         self.file_path = file_path
        #         self.callback = callback
        #         super(FileMessageHandler, self).__init__(file_name)
        #         return
        #
        #     def dispatch(self, event):
        #         if os.path.getsize(self.file_path) > 0:
        #             f = open(self.file_path, "r")
        #             msg = f.read()
        #             print(msg)
        #             f.close()
        #             f = open(self.file_path, "w")
        #             f.write("")
        #             f.close()
        #             self.callback(msg)
        #         return
        #
        # def on_msg_receive(msg):
        #     # print("Received From Autohotkey: {}".format(msg))
        #     path = self.action_folder + "\\" + msg
        #     self.set_image_path(path)
        #     return
        #
        # event_handler = FileMessageHandler("image.pipe", self.action_folder + "\\image.pipe", on_msg_receive)
        # observer = Observer()
        # observer.schedule(event_handler, self.action_folder)
        # observer.start()
        #

        while True:
            path = self.action_folder + "/image.pipe"
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) == 0:
                time.sleep(0.005)

            f = open(path, "r")
            msg = f.read()
            f.close()
            f = open(path, "w")
            f.write("")
            f.close()
            print("Received From Autohotkey: {}".format(msg))
            image_path = self.action_folder + "\\" + msg
            self.set_image_path(image_path)

        return

    

    def initialize(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("initialize")
            f.close()

        return

    def on_pressed(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("on_pressed")
            f.close()
        return

    def on_hold_down(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("on_hold_down")
            f.close()
        return

    def on_released(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("on_released")
            f.close()
        return

    def on_visible(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("on_visible")
            f.close()
        return

    def on_invisible(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("on_invisible")
            f.close()
        return

    def on_update_sec(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("on_update_sec")
            f.close()
        return

    def on_update(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("on_update")
            f.close()
        return

    def on_exit(self):
        path = self.action_folder + "/events.pipe"
        
        with self.events_lock:
            while not os.path.isfile(path):
                time.sleep(0.005)

            while os.path.getsize(path) > 0:
                time.sleep(0.005)

            f = open(path, "w")
            f.write("on_exit")
            f.close()
        self.proc.terminate()
        return
