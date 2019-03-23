
import time

from Util.do_threaded import do_threaded


class Action:

    def __init__(self, deck):
        self.image_path = "Assets/empty.png"
        self.is_visible = False
        self.current_space = 0
        self.is_pressed = False
        self.deck = deck
        self.initialize()
        do_threaded(self._update_loop)
        return

    def _set_visible(self, space):
        self.is_visible = True
        self.current_space = space
        self.on_visible()
        self._draw()
        return

    def _set_invisible(self, space):
        self.is_visible = False
        self.on_invisible()
        return

    def set_image_path(self, image_path):
        self.image_path = image_path
        self._draw()
        return

    def _draw(self):
        if self.is_visible:
            self.deck.set_key_image_path(self.current_space, self.image_path)
        return

    def _pressed(self):
        self.is_pressed = True
        self.on_pressed()
        return

    def _released(self):
        self.is_pressed = False
        self.on_released()
        return

    def _update_loop(self):
        last_1_sec_update = time.time()

        while True:
            last_update = time.time()

            self.on_update()
            if last_update - last_1_sec_update > 1:
                self.on_update_sec()
                last_1_sec_update = last_update
            if self.is_pressed:
                self.on_hold_down()

            time_elapsed = time.time() - last_update
            if time_elapsed < 0.1:
                time.sleep(0.1-time_elapsed)
        return

    def initialize(self):
        return

    def on_visible(self):
        return

    def on_invisible(self):
        return

    def on_pressed(self):
        return

    def on_hold_down(self):
        return

    def on_released(self):
        return

    def on_update_sec(self):
        return

    def on_update(self):
        return

    def on_exit(self):
        return



    

    