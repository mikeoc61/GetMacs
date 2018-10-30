###########
# Python3 program to scan the local area network for valid MAC addresses
#
# Basically does the same thing that "arp -a" but more brute force and
# with output formatting. Only tested on MacOS and Linux.
#
# Date: 9/10/2017
# Revised: 10/30/2018
#
##########

__author__      = "Michael E. O'Connor"
__copyright__   = "Copyright 2018"

import os
import sys
import platform
import subprocess

# Default network address space to search if not otherwise provided by user

Default_net = '192.168.1'
cmd_base = ['arp']

# Execute command to step through /24 network addresses and return result
# In this case, we are using the ARP command to query associated MAC addreses

def get_macs(net):

    host_type = platform.system()
    if host_type == 'Darwin':
        cmd_base = 'arp'
    elif host_type == 'Linix':
        cmd_base = 'arp -a'
    else:
        print(f'Sorry, host type [{host_type}] is not supported')
        raise SystemExit()

    # Print out a nice header

    print('      Name                 IP                MAC Addr')
    print('-' * 60)

  # Main iterative loop

    for host in range(1,255):

        # Cmd needs to be formatted as an array of strings

        cmd = f'{cmd_base} {net}.{str(host)}'.split()
        # print(f'command = {cmd}')

        # Send command to Operating Environment as array of strings
        p_stdout = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None)

        # Wait for complete and reformat to string
        out_str = p_stdout.communicate("n\n")[0].decode('utf-8').strip(' ')

        # Split resulting string into array of words for further parsing
        out_array = out_str.split()

        # Test for valid IP address, if valid then format output
        if out_array[3].startswith('no') == False:
            print ('{0:20} {1:20} {2:20}'.format(out_array[0], out_array[1], out_array[3]))

def main():

    # Get the cmd from the command line, using 'typical /24 LAN' as a fallback.

    arg_cnt = len(sys.argv)

    if arg_cnt > 2:
        print("Usage: {} <network>".format(sys.argv[0]))
        print("Example: {} 192.168.0".format(sys.argv[0]))
        raise SystemExit()
    elif arg_cnt == 2:
        addr = sys.argv[1]
    else:
        addr = Default_net

    print("Scanning Network: {}".format(addr))

    get_macs(addr)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__': main()
