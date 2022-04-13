
import socket
import threading


def start_server():
    """
    Start the server and wait for the other RPi to connect
    """
    
    # Create a socket with IPv4 and TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('- Socket created')
    
    # Reserve port number
    port = 12345 

    # Bind any address to port number
    s.bind(('', port))

    # Socket is listening for clients
    # Max 1 clients
    s.listen(1)
    print('- Listening for clients..')
    
    # Accept client and crate a socket object and the associated IP
    client, addr = s.accept()
    print(f'- {addr} connected')
    
    while True:
        # Receive data from client with the temperature
        data = client.recv(1024)
        print(f'TEMPERATURE: {data.decode()}')
        
        if not data:
            break
        elif float(data.decode()) >= 24:
            break
    
    # Close connections
    client.close()
    s.close()


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        exit()

