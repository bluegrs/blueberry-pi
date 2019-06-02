# Interprocess Communication
FIFO resource to use between wifi transfer and data aquisition processes.

## Modules
- **ipc.py:** This module implements a few IPC classes to see which method will function best.

## Scripts
- **reader.py:** This script tests if a process could safely read from the common resource.
- **writer.py:** This script tests if a process could safely write to the common resource.
- **ipc-con.sh** Unix shell script to run the reader/writer processes concurrently for all IPC implementations.
- **ipc-seq.sh** Unix shell script to run the reader/writer processes sequentially for all IPC implementations.
