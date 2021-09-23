import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar socket al puerto donde se esta escuchando
server_address = ('localhost', 10000)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    
    # Enviar datos
    message = b'Esto es un mensaje'
    print (sys.stderr, 'enviando "%s"' % message)
    sock.sendall(message)

    # buscar la respuesta
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print (sys.stderr, 'Recibido "%s"' % data)

finally:
    print (sys.stderr, 'Cerrar socket')
    sock.close()