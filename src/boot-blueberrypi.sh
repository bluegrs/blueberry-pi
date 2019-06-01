#!/bin/bash

# SUMMARY
# This script boots up all the required blueberry-pi
# processes to begin sending hand orientation data to 
# the server.

# EXECUTING
# in command line, type the following:
# ./boot-blueberrypi.sh

# CONFIGURATIONS
WIFI=./wifi

# give permissions for the script to run on command line
chmod +x boot-blueberrypi.sh

# add all background processes here
python3 $WIFI/sb_client.py &

exit
