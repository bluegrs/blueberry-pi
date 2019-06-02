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
from ipc import IPCSpeaker as shareable

def sequential():
    termPrint("Running sequential test."

    # Send the test data to the reader
    writer = shareable(6000)
    writer.WriteByte('H')
              
    print("EOP")

def concurrent():
    termPrint("Running concurrent test.")
    termPrint("EOP")

def termPrint(message):
    print("*** WRITER *** : " + message)

if __name__ == "__main__":
    print(sys.version)
    request = sys.argv[1]

    if request == '-seq':
        sequential()

    elif request == '-con':
        concurrent()

    else
        termPrint("Request must be -seq or -con")
