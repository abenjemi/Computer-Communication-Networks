# Data-Link-Layer

In this project, I implemented the data link layer routing using Spanning Tree Protocol
(STP) and MAC learning and forwarding in a simulated network environment. I created a forwarding table at each switch, implemented STP and MAC learning to populate those forwarding tables, and implement MAC forwarding to forward DATA packets. 

Since the link status can change dynamically, i.e., during the run time, existing links can be removed,
or new links can be added, or the link cost can change, my implementation must be resilient to
changes in link status. 

The simulated network has switches, clients (end hosts), links, and packets just like a real network. Files like “switch.py”, “client.py”, “link.py” and “packet.py” contain the implementations of a switch,
a client, a link, and a packet respectively. 
I implemented STP, and learning and forwarding in "STPswitch.py". 

There are 3 sample network simulation files, “01.json”, “02.json”, and “03.json” that contain information about the switches, clients, changes, and correct paths that I used to compare my output paths to.

The code can be run and the output can be viewed using the command following command: "./run_all.sh".
