#!/usr/bin/python
import socket, select, string, sys, os, time

def enviar_nuevo(s,narchivo):

    f=open(narchivo,"rb")                
    l = f.read()
    total = len(l)

    mensaje = '1,'+narchivo+','+str(total)+','
    tam = len(mensaje)
    faltante = 1024-tam
    i=0
    x=1                
    while x==1:
        mensaje = mensaje+'\0'
        i=i+1;
        if i==faltante:
            x=0

    s.send(mensaje)
    
    f.seek(0, 0)
    l = f.read(1024)
    s.send(l)
    while(l):
        l = f.read(1024)
        if l:
            s.send(l)
    f.flush()
    f.close()


def eliminar_arch(s,archivo):
    
    mensaje = '2,'+archivo+','
    tam = len(mensaje)
    faltante = 1024-tam
    i=0
    x=1                
    while x==1:
        mensaje = mensaje+'\0'
        i=i+1;
        if i==faltante:
            x=0

    s.send(mensaje)
 
#main
def main(ADDR,directorio):
     
    #ipv6
    port = 5000     
    addr1 = ADDR + '%eth0'
    addr = (addr1,port)
    
    for res in socket.getaddrinfo(addr[0], addr[1], socket.AF_INET6,socket.SOCK_STREAM, socket.SOL_TCP):
        af, socktype, proto, canonname, sa = res

    s = socket.socket(af,socktype,proto)

    s.settimeout(4)
     
    #conexion al host remoto
    try :
        s.connect((sa))
    except :
        print 'no se puede conectar'
        sys.exit()
     
    print 'Conectado al host remoto.'

    #creacion de carpeta
    nuevacarpeta = str(os.getcwd())+'/'+directorio

    if not os.path.exists(nuevacarpeta):
        os.mkdir(nuevacarpeta)
     
    os.chdir(nuevacarpeta)
    print os.getcwd()

    listaArchivo = os.listdir(os.getcwd())
    while 1:
        #Recibiendo desde servidor
        if s:
            try:
                data0 = s.recv(1024)
                if data0:
                    if len(data0) == 1024:

                        keywords = data0.split(",")
                        tipo = int(keywords[0])
                        nombre_arch = keywords[1]

                        if tipo==1:

                            f = open(nombre_arch,'wb')  
                            tam_arch = int(keywords[2])

                            if tam_arch == 0:
                                f.flush()
                                f.close()
                                print 'se agrego '+nombre_arch
                                listaArchivo.append(nombre_arch)
                            else:
                                if tam_arch < 1024:
                                    data = s.recv(tam_arch)
                                    f.write(data)
                                    f.flush()
                                    f.close()
                                    print 'se agrego '+nombre_arch
                                    listaArchivo.append(nombre_arch)                   
                                else:
                                    recibir = (tam_arch/1024)
                                    for i in xrange(recibir):
                                        data = s.recv(1024)
                                        f.write(data)
                                    lleva = recibir*1024
                                    recilast = tam_arch-lleva
                                    data = s.recv(recilast)
                                    f.write(data)
                                    f.flush()
                                    f.close()
                                    print 'se agrego '+nombre_arch
                                    listaArchivo.append(nombre_arch)
                                    
                        else:
                            print 'se elimino '+nombre_arch
                            listaArchivo.remove(nombre_arch)
                            os.remove(nombre_arch)

            except:
                print 'no hay datos desde servidor'

        #Enviar nuevo
        listaArchivonueva = os.listdir(os.getcwd())

        nuevo=0
        for i in range(len(listaArchivonueva)):
            if nuevo==0:    
                for j in range(len(listaArchivo)):  
                    if listaArchivonueva[i]==listaArchivo[j]:
                        nuevo=0
                        break;
                    else:
                        nuevo=1
                        auxi = i
                        
        if nuevo==1:
            print 'agregado '+listaArchivonueva[auxi]
            listaArchivo.append(listaArchivonueva[auxi])
            archenvio=listaArchivonueva[auxi]
            enviar_nuevo(s,archenvio)

        if len(listaArchivo)==0:
            if not len(listaArchivonueva)==0:
                listaArchivo.append(listaArchivonueva[0])
                archenvio=listaArchivonueva[0]
                enviar_nuevo(s,archenvio)
                
        #Eliminar
        if len(listaArchivonueva)==0:
            if not len(listaArchivo)==0:
                elimi = listaArchivo[0]
                listaArchivo.remove(listaArchivo[0])
                eliminar_arch(s,elimi)

        eliminado=0
        for i in range(len(listaArchivo)):
            if eliminado==0:    
                for j in range(len(listaArchivonueva)):  
                    if listaArchivonueva[j]==listaArchivo[i]:
                        eliminado=0
                        break;
                    else:
                        eliminado=1
                        auxi = i
                        
        if eliminado==1:
            print 'eliminado '+listaArchivo[auxi]
            elimi = listaArchivo[auxi]
            listaArchivo.remove(listaArchivo[auxi])
            eliminar_arch(s,elimi)


        #time.sleep(2)
                        
        
                    
               
