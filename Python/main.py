from pystray import Icon, MenuItem, Menu
from PIL import Image

from pmdeck import manager
import settings
from Action.folder import Folder
from do_threaded import do_threaded

import os
from threading import Event

if __name__ == "__main__":

    s = settings.Settings()
    s.read_settings()

    manager = manager.DeviceManager()

    def key_callback(deck, key, status):

        if status == "0":
            deck.current_folder.button_pressed(key)
        else:
            deck.current_folder.button_released(key)
        return

    def on_connected_callback(deck):
        deck.set_key_callback(key_callback)
        # TODO if already connected, don't reset
        deck.reset()

        root_folder = Folder(s, deck, "root")
        # root_folder.set_action(12, create_custom_action(deck, "MicOnOffAction"))
        # root_folder.set_action(0, create_custom_action(deck, "MicOnOffPy"))
        # root_folder.set_action(14, CallibrateFootAction(deck))

        # root_folder.set_action(1, AutoHotkeyAction(deck, "Action001"))
        # root_folder.set_action(0, AutoHotkeyAction(deck, "Action000-Blank"))
        # for i in range(1,15,2):
        #     root_folder.set_action(i, TestAction(deck))
        root_folder.open()

        return

    manager.set_on_connected_callback(on_connected_callback)

    manager.listen_connections()

    def test_button():
        print("test button")

    def open_ui_button():
        print("opening ui")

    def quit_button():
        print("quitting")
        os._exit(0)

    image = Image.open("icon.png")

    tray_app = Icon('test', image, menu=Menu(
        MenuItem(
            'Test',
            test_button),
        MenuItem(
            'Open UI',
            open_ui_button,
            default=True),
        MenuItem(
            'Quit',
            quit_button)))

    # do_threaded(tray_app.run)
    tray_app.run()
    # Event().wait()
