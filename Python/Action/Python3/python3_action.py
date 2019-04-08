from Action.action import Action
import os
import subprocess
from Util.do_threaded import do_threaded


class Python3Action(Action):

    def __init__(self, deck, action_id):

        f = open("Action/Python3/py3glue.py", "r")
        gluetext = f.read()
        f.close()

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

    def on_hold_down(self):
        self.proc.stdin.write("on_hold_down\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_released(self):
        self.proc.stdin.write("on_released\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_visible(self):
        self.proc.stdin.write("on_visible\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_invisible(self):
        self.proc.stdin.write("on_invisible\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_update_sec(self):
        self.proc.stdin.write("on_update_sec\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_update(self):
        self.proc.stdin.write("on_update\n".encode("utf-8"))
        self.proc.stdin.flush()
        return

    def on_exit(self):
        self.proc.stdin.write("on_exit\n".encode("utf-8"))
        self.proc.stdin.flush()
        self.proc.terminate()
        return

