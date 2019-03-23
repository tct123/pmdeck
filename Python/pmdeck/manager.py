import json
import socket
from Util.do_threaded import do_threaded

import zeroconf

from pmdeck.get_uid import get_uid
from pmdeck.get_ip import get_ip
from pmdeck.deck import Deck


class DeviceManager:

    def __init__(self):
        self.connected_callback = None
        self.disconnected_callback = None
        self.zeroconf = zeroconf.Zeroconf()
        self.Decks = {}
        self.load_deck_info()
        self.server_socket = None
        self.connector_thread = None
        return

    def connector_listener(self):
        bind_ip = '0.0.0.0'
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((bind_ip, 0))
        self.server_socket.listen(5)  # max backlog of connections
        local_ip = get_ip()
        port = self.server_socket.getsockname()[1]

        print('Listening on {}:{}'.format(local_ip, port))

        print("Registering Service")
        service_name = "{}:{}._pmdeckdiscovery._tcp.local.".format(local_ip, str(port))
        service_type = "_pmdeckdiscovery._tcp.local."
        desc = {"uid": get_uid()}
        info = zeroconf.ServiceInfo(service_type,
                                    service_name,
                                    socket.inet_aton(local_ip), port, 0, 0,
                                    desc, local_ip + ".")

        self.zeroconf.register_service(info)

        while True:
            try:
                client_socket, address = self.server_socket.accept()
                print('Accepted connection from {}:{}'.format(address[0], address[1]))
                deck = Deck(client_socket, self)
                deck.read()
            except Exception as e:
                print(e)
                return
        return

    def listen_connections(self):
        self.connector_thread = do_threaded(self.connector_listener)
        return

    def stop_listening_connections(self):
        self.server_socket.close()
        return

    def unregister_service(self):
        self.zeroconf.unregister_all_services()
        return

    def sync_new_device(self):
        return

    def stop_syncing(self):
        return

    def set_on_connected_callback(self, callback):
        self.connected_callback = callback
        return

    def on_connected(self, deck):
        # deck.reset()
        if self.connected_callback:
            self.connected_callback(deck)
        return

    def set_on_disconnected_callback(self, callback):
        self.disconnected_callback = callback
        return

    def on_disconnected(self, deck):
        if self.disconnected_callback:
            self.disconnected_callback(deck)
        return

    def save_deck_info(self):
        try:
            with open('decks.json', 'w') as outfile:
                json.dump(self.Decks, outfile)
        except:
            pass
        return

    def load_deck_info(self):
        try:
            with open('decks.json') as json_file:
                self.Decks = json.load(json_file)
        except:
            pass
        return

