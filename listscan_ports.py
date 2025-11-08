#!/usr/bin/env python3
"""
Network Scanner Project - Continuation
By: Mattias.K
Date: 251021

O.G Students: Björn, Daniel, Mattias.K, Lukas.S, Vien

"""
# Importing modules
import re
import socket
import sys
from tqdm import tqdm
from colorama import init, Fore

# Init colors
init()
RED = Fore.RED
GREEN = Fore.GREEN
MAGENTA =Fore.MAGENTA
BLUE = Fore.BLUE
RESET = Fore.RESET

"""To do:
Fix readme
Comments
Ask for user for ports only when necessary
"""



def read_targets_list(ip_list="ip_list.txt"):
    with open (ip_list) as r:
        targets_list = []
        # Each line in the .txt is an IP, with or without ports
        for line in r.readlines():
            # It will go through each line, remove prefix and suffix
            row = line.removeprefix("http://").removesuffix("\n")
            # Whatever the ip/port format in the list, it will substitute the characters for a space, before splitting
            row = re.sub(r'[-/:_,\\]', ' ', row).split(" ")
            # IP and port range in correct format are appended to target list 
            targets_list.append(row)
        r.close()

    # The target list is split in three lists: targets, start_port and max_port
    for x in targets_list:
        targets.append(x[0])
        # If no ports are set in target_list, it will use a default value set by the user
        try: # Converting str to int
            start_ports.append(int(x[1]))
            max_ports.append(int(x[2]))
        except:
            start_ports.append("NULL")
            max_ports.append("NULL")
        
        


# Set range of ports, including the max port
def start_multiscan(targets, start_port, max_port, timeout, file_name="port_results.txt"):
    try:
        with open(file_name, "w") as f:
            #Counting each target for the progress bar
            targets_count = 0
            # Merging the split targets_list
            for ips, start_port, max_port in zip(targets, start_ports, max_ports):                
                total_targets = len(targets)
                targets_count += 1
                # Where the open ports are saved, reset for each target.
                open_ports = []  
                target = socket.gethostbyname(ips)
                # Optional text in save file when only scanning one port
                if start_port == max_port:
                    f.write(f"{'='*60}\nScanning target IP {target} : Port {start_port} \n")
                else:
                    f.write(f"{'='*60}\nScanning target IP {target} : Ports {start_port}-{max_port} \n")
                # Calculation for progress bar
                total_ports = max_port - start_port + 1
                with tqdm(total=total_ports, desc=f"{MAGENTA}Scanning target [{targets_count} of {total_targets}], port [{start_port}] to [{max_port}]", unit="port") as progress_bar:

                # Set range of ports, including the max port
                    for port in range(start_port, max_port + 1):
                        #AF_INET = IPv4, SOCK_STREAM = constant, create a TCP socket
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        # Try to connect port with time out
                        try:
                            s.settimeout(timeout)
                            # Returns to 0 if a port is open
                            result = s.connect_ex((target, port))
                            # If a port is open, add the open port to the open_ports list
                            if result == 0:

                                # Try to identify the port service
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
                                        # Add open port to the open_ports list
                                        open_ports.append(f"Port {port} : Banner {banner}")
                                        f.write(f"Port {port} : Banner {banner}\n")
                                        #progress_bar.write(f"\nBanner for {target}:{port} -> {banner}")
                                    else:
                                        open_ports.append(f"Port {port} : No banner received")
                                        f.write(f"Port {port} : No banner received\n")
                                        #progress_bar.write(f"\nNo banner received for {target}:{port}")

                                # Socket timed out error
                                except socket.timeout:
                                    open_ports.append(f"Port {port} : No banner (timeout)")
                                    f.write(f"Port {port} : No banner (timeout)\n")
                                    #progress_bar.write(f"\nNo banner (timeout) for {target}:{port}")
                                # Catch other errors
                                except Exception as e:                                
                                    open_ports.append(f"Port {port} : Error reading banner {e}")
                                    f.write(f"Port {port} : Error reading banner {e}\n")
                                    #progress_bar.write(f"\nError reading banner for {target}:{port}: {e}")
                        # DNS lookup failed error
                        except socket.gaierror as e:
                            f.write(f"{target} Hostname could not be resolved. {e}\n")
                            return open_ports
                        # Socket error
                        except socket.error as e:
                            f.write(f"{target} Could not connect to server. {e}\n")
                            return open_ports
                        # Close socket
                        finally:

                            s.close()
                            progress_bar.update(1)
                    if not open_ports:
                        f.write(f"No ports are open for {target}\n")
        
        # 'Scan complete' message will appear, once all targets are scanned,
        if targets_count == total_targets:
            print(f"{GREEN}Scan complete. Results saved in '{file_name}'")    
    except FileNotFoundError:
        print(f"{RED}File not found.")
    # Writing to file errors
    except IOError as e:
        print(f"{RED}An I/O error occurred.", e)
    # Other errors
    except Exception as e:
        print(f"{RED}Something went wrong...", e)
    # Close file
    f.close()



# Run the program
if __name__ == "__main__":
    timeout = 0.2
    start_ports = []
    max_ports = []
    max_port = []
    targets = []   
    
    if len(sys.argv) == 5:
        userinput = sys.argv[1]
        start_port = int(sys.argv[2])
        max_port = int(sys.argv[3])
        inp_timeout = float(sys.argv[4])
        
    elif len(sys.argv) == 4:
        userinput = sys.argv[1]
        start_port = int(sys.argv[2])
        max_port = int(sys.argv[3])
        inp_timeout = input(BLUE + "(Optional) Set timout for each port: ")

    elif len(sys.argv) == 3:
        userinput = str(input(BLUE + 'Enter <IP>, <domain> or file <*.txt>: '))
        start_port = int(sys.argv[1])
        max_port = int(sys.argv[2])
        inp_timeout = input("(Optional) Set timout for each port: ")

    elif len(sys.argv) == 2:
        userinput = sys.argv[1]
#        start_port = int(input('Set default starting port: '))
#        max_port = int(input('Set default ending port: '))
        inp_timeout = input("(Optional) Set timout for each port: ")
            
    else:
        userinput = str(input(BLUE + 'Enter <IP>, <domain> or file <*.txt>: '))
#        start_port = int(input('Set default starting port: '))
#        max_port = int(input('Set default ending port: '))
        inp_timeout = input("(Optional) Set timout for each port: ")

    if not userinput:
        read_targets_list()

    elif ".txt" in userinput:
        read_targets_list(userinput)                 
                
    elif "http" in userinput:
        domain = userinput.split("://")
        targets.append(domain[1])
        
    else:
        targets.append(userinput)
        
    while len(start_ports) < len(targets) or len(max_ports) < len(targets) or "NULL" in start_ports:
        if not max_port: 
            # Ports will be used as defaults, for when target list doesn't specify.
            start_port = int(input(BLUE + 'Not all targets have a set port range. Set default starting port: ' + RESET))
            max_port = int(input(BLUE + 'Set default ending port: ' + RESET))
        
        # To no lose corresponding port to ip from target list, it will set the string "NULL" in it's place.
        # Before then replacing all "NULL" in each list.
        if "NULL" in start_ports:
            start_ports = [x if x != "NULL" else start_port for x in start_ports]
            max_ports = [x if x != "NULL" else max_port for x in max_ports]

        else:
            start_ports.append(start_port)
            max_ports.append(max_port)

    if inp_timeout:
        timeout = float(inp_timeout)
        
    # Scan the give url with start and end ports
    start_multiscan(targets, start_ports, max_ports, timeout)