'''
SCRIPT DESCRIPTION:
This script tries to make a connection to the server (Rasp-Pi) and
asks to receive sensor data from the controller.
'''

import sys
import config as cfg
from wifi.sb_client import client

# +----------+----------+----------+----------+
# |            MAIN (NON-THREADED)            |
# +----------+----------+----------+----------+
def main_single():
    print("Running device drivers (NON-THREADED).")
    connOpen = False
    
    # Try to connect to the device. If no device was found,
    # ask the user to try again or exit.
    while True:
        try:
            wifi = client(cfg.WIFI_PORT, cfg.TIMEOUT)
            
            # Try to receive data from the client. If there is an
            # error, no connection was made and the exception will
            # be thrown.
            trash = wifi.request(cfg.ACCEL)
            connOpen = True
            break
            
        except:
            wifi.close()
            restart = input("No connection made. Try again? [y/n]: ")
        
            if restart == "y":
                continue
            else:
                break

    # Only begin sending requests if a connection was made
    if connOpen:
        while True:
        
            # Request sensor data
            ax,ay,az = wifi.request(cfg.ACCEL)
            # print(str(ax) + " " + str(ay) + " " + str(az))
            
            gx,gy,gz = wifi.request(cfg.GYRO)
            # print(str(gx) + " " + str(gy) + " " + str(gz))
            
            mx,my,mz = wifi.request(cfg.MAG)
            # print(str(mx) + " " + str(my) + " " + str(mz))

        print("Connection to server closed.")
    
    print("EOP.")
        
        
# +----------+----------+----------+----------+
# |               MAIN (THREADED)             |
# +----------+----------+----------+----------+
def main_threaded():
    print("Running device drivers (THREADED).")

if __name__ == '__main__':
    
    # default to running the non-threaded version
    # unless the user requests to use the threaded
    # version in the configs file.
    if cfg.VERSION == 'threaded':
        main_threaded()
    else:
        main_single()
