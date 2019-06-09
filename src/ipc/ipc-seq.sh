#!/bin/bash

# SUMMARY
# This script tests if the ipc module works for sequential
# writes then reads.

# EXECUTING
# in command line, type the following:
# ./ipc-seq.sh

# give permissions for the script to run on command line
chmod +x ipc-seq.sh

# +----------+----------+----------+----------+
# |	    MULTITHREAD SEQUENTIAL METHOD         |
# +----------+----------+----------+----------+
echo "RUNNING SEQUENTIAL MULTITHREAD VERSION"

# add all background processes here
python3 writer.py -multithread -seq &
python3 reader.py -multithread -seq &

# +----------+----------+----------+----------+
# |	    	 SOCKET SEQUENTIAL METHOD         |
# +----------+----------+----------+----------+
echo "RUNNING SEQUENTIAL SOCKET VERSION"

# add all background processes here
python3 writer.py -socket -seq &
python3 reader.py -socket -seq &

exit
