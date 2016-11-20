#import socket, select, string, sys , struct, time 
import client4
import server4
import multireceiver
import multisender
import threading
import sys

def iniciar_multicast (grupo6):
    multisender.main(grupo6)    
    #print 'hola'

def iniciar_unicast(directorio):
	server4.iniciar(directorio)

def Iniciar_client_unicast(ADDR,directorio):
	client4.main(ADDR,directorio)	

def prueba():
	while 1:
		print 'prueba'	

def main (valor,grupo6,directorio):
    
    if valor == 1:
    #if int(sys.argv[1]) == 1 :
    	print 'Ha iniciado como servidor, iniciando multicast e anycast...'
    	thread = threading.Thread(target=iniciar_multicast,args=(grupo6,))
    	thread.start()
    	thread1 = threading.Thread(target=iniciar_unicast,args=(directorio,))
    	thread1.start()
    elif valor == 2:
        multireceiver.main(grupo6)
        #en caso de que agarre la ip de otra interfaz de red, meterla manual
        hilo = threading.Thread(target=Iniciar_client_unicast,args=(multireceiver.ADDR,directorio,))
        # lan  'fe80::3a60:77ff:fe4a:f063%eth0'
        # wifi 'fe80::762f:68ff:feb2:a231%wlan0'
        #hilo = threading.Thread(target=Iniciar_client_unicast,args=('fe80::762f:68ff:feb2:a231',directorio,))
        hilo.start()
       
    elif valor > 2:
    	hilo = threading.Thread(target=prueba)
    	hilo.start()
    
    

