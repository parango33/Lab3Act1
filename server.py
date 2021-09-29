import socket
import sys
import os 
import hashlib
import datetime
# Crear socket tcp/ip
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Creación del Log
log = open("./"+datetime.today().strftime('%Y-%m-%d-%H:%M:%S')+"./txt", "w")

# conectar socket al puerto
server_address = ('localhost', 10000)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

#archivo a transmitir
filename = "100mb.txt"
tamano_archivo = os.path.getsize(filename)

#Leemos la primera linea del archivo 
f = open(filename,'rb')
l = f.read(1024)


archivo = open(filename, 'rb')
buf = archivo.read(1024)
md5 = hashlib.md5() 

while(buf):
    md5.update(buf)
    buf = archivo.read(1024)

#Saca el hash del archivo
    
# Listen for incoming connections
sock.listen(1)

while True:
    # Espera por una conexion
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print (sys.stderr, 'connection from', client_address)
        data = connection.recv(32)
        connection.sendall(b'ok')
        data = connection.recv(32)
        print(data.decode('utf-8'))
        # Recibir datos y retransmitirlos
        if(data.decode('utf-8')== "listo"):
            connection.sendall(bytes(md5.hexdigest(), 'utf-8'))
            #Enviamos linea por linea el archivo
            recibido = connection.recv(32)
            if(recibido.decode('utf-8') == 'Hash recibido'):
                while (l):
                    connection.send(l) 
                    l= f.read(1024)
            
                connection.send(l)
            #Enviamos el hashÑ
            
           # confirmacionArchivo = connection.recv(32)
           # print(confirmacionArchivo.decode('utf-8'))
            #if(confirmacionArchivo.decode('utf-8')== "Archivo leido"):
               # connection.send(bytes(md5.hexdigest(), 'utf-8'))
            print("MD5: {0}".format(md5.hexdigest())) 
            
        
            
    finally:
        # cerrar coneccion
        connection.close()