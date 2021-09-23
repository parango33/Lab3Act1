import socket
import sys
import os 
import hashlib
# Crear socket tcp/ip
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conectar socket al puerto
server_address = ('localhost', 10000)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

#archivo a transmitir
filename = "archivo.txt"
tamano_archivo = os.path.getsize(filename)

bytes_read = "oe"
f = open(filename,'rb')
l = f.read(1024)
hashmd5 = hashlib.md5() 

hashmd5.update(l.decode("utf-8").encode())

# Listen for incoming connections
sock.listen(1)

while True:
    # Espera por una conexion
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print (sys.stderr, 'connection from', client_address)

        # Recibir datos y retransmitirlos
        while True:
            data = connection.recv(16)
            print (sys.stderr, 'received "%s"' % data)
            if data:
                print (sys.stderr, 'sending data back to the client')
                connection.sendall(data)
                print(hashmd5.hexdigest())
                connection.sendall(bytes(hashmd5.hexdigest(), 'utf-8'))
            else:
                print (sys.stderr, 'no more data from', client_address)
                break
            
    finally:
        # cerrar coneccion
        connection.close()