
import Python3Action
import sys
import os

def on_event_received(event):
    if (event == "initialize"):
        Python3Action.initialize()

    if (event == "on_pressed"):
        Python3Action.on_pressed()

    if (event == "on_released"):
        Python3Action.on_released()

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
