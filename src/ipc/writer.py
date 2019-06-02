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
from ipc import IPCClient as shareable

# +----------+----------+----------+----------+
# |         MULTITHREAD SEQUENTIAL            |
# +----------+----------+----------+----------+
def multithread_sequential():
    termPrint("Running sequential test.")
    writer = shareable(6000)

    # Send the test data to the reader
    termPrint("Writing 'hello world' to resource")
    writer.Write('hello world')
              
    termPrint("EOP")

# +----------+----------+----------+----------+
# |         MULTITHREAD CONCURRENT            |
# +----------+----------+----------+----------+
def multithread_concurrent():
    termPrint("Running concurrent test.")
    writer = shareable(6000)

    # Send series of data 1-2-3-4-5-6-... to see if
    # the user will receive information that makes
    # sense if running concurrently.
    for i in range(0,100):
        data = str(i)

        # See what happens if we "hang" 
        time.sleep(.5)
        
        termPrint("Writing '" + data + "' to resource")
        writer.Write(data)

    termPrint("EOP")

def termPrint(message):
    print("*** WRITER *** : " + message)

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
