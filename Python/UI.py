import subprocess
from subprocess import PIPE

from Util.do_threaded import do_threaded
from Util.windowmgr import WindowMgr

import socket

class UI:

    def __init__(self):
        self.ui_process = None
        self.out_listener = None
        self.window_manager = WindowMgr()

        self.create_ui()

    def create_ui(self):
        self.ui_process = subprocess.Popen("npm start --prefix ..\\Electron", shell=True, close_fds=True,
                                           stdout=PIPE)

        def listen_out():
            while True:
                line = self.ui_process.stdout.readline()
                line = line.decode()
                line: str = line.rstrip()
                if len(line) > 0:
                    print(line)
                    for msg in list(filter(None, line.split(';'))):
                        spl = msg.split(":")
                        cmd = spl[0]

                        if cmd == "PORT":
                            args = spl[1].split(",")
                            print("Electron Started com server " + args[0])
                            UICommunicator(int(args[0]))
                            return


        self.out_listener = do_threaded(listen_out)

    def focus_or_create_ui(self):
        try:
            self.window_manager.find_window_pid(self.ui_process.pid)
            self.window_manager.set_foreground()
        except:
            pass
        return


class UICommunicator:

    def __init__(self, port:int):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", port))

        do_threaded(self.socket_listener)


        pass

    def socket_listener(self):
        while True:
            data = self.socket.recv(1024)
            stream = data.decode('utf-8')
            if len(stream) > 0:
                print("Received from UI:{}".format(stream))
                for msg in list(filter(None, stream.split(';'))):
                    spl = msg.split(":")
                    cmd = spl[0]

                    if cmd == "PING":
                        self.send_message("PONG;")



    def send_message(self,msg):
        self.socket.send(msg.encode("utf-8"))
