
import pipes
import time
import win32pipe
import win32file
import pywintypes

from do_threaded import do_threaded

pipe_name = r'\\.\pipe\pmdeck\button1'


def send_data(s):
    try:
        pipe = win32pipe.CreateNamedPipe(
            pipe_name+"s",
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None)
        win32pipe.ConnectNamedPipe(pipe, None)
        some_data = str.encode(s)
        win32file.WriteFile(pipe, some_data)
    finally:
        win32file.CloseHandle(pipe)

    return


def on_data_reveiced(s):
    print("data received: {}".format(s))
    return


def data_listener():

    while True:
        try:
            handle = win32file.CreateFile(
                pipe_name+"c",
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if res == 0:
                print(f"SetNamedPipeHandleState return code: {res}")
            while True:
                resp = win32file.ReadFile(handle, 64 * 1024)
                on_data_reveiced(resp)
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif e.args[0] == 109:
                print("broken pipe, bye bye")
                break


do_threaded(data_listener)


