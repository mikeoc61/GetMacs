###########
# Python3 program to scan the local area network for valid MAC addresses
#
# Basically does the same thing that "arp -a" but more brute force and
# with output formatting.
#
# Author - Michael O'Connor
#
# Date: 9/10/2017
#
##########

import os
import sys
import subprocess

# Default network address space to search if not otherwise provided by user

Default_net = '192.168.1'

# Execute command to step through /24 network addresses and return result
# In this case, we are using the ARP command to query associated MAC addreses

def get_macs(net):

  host = 1

  # Print out a nice header

  print('      Name                 IP                MAC Addr')
  print('-' * 60)

  while host <= 254:
     ip_addr = "{}.{}".format(net, str(host))		# Form complete IPv4 address (Python3)
     cmd = ["arp", "-i", "en0", ip_addr]			# Form array to be passed to subprocess.Popen()

     p_stdout = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None) # execute command

     out_str = p_stdout.communicate("n\n")[0].decode('utf-8').strip(' ')   # wait for complete and reformat to string

     out_array = out_str.split()					   # Split string into array of words

     if out_array[3].startswith('no') == False:		   # Test for valid IP address
        print ("\n{0:20} {1:20} {2:20}".format(out_array[0], out_array[1], out_array[3]))
#     else:
#        print('.', end='', flush=True)

     host += 1

# Parse command line for network to be scanned or use default if not provided
def main():
  # Get the cmd from the command line, using 'typical /24 LAN' as a fallback.
  if len(sys.argv) >= 2:
    addr = sys.argv[1]
  else:
    addr = Default_net

  print("Scanning Network: {}".format(addr))

  get_macs(addr)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__': main()
