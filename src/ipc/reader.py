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

def sequential():
    termPrint("Running sequential test.")
    reader = shareable(6000)

    # wait for .1 seconds just to make sure the
    # data is not being accessed by the writer anymore.
    time.sleep(.1)
    rx = reader.Read()

    termPrint("Received " + str(rx) + " from socket")
    print("EOP")

def concurrent():
    termPrint("Running concurrent test.")
    termPrint("EOP")

def termPrint(message):
    print("*** READER *** : " + message)

if __name__ == "__main__":
    request = sys.argv[1]

    if request == '-seq':
        sequential()

    elif request == '-con':
        concurrent()

    else:
        termPrint("Request must be -seq or -con")
