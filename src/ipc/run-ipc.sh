#!/bin/bash

# SUMMARY
# This script tests if the ipc module works for sequential
# writes then reads.

# EXECUTING
# in command line, type the following:
# ./run-ipc.sh

# give permissions for the script to run on command line
chmod +x run-ipc.sh

# add all background processes here
python3 writer.py -seq &
python3 reader.py -seq &

exit
