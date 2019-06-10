'''
SCRIPT DESCRIPTION:
This script tries to make a connection to the server (Rasp-Pi) and
asks to receive sensor data from the controller.
'''

import sys
import config as cfg
from wifi.sb_client import wifi_client as client

# +----------+----------+----------+----------+
# |            MAIN (NON-THREADED)            |
# +----------+----------+----------+----------+
def main_single():
    print("Running Blueberry-Pi (NON-THREADED).")
    
    wifi = client(cfg.WIFI_PORT)
    connOpen = True

    # Always listen for a connection to the client.
    while connOpen:
        message = 'READ'
        connOpen = wifi.DataTxToHost(message)

    print("Connection to server closed.")
        
        
# +----------+----------+----------+----------+
# |               MAIN (THREADED)             |
# +----------+----------+----------+----------+
def main_threaded():
    print("Running Blueberry-Pi (THREADED).")

if __name__ == '__main__':
    
    # default to running the non-threaded version
    # unless the user requests to use the threaded
    # version in the configs file.
    if cfg.VERSION == 'threaded':
        main_threaded()
    else:
        main_single()
