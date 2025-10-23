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


#optional CLI arguments

if __name__ == "__main__":
    if len(sys.argv) == 4:
        target = socket.gethostbyname(sys.argv[1])
        start_port = int(sys.argv[2])
        max_port = int(sys.argv[3])


    elif len(sys.argv) == 2:
    # translate hostname to IPv4
        target = socket.gethostbyname(sys.argv[1])
        start_port = int(input('starting port: '))
        max_port = int(input('ending port: '))

        
    else:
        domain_name = input('Enter target ip or domain: ')
        target = socket.gethostbyname(domain_name)
        start_port = int(input('starting port: '))
        max_port = int(input('ending port: '))

    

    threads_count = int(input('threads count: '))

    threads = []