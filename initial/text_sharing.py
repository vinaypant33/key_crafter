import threading
import socket

import os
from time import time



def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except Exception as Error:
        print(f"Unable to Get IP Address {Error}")
    finally:
        s.close()
    return ip_address


def start_server(host, port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        
        # Continuously listen for incoming messages
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received message from {addr}: {data}")
        
        conn.close()
        
def send_message(server_ip, port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")
        
        while True:
            message = input("Enter message to send (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode())
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client_socket.close()
    


if __name__:
    print(get_local_ip())
    local_ip = get_local_ip()
    print(f"Your current IP address is: {local_ip}")
    
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(local_ip,))
    server_thread.daemon = True
    server_thread.start()

    # Ask the user for the IP address of the other peer to connect to
    peer_ip = input("Enter the IP address of the other computer to connect to: ")
    
    # Start sending messages to the other peer (acts as the client)
    send_message(peer_ip)