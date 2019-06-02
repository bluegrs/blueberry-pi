#!/bin/bash

# SUMMARY
# This script tests if the ipc module works for concurrent
# write and reads.

# EXECUTING
# in command line, type the following:
# ./ipc-con.sh

# give permissions for the script to run on command line
chmod +x ipc-con.sh

# +----------+----------+----------+----------+
# |	    MULTITHREAD CONCURRENT METHOD         |
# +----------+----------+----------+----------+
echo "RUNNING CONCURRENT MULTITHREAD VERSION"

# add all background processes here
python3 writer.py -multithread -con &
python3 reader.py -multithread -con &

exit