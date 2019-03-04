import subprocess
from subprocess import PIPE

from do_threaded import do_threaded
from windowmgr import WindowMgr


class UI:

    def __init__(self):
        self.ui_process = None
        self.out_listener = None
        self.err_listener = None
        self.window_manager = WindowMgr()


        self.create_ui()

    def create_ui(self):
        self.ui_process = subprocess.Popen("npm start --prefix ..\\Electron", shell=True, close_fds=True,
                                           stdin=PIPE, stdout=PIPE, stderr=PIPE)

        def listen_out():
            while True:
                line = self.ui_process.stdout.readline()
                if len(line) > 0:
                    print(line)

        def listen_err():
            while True:
                line = self.ui_process.stderr.readline()
                if len(line) > 0:
                    print(line)

        self.out_listener = do_threaded(listen_out)
        self.err_listener = do_threaded(listen_err)

    def focus_or_create_ui(self):
        self.window_manager.find_window_pid(self.ui_process.pid)
        self.window_manager.set_foreground()
        return
