
import pipes
import time
import win32file
import win32pipe
pipe_name = r'\\.\pipe\button1'

print("pipe server")
count = 0
pipe = win32pipe.CreateNamedPipe(
    pipe_name,
    win32pipe.PIPE_ACCESS_DUPLEX,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    1, 65536, 65536,
    0,
    None)
try:
    print("waiting for client")
    win32pipe.ConnectNamedPipe(pipe, None)
    print("got client")

    # convert to bytes
    some_data = str.encode(f"asdasdasdad")
    win32file.WriteFile(pipe, some_data)
    time.sleep(1)

    print("finished now")
finally:
    win32file.CloseHandle(pipe)


