'''
SCRIPT DESCRIPTION:
This script is the main process on the controller (raspi) side. This version
of the main function only runs one instance of python and has options to
run non-threaded and threaded versions of the same application to test
performance for various conditions.

1. The controller creates a socket and listens for the PC to connect to it
    as the player decides to use the blueberry-pi as the game controller.
2. Once that happens, begin pulling data from the shared resource.
3. Send the data to the PC over wifi for processing.
'''

import sys
import config as cfg

def main_single():
    print("Running Blueberry-Pi (NON-THREADED).")

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
