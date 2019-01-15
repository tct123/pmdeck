

pipe_name = r'\\.\pipe\button1'

from subprocess import *
import os

FIFO_PATH = '/tmp/my_fifo'

if os.path.exists(FIFO_PATH):
    os.unlink(FIFO_PATH)

if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)
    my_fifo = open(FIFO_PATH, 'w+')
    print ("my_fifo:" + my_fifo)

pipe = Popen('/bin/date', shell=False, stdin=PIPE, stdout=my_fifo, stderr=PIPE)

print (open(FIFO_PATH, 'r').readline())

os.unlink(FIFO_PATH)


