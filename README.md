# Network Scanner

## Group Members
- Mattias.K

## Description
Individual continuation of 'one of the most advanced and secure portscanners in the whole class'. 
The main goal was to make it able to accept a list of ips. I Also wanted to improve useability, to make it close to idiot-proof. A coma patient with amnesia should be able to use it, and easily grasp the extra functions.
It's also a timesaver to launch the program, with shortcuts to run it with default, predetermined settings and only ask for input when necessary.
================================================================================================================
## O.G. Group Members and Description
- Björn
- Daniel
- Mattias.K
- Lukas.S
- Vien

## Description
In October 2025, we decided to make one of the most advanced and secure portscanners in the whole class. We sat many hours programming under very dramatic circumstances, personal struggles and bad weather. Finally, when we thought we couldn’t be done before the first week, we managed to finish our task.

We can now proudly present to the world our port scanner.
================================================================================================================



## Installation
```bash
# Install dependencies (if needed)
pip install -r requirements.txt
```

## Usage
```bash
# How to run your scanner
python multi_port_scanner.py
1. Run the script
2. Enter an IP-adress or URL
3. Enter the starting port in the range
4. Enter the last port in the range
5. Take a snack and a drink and enjoy the loading bar
```

## Features
- [x] Single port check
- [x] Multi-port scanning
- [x] Service identification
- [x] Saves to file
- [X] Loading bar
- [x] OS detection of the target
- [x] Beutiful colorama lines
- [x] User friendly CLI arguments and installation package through requirements.txt
- [x] User friendly URL inputs
- [x] Accepts a list, or several list of ips
- [x] A help menu appears if program launches without arguments
- [x] Automatically parses, and sorts the arguments, to identify target, ports, and timeout
- [x] Timesaving shortcuts to launch with default settings 

## Testing
45.33.32.156 - scanme.nmap.org
44.228.249.3 - testphp.vulnweb.com
127.0.0.1 - opened port on local machine

## Known Limitations
No threading function(yet)
Could have been faster.

## What We Learned
Basic port scanning abilities
To work in a team
Troubleshooting
Testing...and testing again
Better Python and Github abilities

