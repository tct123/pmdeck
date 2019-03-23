import socket
import base64
import traceback
from random import randint
import threading
from Util.do_threaded import do_threaded

from pmdeck.get_uid import get_uid


class Deck:

    def __init__(self, client_socket: socket.socket):

        self.id = None
        self.key_callback = None
        self.client_socket: socket.socket = client_socket
        self.disconnected = False
        self.key_count_x = 3
        self.key_count_y = 2
        self.read_thread: threading.Thread = None

        return

    def __del__(self):
        return

    def read(self):

        # self.client_socket.settimeout(5)

        def listener():
            while not self.disconnected:
                try:
                    data = self.client_socket.recv(1024)
                    stream = data.decode('utf-8')
                    if len(stream) > 1:
                        print("Received: {}".format(stream))
                    for msg in list(filter(None, stream.split(';'))):
                        spl = msg.split(":")
                        cmd = spl[0]
                        if cmd == "PING":
                            self.send("PONG;")

                        elif cmd == "PONG":
                            pass

                        elif cmd == "CLOSE":
                            self.disconnect()
                            return

                        elif cmd == "BTNEVENT":
                            args = spl[1].split(",")
                            self.on_key_status_change(args[0], args[1])

                        elif cmd == "CONN":
                            args = spl[1].split(",")
                            self.id = args[0]
                            if self.id in self.device_manager.Decks:
                                self.send("CONN:{};".format(get_uid()))
                                self.reset()
                                self.device_manager.on_connected(self)
                            else:
                                self.disconnect()

                        elif cmd == "SYNCREQ":
                            args = spl[1].split(",")
                            self.id = args[0]
                            self.send("SYNCTRY:{},{};".format(get_uid(), randint(100000, 999999)))

                        elif cmd == "SYNCACCEPT":
                            args = spl[1].split(",")
                            uid = args[0]
                            password = args[1]
                            self.device_manager.Decks[uid] = {"connected": True, "pass": password}
                            self.device_manager.save_deck_info()
                            self.send("CONN:{},{};".format(get_uid(), password))

                except Exception as e:
                    print(e)
                    self.disconnect()
                    return

        self.read_thread = do_threaded(listener)

        # def pinger():
        #     while not self.disconnected:
        #         try:
        #             self.send("PING;")
        #             time.sleep(3)
        #         except Exception as e:
        #             print(e)
        #             self.disconnect()
        #             return
        #
        # self.ping_thread = threading.Thread(target=pinger)
        # self.ping_thread.start()

        #self.deviceManager.on_connected(self)
        return

    def send(self, s):
        print("Sent: {}".format(s))
        self.client_socket.send(s.encode("utf-8"))
        return

    def disconnect(self):
        if self.disconnected:
            return

        print("Deck Disconnected")
        # TODO
        traceback.print_exc()
        self.client_socket.close()

        self.disconnected = True
        return

    def reset(self):
        for i in range(0, 15):
            self.set_key_image_path(str(i), "Assets/empty.png")
        return

    def set_key_image_path(self, key, image_path: str):
        if image_path.endswith(".png"):
            encoded = base64.b64encode(open(image_path, "rb").read())
            self.set_key_image_base64(key, encoded)
        else:
            print("please give a png file, this is not acceptable -> {}".format(image_path))
        return

    def set_key_image_base64(self, key, base64_string):
        print(base64_string);
        encoded = ("IMAGE:" + str(key) + ",").encode('utf-8') + base64_string + ";".encode('utf-8')
        try:
            self.client_socket.send(encoded)
        except Exception as e:
            print(e)
            self.disconnect()
        return

    def set_key_callback(self, callback):
        self.key_callback = callback
        return

    def on_key_status_change(self, key, status):
        if self.key_callback:
            self.key_callback(self, key, status)
        return
