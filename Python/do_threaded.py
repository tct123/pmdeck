import threading


def do_threaded(func):
    threading.Thread(
        target=func
    ).start()
    return
