import argparse
import sys
import re
import socket
from tqdm import tqdm
from colorama import init, Fore

# Init colors
init()
RED = Fore.RED
GREEN = Fore.GREEN
MAGENTA =Fore.MAGENTA
BLUE = Fore.BLUE
RESET = Fore.RESET

"""Att göra:
Sätt färger på console texten
Sätt under "first_use" 'c', target input, och description att default körs från 'ip_list.txt'
Another option (add-list or new-list, to manually add ip/port into the targets list)
Trying to clean up code some more. Put stuff in functions etc
Add comments
"""

def read_targets_list(ip_list="ip_list.txt"):
    targets_list = []
    with open(ip_list) as r:
        for line in r.readlines():
            row = line.removeprefix("http://").removesuffix("\n")
            row = re.sub(r'[-/:_,\\]', ' ', row).split(" ")
            targets_list.append(row)
        r.close()
        
    targets = []
    start_ports = []
    max_ports = []
    
    for x in targets_list:
        targets.append(x[0])
        try:
            start_ports.append(x[1])
            max_ports.append(x[2])
        except IndexError:
            start_ports.append("NULL")
            max_ports.append("NULL")

    return targets, start_ports, max_ports
            

def targets_processing(t):
    targets = []
    start_ports = ["NULL"]
    max_ports = ["NULL"]
    
    if "http" in t:
        domain = t.split("://")
        targets.append(domain[1])
    else:
        targets.append(t)
    return targets, start_ports, max_ports



def start_multiscan(targets, start_port, max_port, timeout, file_name):
    try:
        with open(file_name, "w") as f:
            #Counting each target for the progress bar
            targets_count = 0
            # Merging the split targets_list
            for ips, start_port, max_port in zip(targets, start_ports, max_ports):
                start_port = int(start_port)
                max_port = int(max_port)      
                #print(type(targets), type(ips), type(start_port), type(max_port), type(timeout), type(file_name))          
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



def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [TARGET or FILE] [PORTS] [TIMEOUT] [OPTIONS]",
        description="'Idiot-proof' port-scanner. Any amounts of arguments in any order will work. It will scan a list, IP or domain.\
            options will override CLI. input from <ip_list>, to output <port_results.txt>. Default [timeout] is 0.5 sec",
    )
    parser.add_argument('args', nargs='*', help="Enter some file names, ips, domains and numbers for ports. If you want to, or don't, it will then ask you for the missing information")
    parser.add_argument('-p', nargs=2, type=int, help="Specify [start_port] and [max_port]")
    parser.add_argument('-t', type=float, help="Set a [timeout] for each port (default is 0.5 sec)")
    parser.add_argument('-s', default='port_results.txt', help="Specify name for save file <*.txt>")
    parser.add_argument('-r', nargs='?', const='run', help="Run default scan from <ip_list.txt>")
    return parser


def parse_positional_args(args):
    ports = []
    userinput = []
    timeout = []

    for arg in args:
        try:
            val = float(arg)
            if val.is_integer() and int(val) < 65536:
                ports.append(int(val))
            else:
                timeout.append(val)
        except ValueError:
            userinput.append(arg)
    
    if timeout:
        timeout.sort()
        timeout = timeout[0] # In the event of several floats, the lowest will be used for timeout # In the event of several floats, the lowest will be used for timeout
    
    timeout = timeout or None
    return userinput, ports, timeout




def get_save_location(filename):
    return filename if filename.endswith('.txt') else f"{filename}.txt"



def run_default_scan():
    choice = input(BLUE + "If this is your first time, press 'R' to run with defaults, or 'C' to set prompted rules: " + RESET).lower()
    if choice == 'r':
        return True
    elif choice == 'c':
        return False
    else: # If neither option is chosen, the script will end.
        sys.exit()



def main():
    global start_ports, max_ports, targets
    start_ports = []
    max_ports = []
    targets = []
    
    parser = init_argparse()
    args = parser.parse_args()
    userinput, ports, timeout = parse_positional_args(args.args)
    start_port, max_port = (None, None)
    if args.p:
        start_port, max_port = sorted(args.p)
    elif len(ports) == 2:
        start_port, max_port = sorted(ports)
    elif len(ports) == 1:
        timeout = timeout or ports[0]
    elif len(ports) >= 3:
        ports = sorted(ports)
        if timeout:
            start_port, max_port = ports[0], ports[-1]
        else:
            timeout, start_port, max_port = ports[0], ports[1], ports[-1]


        
    file_name = get_save_location(args.s) # Calls for the save location. Default file name unless the user calls for a different name.

    
    if args.r:
        targets, start_ports, max_ports = read_targets_list()
    

    if not userinput and not args.r:
        parser.print_help()
        #userinput, file_name, timeout = run_default_scan()
        use_default = run_default_scan()
        if use_default is True:
            targets, start_ports, max_ports = read_targets_list()
        else:
            usertarget = input(BLUE + 'Enter <IP>, <domain> or file <*.txt>: ' + RESET)
            start_port = int(input(BLUE + 'Set default starting port: ' + RESET))
            max_port = int(input(BLUE + 'Set default ending port: ' + RESET))
            userinput.append(usertarget)
                        
    # Checks the userinputs to identify a text file, domain or ip.
    for t in userinput:
        if ".txt" in t: # Appends the list contents to the working list
            targets, start_ports, max_ports = map(lambda x: x[0]+x[1], zip((targets, start_ports, max_ports), read_targets_list(t)))
        else: # To not lose corresponding port to ip from target list, it will set the string "NULL" in it's place.
            targets, start_ports, max_ports = map(lambda x: x[0]+x[1], zip((targets, start_ports, max_ports), targets_processing(t)))
    if not userinput: # Without
        targets, start_ports, max_ports = read_targets_list()


    
    # If ports are not set, or lacking from the target file, it will ask the user for input.
    while len(start_ports) < len(targets) or len(max_ports) < len(targets) or "NULL" in start_ports:
        if not max_port: 
            # Ports will be used as defaults, for when target list doesn't specify.
            start_port = int(input(BLUE + 'Not all targets have a set port range. Set default starting port: ' + RESET))
            max_port = int(input(BLUE + 'Set default ending port: ' + RESET))
        
        
        # Before then replacing all "NULL" in each list.
        if "NULL" in start_ports:
            start_ports = [x if x != "NULL" else start_port for x in start_ports]
            max_ports = [x if x != "NULL" else max_port for x in max_ports]



    # If no timeout are set, the user will be asked to set one, or press enter to use default value.
    timeout = float(args.t) if args.t else timeout
    if not timeout:
        inp_timeout = input(f"{BLUE}Set a port timeout {RESET}(or <CR> for 0.5)")
        if inp_timeout:
            timeout = float(inp_timeout)
        else:
            timeout = 0.5
            
    """print("Timeout",type(timeout), timeout)
    print('Target', targets)
    print('Start', start_ports, 'Max', max_ports)
    print(file_name)"""
    
    # Final scan call
    start_multiscan(targets, start_ports, max_ports, timeout, file_name)
    
    
if __name__ == "__main__":
    main()

