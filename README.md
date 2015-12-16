# File Server and Clustered Memory Simulator
This a file server that operates over TCP sockets (port 8765) and simulates clustered data while doing so.

# TELNET / NC Notes
To follow the specifications, the store command does not expect a newline after the transfer of file data; it expects it to be as in the specificationsand go straight from the end of data with a length as described to the next command.

By Mason Cooper (coopem4) & John Drogo (drogoj)
