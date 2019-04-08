
enabled = True

def initialize():
    set_image("mic-on.png")
    return


def on_pressed():
    global enabled

    if enabled:
        set_image("mic-off.png")
    else:
        set_image("mic-on.png")

    enabled = not enabled
    return

