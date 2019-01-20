from Action.action import Action
import os
import subprocess
from do_threaded import do_threaded

from watchdog.observers import Observer
from watchdog.events import FileModifiedEvent


class Python3Action(Action):

    def __init__(self, deck, action_id):

        event_names = ["initialize", "on_visible", "on_invisible", "on_pressed", "on_hold_down", "on_released", "on_update_sec", "on_update", "on_exit"]

        f = open("Action/Python3/py3glue.py", "r")
        gluetext = f.read()
        f.close()
        action_path = os.path.abspath('Action/CustomActions/{}/Python3Action.py'.format(action_id))

        # f = open(action_path, "r")
        # action_text = f.read()
        # unused_func = "\n"
        # for e in event_names:
        #     if not "{}(){{".format(e) in action_text:
        #         unused_func += "{}(){{\nreturn\n}}\n".format(e)
        # gluetext = gluetext.replace("${DefinitionOfUnusedFunctions}", unused_func)

        self.action_folder = os.path.abspath('Action/CustomActions/{}/'.format(action_id))
        gluepath = self.action_folder+"/glue.py"
        f = open(gluepath, "w")
        f.write(gluetext)
        f.close()

        self.proc = subprocess.Popen("Action/Python3/venv/Scripts/python.exe {}".format(gluepath),
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE)

        do_threaded(self.image_listener)

        super().__init__(deck)
        return

    def image_listener(self):

        def on_msg_receive(msg):
            path = self.action_folder + "\\" + msg
            self.set_image_path(path)
            return

        while True:
            line = self.proc.stdout.readline()
            if len(line) > 0:
                line = line.decode("utf-8")
                line = line.rstrip()
                on_msg_receive(line)

        return

    def initialize(self):
        self.proc.stdin.write("initialize\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_pressed(self):
        self.proc.stdin.write("on_pressed\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_released(self):
        self.proc.stdin.write("on_released\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_exit(self):
        self.proc.terminate()
        return



