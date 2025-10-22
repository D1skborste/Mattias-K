#!/usr/bin/env python3
"""
Network Scanner Project
Students: Björn, Daniel, Mattias.K, Lukas.S, Vien
Date: 251021
"""
# Importing modules
import socket
import sys
import threading
from datetime import datetime


open_ports= []

#optional CLI arguments
if len(sys.argv) == 4:
    start_port = int(sys.argv[3])
    max_port = int(sys.argv[4])
    print(sys.argv)
    

elif len(sys.argv) == 2:
    print(sys.argv)
    # translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])

else:
    target = input('Enter target ip: ')
    start_port = int(input('starting port: '))
    max_ports = int(input('ending port: '))


"""Kan kanske ha koden ovan som en optional CLI argument, 
eller input om man inte gett nåot"""

"""Placeringen i koden behöver justeras"""

def start_scan(target, start_port, max_port):
   #Define the target

    print("Inside func")
    
    try:
        for port in range(start_port, max_port):
            if (port - 1) == max_port - 1:
                print(target, "is finishing its tasks")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = client.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            print(open_ports)
            client.close()
    except socket.gaierror:
        print("Hostname could not be resolved")
        sys.exit()
    except socket.error:
        print("Could not connect to server")
        sys.exit()

if __name__ == "__main__":
    start_scan("45.33.32.156", 20, 25) 
