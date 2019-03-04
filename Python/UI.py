from do_threaded import do_threaded
from windowmgr import WindowMgr


class UI:

    def __init__(self):
        self.ui_process = None
        self.out_listener = None
        self.err_listener = None

    def create_ui(self):
        global ui_process
        global out_listener
        global err_listener

        ui_process = subprocess.Popen("npm start --prefix ..\\Electron", shell=True, close_fds=True,
                                      stdin=PIPE, stdout=PIPE, stderr=PIPE)

        def listen_out():
            while True:
                line = ui_process.stdout.readline()
                if len(line) > 0:
                    print(line)

        def listen_err():
            while True:
                line = ui_process.stderr.readline()
                if len(line) > 0:
                    print(line)

        out_listener = do_threaded(listen_out)
        err_listener = do_threaded(listen_err)

    def focus_or_create_ui(self):
        global ui_process

        try:
            w = WindowMgr()
            w.find_window_wildcard(".*PMDECK.*")
            w.set_foreground()
        except:
            self.create_ui()

        return
