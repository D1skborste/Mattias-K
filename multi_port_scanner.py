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
import time
from tqdm import tqdm
from colorama import init, Fore
from datetime import datetime

# Init colors
init()
GREEN = Fore.GREEN
MAGENTA =Fore.MAGENTA
BLUE = Fore.BLUE
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

# Global list to save ports
open_ports = []
        
# Set range ports, including the max port
def start_multiscan(name, start_port, max_port, timeout=1.0):

    # Set range ports, including the max port
    for port in range(start_port, max_port + 1):
        #AF_INET = IPv4, SOCK_STREAM = constant, create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            # If a port is open, add the open port to the open_ports list
            if result == 0:
                # Add open port to the open_ports list
                open_ports.append(port)
                try:
                    # For HTTP-ports
                    if port in (80, 8080):
                        # Sends an HTTP HEAD request to the connected server, asking for only HTTP headers without a body
                        s.sendall(b"HEAD / HTTP/1.0\r\nHost: %b\r\n\r\n" % target.encode())
                    # Read max 1024 bytes from the opened socket
                    data = s.recv(1024)
                    # Convert the data and do split and strip empy spaces, and get the first part
                    banner = data.decode(errors="ignore").splitlines()[0].strip()
                    # If the banner exists
                    if banner:
                        print(f"Banner for {target}:{port} -> {banner}")
                    else:
                        print(f"No banner received for {target}:{port}")
                # Socket timed out error
                except socket.timeout:
                    print(f"No banner (timeout) for {target}:{port}")
                # Catch other errors
                except Exception as e:
                    print(f"Error reading banner for {target}:{port}: {e}")
        # DNS lookup failed error
        except socket.gaierror as e:
            print(f"Hostname could not be resolved. {e}")
            return
        # Socket error
        except socket.error as e:
            print(f"Could not connect to server. {e}")
            return
        # Close socket
        finally:
            s.close()

    # Print out the open_ports list
    for p in open_ports:
        print(f"{GREEN} Port {p} is open.")

    # Ports to file
    save_ports_to_file(open_ports)

# Save the ports to file
def save_ports_to_file(port_list):
    print(f"{GREEN}Save ports {port_list} to file.")
    file_name = "port_results.txt"

    # Try to save to file
    try:
        with open(file_name, "w") as f:
            # Separate each line with \n at the end
            for port in port_list:
                f.write(f"Port {port} is open.\n")
                # Print out the result of the saved file 
            print(f"{MAGENTA}The results have been saved to the file: {file_name}")

    # File not found error
    except FileNotFoundError:
        print("File not found.")
    # Writing to file errors
    except IOError:
        print("An I/O error occurred.")
    # Other errors
    except:
        print("Something went wrong...")
    # Close file
    f.close()

# Run the program
if __name__ == "__main__":
    
    # Optional CLI arguments, i.e multi_port_scanner.py scanme.nmap.org 1 30
    # len(sys.argv) checks are optional CLI arguments.
    # I assume an argument format of <domain name or IP>, <start_port>, <end_port>.
    if len(sys.argv) == 4:
        target = socket.gethostbyname(sys.argv[1])
        start_port = int(sys.argv[2])
        max_port = int(sys.argv[3])
                
        
    # I.e multi_port_scanner.py scanme.nmap.org
    # With only 2 arguments, it will ask the user to input <start_port> and <end_port>.
    elif len(sys.argv) == 2:
    # translate hostname to IPv4. It will also accept just the IP.
        target = socket.gethostbyname(sys.argv[1])
        start_port = int(input('starting port: '))
        max_port = int(input('ending port: '))

    # Else inputs from console
    # As last resort, it will ask the user to input IP or domain.
    else: # It will convert <domain name> to IPv4, before asking for <start_port> and <end_port>.
        domain_name = str(input(Fore.BLUE + 'Enter target IP or domain: '))
        target = socket.gethostbyname(domain_name)
        start_port = int(input(Fore.BLUE + 'Starting port: '))
        max_port = int(input(Fore.BLUE + 'Ending port: '))

    # Simulates the loading bar 
    for x in tqdm(range(100)):
        time.sleep(0.005)

    # Scan the give url with start and end ports
    start_multiscan(target, start_port, max_port)
