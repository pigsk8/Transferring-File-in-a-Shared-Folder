#!/usr/bin/env python

  
MYPORT = 8123
MYTTL = 1 # Increase to reach other networks
  
import time
import struct
import socket
import sys
  
def main(grupo6):
    sender(grupo6)
    
  
  
def sender(group):
    addrinfo = socket.getaddrinfo(group, None)[0]
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    print addrinfo 
    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', MYTTL)
    s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)
  
    while True:
        data = repr(time.time())
        s.sendto(data + '\0', (addrinfo[4][0], MYPORT))
        time.sleep(1)
  
  

  
  
