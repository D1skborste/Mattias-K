#!/usr/bin/env python3
"""
Network Scanner Project
Students: Björn, Daniel, Mattias.K, Lukas.S, Vien
Date: 251021
A simple, user-friendly, multi-port scanner without threading.
"""
# Importing modules
import socket
import sys
import threading
from datetime import datetime


open_ports= []



def start_scan(name, start_port, max_port):
   #Define the target    
    try:
        for port in range(start_port, max_port):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.2)
            result = client.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            
            client.close()
    except socket.gaierror:
        print("Hostname could not be resolved")
        sys.exit()
    except socket.error:
        print("Could not connect to server")
        sys.exit()




if __name__ == "__main__":
    print("=" * 50)
    print("Port scanner by '404-gänget'")
    print("=" * 50)
    # len(sys.argv) checks are optional CLI arguments.
    # I assume an argument format of <domain name or IP>, <start_port>, <end_port>.
    if len(sys.argv) == 4:
        target = socket.gethostbyname(sys.argv[1])
        start_port = int(sys.argv[2])
        max_port = int(sys.argv[3])

    # With only 2 arguments, it will ask the user to input <start_port> and <end_port>.
    elif len(sys.argv) == 2:
    # translate hostname to IPv4. It will also accept just the IP.
        target = socket.gethostbyname(sys.argv[1])
        start_port = int(input('starting port: '))
        max_port = int(input('ending port: '))

    # As last resort, it will ask the user to input IP or domain.
    else: # It will convert <domain name> to IPv4, before asking for <start_port> and <end_port>.
        domain_name = input('Enter target ip or domain: ')
        target = socket.gethostbyname(domain_name)
        start_port = int(input('starting port: '))
        max_port = int(input('ending port: '))


    
    print("-" * 50)
    print("Scanning for open ports in range {}-{} . . .".format(start_port, max_port))
    print("Time started: " + str(datetime.now()))
    print("-" * 50)

    start_scan(target, start_port, max_port)

    print(f"Done scanning on target ip: {target}")
    print("Time Ended: " + str(datetime.now()))
    if len(open_ports) == 0:
        print("no open ports found in range {}-{}".format(start_port, max_port))
    else:
        print("open ports found:")
        print("-" * 50)
        for port in open_ports:
            print(port)
        print("-" * 50)
