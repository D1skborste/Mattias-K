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
    



def start_multiscan(targets, start_port, max_port, timeout, file_name="port_results.txt"):
    count = 0
    for ips, start_port, max_port, in zip(targets, start_ports, max_ports):
        count += 1
        print(count, ips, start_port, max_port, timeout, file_name)
        

"""IS THIS SPAGHETTI CODE??!?"""

        
"""
Att göra:

Trying to clean up code. Put stuff in functions etc
Can i clean up all if/elif/else... for while loops? under __name__ ?
(Maybe do a check, instead of writing, and rewriting args, like ["t"])

Halt program without args, or ask user if they want to continue
"""

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [target or file] [-h] ",
        description="'Idiot-proof' port-scanner. Any 0-4 arguments in any order will work. Use [-r] to run with all default values: \
            input from <ip_list>, to output <port_results.txt>. Default [timeout] is 0.5 sec",
       
    )
    parser.add_argument('first', nargs='?', )
    parser.add_argument('second', nargs="?", )
    parser.add_argument('third', nargs="?", )
    parser.add_argument('fourth', nargs="?", )
    parser.add_argument('-p', nargs=2, help="Specify [start_port] and [max_port]")
    parser.add_argument('-t', help="Set a [timeout] for each port (default is 1 sec)" )
    parser.add_argument('-s', help="Specify name for save file <*.txt>", default='port_results.txt' )
    parser.add_argument('-r', nargs='?', default='69', help="Run the port-scanner from <ip_list.txt> -> save results in <port_results.txt>. With a default [timeout] of 0.5 sec." )
    
    return parser


no_args = False
#list_2 = [num for num in list_1 if isinstance(num, (int,float))]
#def parse_pos_args():
max_port = []
#start_port = []
userinput = []
sargs = []
pargs = [] # Cache for storing, and sorting the arguments
parser = init_argparse()
arg_dict = vars(parser.parse_args())
#arg_dict = vars(args)
argvalues = list(arg_dict.values())
argvalues = argvalues[0:4]


timeout = arg_dict["t"]

if len(set(argvalues)) == 1 and set(argvalues) == {None}:
    parser.print_help()
    no_args = True

if not no_args:
    for i in argvalues[0:4]:
        if i != None:
            if len(i) >= 6:
                userinput = i
        
        try:
            int(i)
            pargs.append(int(i))
        except:
            try:
                float(i)
                timeout.append(float(i))
            except:
                None



if pargs:
    pargs.sort()
    if not timeout and len(pargs) != 2:
        timeout = pargs[0]
    if len(pargs) == 2:
        start_port = pargs[0]
        max_port = pargs[1]
    elif len(pargs) == 3:
        start_port = pargs[1]
        max_port = pargs[2]


if arg_dict["t"]:
    timeout = arg_dict["t"]

if arg_dict["p"]:
    pargs = arg_dict.get("p")
    pargs.sort()
    start_port = pargs[0]
    max_port = pargs[1]

if arg_dict["s"]:
    if ".txt" not in arg_dict["s"]:
        file_name = arg_dict.get("s")
        file_name += ".txt"
    else:
        file_name = arg_dict.get("s")
        
run_default = arg_dict['r']
if run_default != "69":
    userinput = "ip_list.txt"
    file_name = "port_results.txt"
    timeout = 37
        #timeout = float(timeout)
    #return userinput, start_port, max_port, timeout





if __name__ == "__main__":
    #parser.print_help()
    
    #userinput = []
    start_ports = []
    max_ports = []
    #userinput, start_port, max_port, timeout = parse_pos_args()
    #parse_pos_args()
    #targets = userinput_parse()
    targets = []
    if not userinput:
        read_targets_list()
    
    #print(argvalues[0:4])
    #if argvalues[0:4]:

    elif ".txt" in userinput:
        read_targets_list(userinput)     

    elif "http" in userinput:
        domain = userinput.split("://")
        targets.append(domain[1])
        
    else:
        targets.append(userinput)    



    while len(start_ports) < len(targets) or len(max_ports) < len(targets) or "NULL" in start_ports:
        if not max_port: #or not start_port:
            start_port = int(input(BLUE + 'Set default starting port: '))
            max_port = int(input(BLUE + 'Set default ending port: ' + RESET))
                
        if "NULL" in start_ports:
            start_ports = [x if x != "NULL" else start_port for x in start_ports]
            max_ports = [x if x != "NULL" else max_port for x in max_ports]

        else:
            start_ports.append(start_port)
            max_ports.append(max_port)



    if not timeout:
        inp_timeout = input(f"{BLUE}Set a port timeout {RESET}(or <CR> for 0.2)")
        if inp_timeout:
            timeout = float(inp_timeout)
        else:
            timeout = 0.5
    timeout = float(timeout)
    
    print("Timeout",type(timeout), timeout)
    print('Target', targets)
    print('Start', start_ports, 'Max', max_ports)
    print(file_name)
    start_multiscan(targets, start_ports, max_ports, timeout, file_name)
