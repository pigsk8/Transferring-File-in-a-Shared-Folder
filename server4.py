#!/usr/bin/python
import socket, select, os, sys, time
import pdb
import netifaces

# Lista para realizar un seguimiento de los descriptores de socket
CONNECTION_LIST = []
#Funcion transmitir data a un nuevo cliente con data existente
def enviar_data_nuevo (sock):
    for socket in CONNECTION_LIST:
        if socket == sock :
            try :  

                listaArchivo=os.listdir(os.getcwd())
                for i in range(len(listaArchivo)):
                    f=open(listaArchivo[i],"rb")
                    l = f.read()
                    total = len(l)
                    mensaje = '1,'+listaArchivo[i]+','+str(total)+','
                    tam = len(mensaje)
                    faltante = 1024-tam
                    j=0
                    x=1
                    while x==1:
                        mensaje = mensaje+'\0'
                        j=j+1;
                        if j==faltante:
                            x=0

                    socket.send(mensaje)

                    f.seek(0, 0)
                    l = f.read(1024)
                    socket.send(l)
                    while (l):
                        l=f.read(1024)
                        if l:
                            socket.send(l)
                    f.flush()
                    f.close()
                    time.sleep(2)
            except :
                # la conexion con el socket puede ser interrumpida, el cliente presiona Ctrl + C , por ejemplo
                socket.close()
                CONNECTION_LIST.remove(socket)

def enviar_eliminado(sock, nombre_arch,server_socket):
    
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try:
                mensaje= '2,'+nombre_arch+','
                tam = len(mensaje)
                faltante = 1024-tam
                i=0
                x=1                
                while x==1:
                    mensaje = mensaje+'\0'
                    i=i+1;
                    if i==faltante:
                        x=0
            
                socket.send(mensaje)
            except :
                # la conexion con el socket puede ser interrumpida, el cliente presiona Ctrl + C , por ejemplo
                socket.close()
                CONNECTION_LIST.remove(socket)

 
#Funcion para transmitir data a todos los clientes conectados
def enviar_data (sock, nombre_arch,server_socket):
    #No envie el mensaje a socket especifico y el cliente tiene que enviarnos el mensaje
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :        
                f=open(nombre_arch,"rb")            
                l = f.read()
                total = len(l)
                mensaje = '1,'+nombre_arch+','+str(total)+','
                tam = len(mensaje)
                faltante = 1024-tam

                i=0
                x=1                
                while x==1:
                    mensaje = mensaje+'\0'
                    i=i+1;
                    if i==faltante:
                        x=0

                socket.send(mensaje)
                
                f.seek(0, 0)
                l = f.read(1024)
                socket.send(l)
                while(l):
                    l = f.read(1024)
                    if l:
                        socket.send(l)
                f.flush()
                f.close()
                         
            except :
                # la conexion con el socket puede ser interrumpida, el cliente presiona Ctrl + C , por ejemplo
                socket.close()
                CONNECTION_LIST.remove(socket) 

def iniciar(directorio):

    #ipv6
    PORT = 5000
    addrs = netifaces.ifaddresses('eth0')
    dir_ipv6 = addrs[netifaces.AF_INET6][0]['addr']
    addr = (dir_ipv6,PORT)

    for res in socket.getaddrinfo(addr[0], addr[1], socket.AF_INET6,socket.SOCK_STREAM, socket.SOL_TCP):
        af, socktype, proto, canonname, sa = res

    server_socket = socket.socket(af,socktype,proto)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((sa))
    server_socket.listen(10)
 
    # Anadir socket del servidor a la lista de conexiones de lectura
    CONNECTION_LIST.append(server_socket)

    nuevacarpeta = str(os.getcwd())+'/'+directorio

    if not os.path.exists(nuevacarpeta):
        os.mkdir(nuevacarpeta)
     
    os.chdir(nuevacarpeta)
    print os.getcwd()
    listaArchivo = os.listdir(os.getcwd())

    while 1:
        # Obtener la lista de los sockets que estan listos para ser leidos
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #Nueva conexion
            if sock == server_socket:
                # Manejar el caso en el que hay una nueva conexion recibido a traves server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Cliente (%s, %s, %s, %s) conectado" % addr
                enviar_data_nuevo(sockfd)
                             
            #Algunos mensaje entrante desde un cliente
            else:
                # Los datos recibidos desde el cliente
                try:
                   # En Windows a veces cuando un programa TCP se cierra bruscamente  
          #se lanza una exepcion de conexion restablecida por el interlocutor
                    data0 = sock.recv(1024)
                    if data0:
                        if len(data0) == 1024:
                            keywords = data0.split(",")
                            tipo = int(keywords[0])
                            nombre_arch = keywords[1]

                            if tipo == 1:    
                                tam_arch = int(keywords[2])
                                f = open(nombre_arch,'wb')
                                
                                if tam_arch == 0:
                                    f.flush()
                                    f.close()
                                    print 'se agrego '+nombre_arch
                                    break
                                else:
                                    if tam_arch < 1024:
                                        data = sock.recv(tam_arch)
                                        f.write(data)
                                        f.flush()
                                        f.close()
                                        print 'se agrego '+nombre_arch
                                        #enviar nuevo archivo a los demas clientes
                                        enviar_data(sock,datacompleta,server_socket)        
                                        break

                                    else:
                                        data = sock.recv(1024)
                                        f.write(data)
                                        recibir = (tam_arch/1024)
                                        ciclo = recibir-1
                                        for i in xrange(ciclo):
                                            data = sock.recv(1024)
                                            f.write(data)
                                        lleva = recibir*1024
                                        recilast = tam_arch-lleva
                                        data = sock.recv(recilast)
                                        f.write(data)
                                        f.flush()
                                        f.close()
                                        print 'se agrego '+nombre_arch
                                        #enviar nuevo archivo a los demas clientes
                                        enviar_data(sock,nombre_arch,server_socket)        
                                        break

                            else:
                                print 'se elimino '+nombre_arch
                                os.remove(nombre_arch)
                                enviar_eliminado(sock,nombre_arch,server_socket) 
                                break
                               
                except:
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
