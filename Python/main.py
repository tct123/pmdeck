from pmdeck import pmdeck
from threading import Event

import settings
from Action.folder import Folder
from Action.custom_action import create_custom_action
import atexit
import threading
import time
import sys
import os

import pystray
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import time



# Decorators


# def callback(icon):
#     image = Image.new('RGBA', (128,128), (255,255,255,255)) # create new image
#     percent = 100
#     while True:
#         img = image.copy()
#         d = ImageDraw.Draw(img)
#         d.rectangle([0, 128, 128, 128-(percent * 128) / 100], fill='blue')
#         icon.icon = img
#         time.sleep(1)
#         percent -= 5
#         if percent < 0:
#             percent = 100


if __name__ == "__main__":

    s = settings.Settings()
    s.read_settings()

    manager = pmdeck.DeviceManager()


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

    Event().wait()

    # state = False
    #
    # def on_clicked(icon, item):
    #     global state
    #     print("Blah")
    #     state = not state
    #
    #
    # Update the state in `on_clicked` and return the new state in
    # a `checked` callable
    # Icon('test', Image.new('RGBA', (128,128), (255,255,255,255)), menu=Menu(
    #     MenuItem(
    #         'Sync New',
    #         on_clicked),
    #     MenuItem(
    #         'Restart',
    #         on_clicked,
    #         default=True),
    #     MenuItem(
    #         'Quit',
    #         on_clicked,
    #         checked=lambda item: state) )
    #     ).run()


