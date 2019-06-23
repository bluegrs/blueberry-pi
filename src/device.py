'''
SCRIPT DESCRIPTION:
This script tries to make a connection to the client (PC) and waits
to receive a data request from it. When the server is waiting on the
client to request another transfer, pull more data from the sensor.
'''

import sys
import config as cfg
from wifi.sb_server import server
from sensor.nxp import sensor as sensor_if

# +----------+----------+----------+----------+
# |            MAIN (NON-THREADED)            |
# +----------+----------+----------+----------+
def main_single():
    print("Running Blueberry-Pi (NON-THREADED).")

    # object construction
    wifi    = server(cfg.WIFI_PORT)
    sensor  = sensor_if()

    serverOpen = True

    # Continue to make connections or send/receive data
    # until a client requests that the server socket is
    # closed.
    while serverOpen:

        # Always listen for a connection to the client.
        try:
            wifi.SetupConnection()

            while True:

                # Wait for a request from the client.
                mess = str(wifi.receive())
                print(mess)

                # If kill or exit, skip the rest of the loop
                if mess == cfg.EXIT:
                    notification = "EXIT CONNECTION"
                    wifi.closeConnection()
                    break

                elif mess == cfg.KILL:
                    notification = "KILL SERVER"
                    wifi.closeConnection()
                    wifi.closeServer()
                    serverOpen = False
                    break

                # Decode request from the client.
                if mess == cfg.ACCEL:
                    notification = "Accel"
                    data = sensor.accelj()

                elif mess == cfg.MAG:
                    notification = "Mag"
                    data = sensor.magj()

                elif mess == cfg.GYRO:
                    notification = "Gyro"
                    data = sensor.gyroj()
                    
                else:
                    print("Unknown command: " + mess)
                    continue
                
                # Print out the client request.
                print(notification)

                # Send the data as a json.dump string
                print("Responding with :" + data)
                wifi.respond(data)

        except Exception as e:
            print(e)
            print("Closing server.")
            wifi.closeServer()
            serverOpen = False


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
