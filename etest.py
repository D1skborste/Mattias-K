import sys
import argparse
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

"""IS THIS SPAGHETTI CODE??!?"""

"""
Drawbacks:
Att göra:

Trying to clean up code. Put stuff in functions etc
Can i clean up all if/elif/else... for while loops? under __name__ ?
Can i clean up timeout defaults? It's like 3 different ones
Another option (add-list or new-list, to manually add ip/port into the targets list)

"""

def read_targets_list(ip_list="ip_list.txt"):
    with open (ip_list) as r:
        targets_list = []
        # Each line in the .txt is an IP, with or without ports
        for line in r.readlines():
            # It will go through each line, remove prefix and suffix
            row = line.removeprefix("http://").removesuffix("\n")
            # Whatever format the ip and ports are entered in the list, it will substitute the characters for a space, before splitting
            row = re.sub(r'[-/:_,\\]', ' ', row).split(" ")
            # IP and port range in correct format are appended to target list 
            targets_list.append(row)
        r.close()
    print("HELLO", targets_list)
    # The target list is split in three lists: targets, start_port and max_port
    for x in targets_list:
        targets.append(x[0])
        # With no ports set in list, it will use a default value
        try:
            start_ports.append(x[1])
            max_ports.append(x[2])
        except:
            start_ports.append("NULL")    
            max_ports.append("NULL")
    


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
        



# Initial function to set accepted arguments. Optional with '-' prefix, and "positional" without prefix.
def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [TARGET or FILE] [PORTS] [TIMEOUT] [OPTIONS] ",
        description="'Idiot-proof' port-scanner. Any 0-4 CLI arguments in any order will work. It will scan a list, IP or domain.\
            options will override CLI. input from <ip_list>, to output <port_results.txt>. Default [timeout] is 0.5 sec",
       
    )
    parser.add_argument('first', nargs='?', help=argparse.SUPPRESS)
    parser.add_argument('second', nargs="?", help=argparse.SUPPRESS)
    parser.add_argument('third', nargs="?", help=argparse.SUPPRESS)
    parser.add_argument('fourth', nargs="?", help=argparse.SUPPRESS)
    parser.add_argument('-p', nargs=2, help="Specify [start_port] and [max_port]")
    parser.add_argument('-t', help="Set a [timeout] for each port (default is 1 sec)" )
    parser.add_argument('-s', help="Specify name for save file <*.txt>", default='port_results.txt' )
    parser.add_argument('-r', nargs='?', default='69', help="Run the port-scanner from <ip_list.txt> -> save results in <port_results.txt>. With a default [timeout] of 0.5 sec, unless specified with [-t]" )
    
    return parser


# Flag checks. Timeout doesn't have a flag, as it's only one line.
no_args = False
flag_p = False
flag_s = False
flag_r = False


max_port = [] # Set to accept an input, or check for a lack thereof. 
userinput = [] # Set to accept an input, or check for a lack thereof.
pargs = [] # Cache for storing, and sorting the arguments
parser = init_argparse() # Returned parser class to create a 'Namespace' object as a string.
arg_dict = vars(parser.parse_args()) # Convert this object into a dictionary.
argvalues = list(arg_dict.values()) # Convert the dictionary values into a list.
argvalues = argvalues[0:4] # We only need the first 4 arguments, for processing and sorting the input. 


timeout = arg_dict["t"]


# Convert the positional arguments to a set, to look for inputs. If no inputs were made, it will print the 'help'.
if len(set(argvalues)) == 1 and set(argvalues) == {None}:
    no_args = True # Asks for userinput: "RUN DEFAULT" OR "CUSTOM SEARCH"



for i in argvalues: # Iterates the list of positional arguments,
    if i != None: # Some checks will be performed with each discovered value
        try: 
            if len(i) < 6: # If lenght is above a threshold, it can't be a port. 
                pargs.append(int(i)) # Can i be converted to an int, it will be added to a temporary list of parsed args. 
            elif len(i) >= 6: 
                userinput.append(i) # It's saved for later, to be processed for a list, IP or domain.

        except:
            try: # Failed int conversion will check for a float conversion.
                if not timeout: # If successful and there's no timeout yet set, it will be added to a timeout list.
                    timeout = []
                    timeout.append(float(i))
                    timeout.sort()
                    timeout = timeout[0] # In the event of several floats, the lowest will be used for timeout

            except: # As a last resort, it will be added to the list of targets. 
                userinput.append(i) # It also means you can set up to 4 targets from the CLI.


if pargs: # If any ints were added to the temp list, they will be sorted
    pargs.sort() # Timeout is supposed to be the lowest value
    if not timeout and len(pargs) == 1:
        timeout = pargs[0]
