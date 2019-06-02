'''
This file contains two tests outlined below for the shareable object.

SEQUENTIAL: Test if the reader can see the data AFTER the writer writes the
data to the socket.

CONCURRENT: Test if the reader can see the correct data while the reader
and writer processes are constantly running. The module will not function
for the blueberry-pi applications if it does not pass the concurrent test.

NOTE: This module only tests the sequential operation of the reader
and writer, which does NOT reflect how these classes will operate
when separate python instances are trying to read and write to these
classes concurrently (during OS operation).
'''
import sys
import time
from ipc import IPCServer as shareable

# +----------+----------+----------+----------+
# |         MULTITHREAD SEQUENTIAL            |
# +----------+----------+----------+----------+
def multithread_sequential():
    termPrint("Running sequential test.")
    reader = shareable(6000)

    # wait for .1 seconds just to make sure the
    # data is not being accessed by the writer anymore.
    time.sleep(.5)
    rx = reader.Read()

    termPrint("Received '" + str(rx) + "' from resource")
    termPrint("EOP")

# +----------+----------+----------+----------+
# |         MULTITHREAD CONCURRENT            |
# +----------+----------+----------+----------+
def multithread_concurrent():
    termPrint("Running concurrent test.")

    reader = shareable(6000)
    rx = None

    # wait for .1 seconds just to make sure the
    # data is not being accessed by the writer anymore.
    while True:

        # Read infinitely until data runs out
        try:
            rx = reader.Read()
            termPrint("Received '" + str(rx) + "' from resource")

        # EOF reached
        except:
            break

    termPrint("EOP")

def termPrint(message):
    print("*** READER *** : " + message)

# +----------+----------+----------+----------+
# |                    MAIN                   |
# +----------+----------+----------+----------+
if __name__ == "__main__":
    method = sys.argv[1]
    proc = sys.argv[2]

    # determine if the requested method is
    # multithreaded, socket, etc..
    if method == '-multithread':

        # determine if the user is requesting
        # to test the sequential or concurrent
        # operation.
        if proc == '-seq':
            multithread_sequential()

        else:
            multithread_concurrent()

    else:
        termPrint(str(method) + " " + str(proc) + " does not exist yet")
