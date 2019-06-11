'''
SCRIPT DESCRIPTION:
This script tries to make a connection to the client (PC) and waits
to receive a data request from it. When the server is waiting on the
client to request another transfer, pull more data from the sensor.
'''

import sys
import config as cfg
from wifi.sb_server import wifi_server as server
from sensor.nxp import sensor as sensor_if

# +----------+----------+----------+----------+
# |            MAIN (NON-THREADED)            |
# +----------+----------+----------+----------+
def main_single():
    print("Running Blueberry-Pi (NON-THREADED).")
    
    wifi = server(cfg.WIFI_PORT)
    sensor = sensor_if()

    while True:

        # Always listen for a connection to the client.
        try:
            wifi.SetupConnection()
            connOpen = True

            while connOpen:

                # Pull the data from the sensors
                accel_x, accel_y, accel_z = sensor.accel()
                mag_x, mag_y, mag_z = sensor.mag()
                gyro_x, gyro_y, gyro_z = sensor.gyro()

                # Send the data to the client
                connOpen = wifi.DataRxFromClient()

        except:
            print("Unable to connect to client.")
            print("Closing server.")
            break
            
        
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