# Different actions depending on how many args in the list
    elif len(pargs) == 2:
        start_port = pargs[0]
        max_port = pargs[1]
        
    elif len(pargs) == 3:
        if timeout:
            start_port = pargs[0]
        else:
            timeout = pargs[0]
            start_port = pargs[1]
        max_port = pargs[-1]
        


# Checks for optional flags in the CLI, from the dict version of the args.
if arg_dict["p"]: # Flag [-p] for ports, it forces 2 'nargs', min and max port
    pargs = arg_dict.get("p")
    pargs.sort()
    start_port = pargs[0]
    max_port = pargs[1]
    flag_p = True # Flag is set for future checks

# Function for specific save location. It may be called as a modifier when running the script, to overwrite default location.
def save_location(): # If the user doesn't type '.txt' after file name, it will be added automatically.
    if ".txt" not in arg_dict["s"]:
        file_name = arg_dict["s"]
        file_name += ".txt"
    else:
        file_name = arg_dict["s"]
    return file_name

# Shortcut to run default program, as is. As long as the user doesn't type "-r 69" in the CLI. 
run_default = arg_dict['r']
if run_default != "69":
    flag_r = True # Another flag set for future checks

# The function for default script. But optional flags can overwrite some values.
def run_default_scan():
    timeout = arg_dict["t"]
    #if run_default != "69":
    userinput = ["ip_list.txt"]
    file_name = save_location() # Calls for the save location. Default file name unless the user calls for a different name.
    if not timeout: # Checks if timeout is set, will use a default value if not.
        timeout = 0.5
    return userinput, file_name, timeout # Returns 3 variables.



"""WHERE TO PUT if __name__ == "__main__": ??"""


#if __name__ == "__main__":

# Sets a default save location
file_name = save_location()

# Multiple flag checks to verify the lack of user input. It will then show a "help menu" with the availible arguments
if no_args == True and flag_p == False and flag_r == False:
    parser.print_help() # Asks the user to run the default program, or enter custom variables with input prompts.
    first_use = input(BLUE + "If this is your first time, press 'R' to run with defaults, or 'C' to set prompted rules: " + RESET)

    # Sets the "default" flag, if user affirms.
    if first_use == 'r' or first_use == 'R' or run_default != "69":
        flag_r = True
    # Prompts the user for inputs, if that option is picked.
    elif first_use == 'c' or first_use == 'C':
        usertarget = input(BLUE + 'Enter <IP>, <domain> or file <*.txt>: ' + RESET)
        start_port = int(input(BLUE + 'Set default starting port: ' + RESET))
        max_port = int(input(BLUE + 'Set default ending port: ' + RESET))
        userinput.append(usertarget)
    # If neither option is chosen, the script will end.
    else: 
        sys.exit()

if flag_r: # If the 'default' flag is set, the default function is called to set the default variables.
    userinput, file_name, timeout = run_default_scan()


# The final lists used to scan multiple targets.
start_ports = []
max_ports = []
targets = []

# Checks the userinputs to identify a text file, domain or ip.
for t in userinput:
    if ".txt" in t:
        read_targets_list(t)     

    elif "http" in t:
        domain = t.split("://")
        targets.append(domain[1])
        
    else:
        targets.append(t)
if not targets:
    read_targets_list()

# If ports are not set, or lacking from the target file, it will ask the user for input.
while len(start_ports) < len(targets) or len(max_ports) < len(targets) or "NULL" in start_ports:
    if not max_port: 
        # Ports will be used as defaults, for when target list doesn't specify.
        start_port = int(input(BLUE + 'Not all targets have a set port range. Set default starting port: ' + RESET))
        max_port = int(input(BLUE + 'Set default ending port: ' + RESET))
    
    # To nos lose corresponding port to ip from target list, it will set the string "NULL" in it's place.
    # Before then replacing all "NULL" in each list.
    if "NULL" in start_ports:
        start_ports = [x if x != "NULL" else start_port for x in start_ports]
        max_ports = [x if x != "NULL" else max_port for x in max_ports]

    else:
        start_ports.append(start_port)
        max_ports.append(max_port)


# If no timeout are set, the user will be asked to set one, or press enter to use default value.
if not timeout:
    inp_timeout = input(f"{BLUE}Set a port timeout {RESET}(or <CR> for 0.5)")
    if inp_timeout:
        timeout = float(inp_timeout)
    else:
        timeout = 0.5
timeout = float(timeout)


"""print("Timeout",type(timeout), timeout)
print('Target', targets)
print('Start', start_ports, 'Max', max_ports)
print(file_name)"""
start_multiscan(targets, start_ports, max_ports, timeout, file_name)


"""Problems:
broke sorting, default timeout, default run, custom ports for each ip (and with it, set fallback ports)
Doesn't process the userinputs

heje.com 5 3 2 4 -t 3 --- will output ports 3 5, timeout 3...
fix so that port 2 is first if -t is used"""