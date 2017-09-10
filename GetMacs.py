###########
# Python3 program to scan the local area network for valid MAC addresses
#
# Author - Michael O'Connor
#
# Date: 9/10/2017
#
##########

import os
import sys
import subprocess

# Execute command to step through /24 network addresses and return result
# In this case, we are using the ARP command to query associated MAC addreses

def get_macs(net):

  host = 1

  while host <= 254:
     ip_addr = "{}.{}".format(net, str(host))			# Form complete IPv4 address (Python3)
     cmd = ["arp", "-i", "en0", ip_addr]			# Form array to be passed to subprocess.Popen()

     p_stdout = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None) # execute command

     out_str = p_stdout.communicate("n\n")[0].decode('utf-8').strip(' ')   # wait for complete and reformat to string

     out_array = out_str.split()					   # Split string into array of words

     if out_array[0].startswith('?'):					   # Test for valid IP address
       print ("IP:{}\tMAC:{}".format(out_array[1], out_array[3]))

     host += 1

# Define a main() function that prints a little greeting.
def main():
  # Get the cmd from the command line, using 'date' as a fallback.
  if len(sys.argv) >= 2:
    addr = sys.argv[1]
  else:
    addr = '192.168.0'

  print("Scanning Network: {}".format(addr))
  
  print(get_macs(addr))

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
