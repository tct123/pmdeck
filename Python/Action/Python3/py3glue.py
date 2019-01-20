
import Python3Action
import sys
import os

def on_event_received(event):

    try:
        if (event == "initialize"):
            Python3Action.initialize()
        if (event == "on_pressed"):
            Python3Action.on_pressed()
        if (event == "on_hold_down"):
            Python3Action.on_hold_down()
        if (event == "on_released"):
            Python3Action.on_released()
        if (event == "on_visible"):
            Python3Action.on_visible()
        if (event == "on_invisible"):
            Python3Action.on_invisible()
        if (event == "on_update_sec"):
            Python3Action.on_update_sec()
        if (event == "on_update"):
            Python3Action.on_update()
        if (event == "on_exit"):
            Python3Action.on_exit()
    except:
        pass

    return


def set_image(name):
    print(name)
    return


if __name__ == "__main__":

    os.chdir(os.path.dirname(sys.argv[0]))

    Python3Action.set_image = set_image

    while True:
        line = sys.stdin.readline()
        line = line.rstrip("\n")
        on_event_received(line)
