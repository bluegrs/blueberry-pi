'''
SCRIPT DESCRIPTION:
This script is the main processes for the wifi module on the controller (raspi)
side. This script pulls data from the common resources and immediately
sends it over to the PC.

1. The controller creates a socket and listens for the PC to connect to it
    as the player decides to use the blueberry-pi as the game controller.
2. Once that happens, begin pulling data from the shared resource.
3. Send the data to the PC for processing.
'''

import sys
import time

# Blueberry-Pi specific modules
import config as cfg
from ipc.ipc import IPCServer as Resource
from wifi.sb_server import wifi_server as WifiServer

def main():

    # instantiate a connection with the shared resource on bootup.
    shared = Resource(6000)
    rx = None

    # instantiate the wifi server which automatically
    # sets up a server socket on the specified port.
    wifi = WifiServer(5560)

    # Continue to make connections or send/receive data
    # until a client requests that the server socket is
    # closed.
    while True:
        try:
            server.SetupConnection()
            closeConnection = False
            
            while not closeConnection:

                # Receive a message from the client (PC) in case of EXIT
                closeConnection = server.DataRxFromClient()

                # Pull the next piece of data from the shared resource
                # if there is anything available.
                try:
                    rx = shared.Read()
                    termPrint("Received '" + str(rx) + "' from resource.")
                except:
                    termPrint("Timeout error. Reconnect to client.")
                    break

        # If SetupConnection causes an error for some reason, the
        # program ends.
        except:
            termPrint("SetupConnection() caused an error.")
            break

'''
SUMMARY: This function will only print to the terminal if the blueberry-pi
is configured in debug mode. Otherwise, it does not waste CPU time printing
to the terminal.
'''
def termPrint(message):
    if cfg.DEBUG_MODE == True:
        print("*** WIFI SERVER *** : " + message)

if __name__ == '__main__':
    main()
