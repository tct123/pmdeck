import threading


def do_threaded(func):
    t = threading.Thread(
        target=func
    )
    t.setDaemon(True)
    t.start()
    return t
