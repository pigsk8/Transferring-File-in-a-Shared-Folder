#!/usr/bin/env python
#

MYPORT = 8123
MYTTL = 1 # Increase to reach other networks
ADDR = " " 
PORT = 0

import time
import struct
import socket
import sys
  
def main(grupo6):
        receiver(grupo6)
  

 #funcion para obtener la direccion ipv6 que nos envia el server el cual nos va servir para la comunicacion no multicasts 
def decodificar_direccion (sender):
    #str(sender).split("'")
    part = str(sender)[2:]
    cont = 0
    while part[cont] != "%" :
        cont = cont + 1 
    global ADDR 
    ADDR = part[:cont]
    print ADDR


#funcion para obtener el puerto por el cual nos vamos a comunicar con el server
def decodificar_puerto (sender):        
    puerto = str(sender).split(",")
    PORT= int(puerto[1])
    print PORT 

def receiver(group):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(group, None)[1]

    bandera = True
    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    
    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
    # Bind it to the port
    s.bind(('', MYPORT))
  
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    mreq = group_bin + struct.pack('@I', 0)
    s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
  
    # Loop, printing any data we receive
    while bandera :
        data, sender = s.recvfrom(1500)
        while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
        decodificar_direccion(sender)
        decodificar_puerto(sender)
       
        #para que solo reciba una vez el mensaje multicast
        if str(sender)[2] == 'f':
                bandera = False 
                
        
  
