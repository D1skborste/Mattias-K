import socket
import sys
from datetime import datetime

"""Recieve IP and port from another script"""

def banner(target, port):
    try:
        # Initialize a socket and connect to the given IP and port
        client = socket.socket()
        client.settimeout(5) # Set a 5-second timeout
        client.connect(ip, int(port))
    
        # Receive the banner and decode it to a string
        banner = client.recv(1024).decode().strip()
        print(f"Banner for {ip}:{port} -> {banner}")
        
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        # Ensure the socket is closed after the operation
        client.close()