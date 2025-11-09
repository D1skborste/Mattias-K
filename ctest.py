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
            

def start_multiscan(targets, start_ports, max_ports, timeout, file_name):
    
    targets_count = 0
    for ips, start_port, max_port, in zip(targets, start_ports, max_ports):
        targets_count += 1
        print(targets_count, ips, start_port, max_port, timeout, file_name)

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [TARGET or FILE] [PORTS] [TIMEOUT] [OPTIONS]",
        description="Idiot-proof port-scanner. Accepts 0-4 CLI arguments in any order."
    )
    parser.add_argument('args', nargs='*', help="Positional arguments: target, ports, timeout")
    parser.add_argument('-p', nargs=2, type=int, help="Specify [start_port] and [max_port]")
    parser.add_argument('-t', type=float, help="Set a [timeout] for each port (default is 1 sec)")
    parser.add_argument('-s', default='port_results.txt', help="Specify name for save file <*.txt>")
    parser.add_argument('-r', nargs='?', const='run', help="Run default scan from <ip_list.txt>")
    return parser

def parse_positional_args(args):
    ports = []
    targets = []
    timeout = None

    for arg in args:
        try:
            val = float(arg)
            if val.is_integer() and int(val) < 65536:
                ports.append(int(val))
            else:
                timeout = timeout or val
        except ValueError:
            targets.append(arg)
    
    return targets, ports, timeout

def get_save_location(filename):
    return filename if filename.endswith('.txt') else f"{filename}.txt"

def prompt_for_defaults():
    choice = input("Press 'R' to run with defaults, or 'C' to customize: ").lower()
    if choice == 'r':
        return True
    elif choice == 'c':
        target = input("Enter target (IP/domain/file): ")
        start_port = int(input("Start port: "))
        max_port = int(input("Max port: "))
        return False, [target], [start_port, max_port]
    else:
        sys.exit()

def main():
    parser = init_argparse()
    args = parser.parse_args()

    targets, ports, timeout = parse_positional_args(args.args)
    start_port, max_port = (None, None)
    print("TARG", targets, "PORT", ports, "TIMEOUT", timeout)
    if args.p:
        start_port, max_port = sorted(args.p)
    elif len(ports) == 2:
        start_port, max_port = sorted(ports)
    elif len(ports) == 1:
        timeout = timeout or ports[0]

    timeout = float(args.t) if args.t else timeout or 0.5
    file_name = get_save_location(args.s)
    print("ARGS_R", args.t)
    print("TARG", targets, "PORT", start_port, max_port, "TIMEOUT", timeout)
    #if args.r:
        #targets, start_ports, max_ports = read_targets_list()
    
    if args.r: #and args.r != '69':
        targets = ['ip_list.txt']

    if not targets and not args.r:
        parser.print_help()
        use_default = prompt_for_defaults()
        if use_default is True:
            targets = ['ip_list.txt']
        else:
            _, targets, ports = prompt_for_defaults()
            start_port, max_port = ports

    # Final scan call
    start_multiscan(targets, [start_port]*len(targets), [max_port]*len(targets), timeout, file_name)
    
"""print("Timeout",type(timeout), timeout)
print('Target', targets)
print('Start', start_ports, 'Max', max_ports)
print(file_name)"""

if __name__ == "__main__":
    main()

"""
1. Group Related Logic into Functions
Encapsulate logic like argument parsing, input classification, and default handling into separate functions.
2. Avoid Global Variables
Use function parameters and return values instead of relying on global state.
3. Simplify Argument Parsing
Instead of using four positional arguments (first, second, etc.), consider using nargs='*' to accept a flexible list.
4. Use Meaningful Variable Names
Avoid vague names like pargs, argvalues, i. Use port_args, positional_args, arg, etc.
5. Avoid Repetitive Checks
Use helper functions for repeated logic like checking if a string is a float or port.

Modular: Easier to test and maintain.
Readable: Clear separation of concerns.
Robust: Handles edge cases more gracefully.
Scalable: Easier to extend with new features."""