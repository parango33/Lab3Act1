import socket
import sys
import hashlib
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar socket al puerto donde se esta escuchando
server_address = ('localhost', 10000)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)
file = open("./archivosRecibidos/Cliente1-prueba-1.txt", "w")

try:
    
    # Enviar datos
    message = b'Iniciar conexion...'
    print (sys.stderr, 'enviando "%s"' % message)
    sock.sendall(message)

    # buscar la respuesta
    amount_received = 0
    amount_expected = len(message)
    confirmacion = sock.recv(32)
    print(confirmacion.decode('utf-8'))
    #hash a comparar
    md5 = hashlib.md5()
    if(confirmacion.decode('utf-8') == "ok"):
        sock.sendall(b'listo')
        hash = sock.recv(32)
        print(hash.decode('utf-8'))
        sock.sendall(b'Hash recibido')
        while True:
            data = sock.recv(1024)
            
            if data:
                try:
                    file.write(data.decode('utf-8') + os.linesep)
                    md5.update(data)
                    
                except:
                    print("Error") 

                
            else:
                print (sys.stderr, 'Termino de leer el archivo')
                break
        file.close()
        sock.sendall(b'Archivo leido')
        print("MD5: {0}".format(md5.hexdigest()))  
        #hash = sock.recv(1024) 
        print(hash.decode('utf-8')) 
        if(hash.decode('utf-8') == md5.hexdigest()):
            print("Archivo leido enviado correctamente")
        else:
            print("hubo un error al momento de leer el archivoÑ")

finally:
    print (sys.stderr, 'Cerrar socket')
    sock.close()